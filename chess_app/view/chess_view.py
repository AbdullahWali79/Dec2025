"""
Chess View - Handles the GUI and user interface.
Uses PyQt5 for the desktop application interface with a visual chess board.
"""

import os
import chess
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QPushButton, QLabel, QMessageBox,
                             QToolBar, QComboBox, QFileDialog, QSizePolicy, 
                             QProgressDialog, QApplication, QDialog, QDialogButtonBox,
                             QListWidget, QListWidgetItem, QSplitter, QSlider, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QThread, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor


class SquareWidget(QLabel):
    """
    A clickable square widget for the chess board.
    Represents a single square on the chess board.
    """
    
    clicked = pyqtSignal(int, int)  # rank, file
    
    def __init__(self, rank, file, is_light):
        """
        Initialize a square widget.
        
        Args:
            rank (int): Rank (0-7, where 0 is rank 8, 7 is rank 1)
            file (int): File (0-7, where 0 is file a, 7 is file h)
            is_light (bool): True if light square, False if dark square
        """
        super().__init__()
        self.rank = rank
        self.file = file
        self.is_light = is_light
        self.is_highlighted = False
        self.piece_symbol = None
        self.piece_color = None
        self.piece_bold = True
        self.piece_size_factor = 100
        
        # Set square color
        self._update_color()
        
        # Set size policy to maintain square aspect
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(50, 50)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
    
    def _update_color(self):
        """Update the square's background color based on its state."""
        # ALWAYS use uniform dark background - never change to alternating colors
        base_color = QColor(52, 73, 94)  # #34495e - uniform dark blue-gray matching app theme
        
        if self.is_highlighted:
            # Highlight color (light blue) with visible white border
            bg_color = QColor(173, 216, 230)  # Light blue
            border = "2px solid #FFFFFF"  # White border for highlighted squares
        else:
            # Uniform dark background for ALL squares (ignoring is_light flag)
            bg_color = base_color
            border = "1px solid #FFFFFF"  # White border for all squares
        
        # Preserve piece color if it exists
        piece_color_part = ""
        if self.piece_color:
            piece_color_part = f"color: {self.piece_color}; "
        
        # Preserve font weight
        font_weight = "bold" if self.piece_bold else "normal"
        
        # Apply background color and border while preserving piece color
        self.setStyleSheet(f"background-color: {bg_color.name()}; {piece_color_part}font-weight: {font_weight}; border: {border};")
    
    def set_highlight(self, highlighted):
        """
        Set the highlight state of the square.
        
        Args:
            highlighted (bool): True to highlight, False to unhighlight
        """
        self.is_highlighted = highlighted
        self._update_color()
    
    def set_piece(self, piece_symbol, piece_color=None, bold=True, size_factor=100):
        """
        Set the piece symbol displayed on this square.
        
        Args:
            piece_symbol (str): Unicode chess piece symbol or None
            piece_color (str): Color hex code for the piece (e.g., "#FFFFFF")
            bold (bool): Whether to make the piece bold
            size_factor (int): Size factor in percentage (100 = normal, 150 = 1.5x, etc.)
        """
        self.piece_symbol = piece_symbol
        self.piece_color = piece_color
        self.piece_bold = bold
        self.piece_size_factor = size_factor
        
        if piece_symbol:
            self.setText(piece_symbol)
            self._update_font_size()
            
            # Apply piece color and update square color (which will preserve piece color)
            # First store piece color, then call _update_color which will preserve it
            self._update_color()
        else:
            self.setText("")
            self.piece_color = None
            # Update square color without piece
            self._update_color()
    
    def _update_font_size(self):
        """Update font size based on current square size and size factor."""
        if not self.piece_symbol:
            return
        
        # Get actual square size (use geometry if width is 0)
        square_size = max(self.width(), self.height(), self.geometry().width(), self.geometry().height())
        if square_size == 0:
            square_size = 80  # Default fallback size
        
        # Calculate base font size (use a larger portion of the square - 70% for better visibility)
        base_size = max(16, int(square_size * 0.7))  # Use 70% of square size as base
        
        # Apply size factor
        font_size = int(base_size * (self.piece_size_factor / 100.0))
        font_size = max(12, min(font_size, 300))  # Clamp between 12 and 300
        
        font = QFont("Arial", font_size)
        font.setBold(self.piece_bold)
        self.setFont(font)
    
    def mousePressEvent(self, event):
        """Handle mouse click on the square."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.rank, self.file)
        super().mousePressEvent(event)
    
    def resizeEvent(self, event):
        """Adjust font size when square is resized."""
        super().resizeEvent(event)
        if self.piece_symbol:
            self._update_font_size()


class PromotionDialog(QDialog):
    """Dialog for selecting pawn promotion piece."""
    
    def __init__(self, parent=None, is_white=True):
        """
        Initialize promotion dialog.
        
        Args:
            parent: Parent widget
            is_white (bool): True if promoting white pawn, False for black
        """
        super().__init__(parent)
        self.selected_piece = chess.QUEEN  # Default to queen
        self.is_white = is_white
        
        self.setWindowTitle("Pawn Promotion")
        self.setModal(True)
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        label = QLabel("Choose promotion piece:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Button layout for pieces
        button_layout = QHBoxLayout()
        
        # Piece options: Queen, Rook, Bishop, Knight
        pieces = [
            (chess.QUEEN, "Queen", "♕" if is_white else "♛"),
            (chess.ROOK, "Rook", "♖" if is_white else "♜"),
            (chess.BISHOP, "Bishop", "♗" if is_white else "♝"),
            (chess.KNIGHT, "Knight", "♘" if is_white else "♞")
        ]
        
        self.buttons = []
        for piece_type, name, symbol in pieces:
            btn = QPushButton(f"{symbol}\n{name}")
            btn.setMinimumSize(60, 80)
            btn.clicked.connect(lambda checked, p=piece_type: self._select_piece(p))
            button_layout.addWidget(btn)
            self.buttons.append((btn, piece_type))
            if piece_type == chess.QUEEN:
                btn.setDefault(True)
        
        layout.addLayout(button_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def _select_piece(self, piece_type):
        """Select a promotion piece."""
        self.selected_piece = piece_type
        # Highlight selected button
        for btn, p_type in self.buttons:
            if p_type == piece_type:
                btn.setStyleSheet("background-color: #3498db; font-weight: bold;")
            else:
                btn.setStyleSheet("")
    
    def get_selected_piece(self):
        """Get the selected promotion piece type."""
        return self.selected_piece


class EndOfGameDialog(QDialog):
    """Dialog shown when game ends (checkmate, stalemate, draw)."""
    
    def __init__(self, parent=None, result_type="", message=""):
        """
        Initialize end-of-game dialog.
        
        Args:
            parent: Parent widget
            result_type (str): Type of result (checkmate, stalemate, draw)
            message (str): Result message to display
        """
        super().__init__(parent)
        self.result_type = result_type
        self.choice = None  # "new_game" or "close"
        
        self.setWindowTitle("Game Over")
        self.setModal(True)
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout()
        
        # Result message
        result_label = QLabel(message)
        result_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        result_label.setFont(font)
        layout.addWidget(result_label)
        
        layout.addSpacing(20)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        new_game_btn = QPushButton("New Game")
        new_game_btn.setMinimumHeight(40)
        new_game_btn.clicked.connect(lambda: self._make_choice("new_game"))
        button_layout.addWidget(new_game_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setMinimumHeight(40)
        close_btn.clicked.connect(lambda: self._make_choice("close"))
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _make_choice(self, choice):
        """Set the user's choice and close dialog."""
        self.choice = choice
        self.accept()
    
    def get_choice(self):
        """Get the user's choice."""
        return self.choice


class ChessView(QMainWindow):
    """
    Main window for the chess application with visual chess board.
    """
    
    # Signals for user interactions
    square_clicked = pyqtSignal(int, int)  # rank, file
    new_game_requested = pyqtSignal()
    undo_requested = pyqtSignal()
    mode_toggled = pyqtSignal(str)  # "human" or "ai"
    difficulty_changed = pyqtSignal(int)  # depth level
    piece_folder_loaded = pyqtSignal(str)  # folder path
    move_history_clicked = pyqtSignal(int)  # move index to jump to
    refresh_board_requested = pyqtSignal()  # Request to refresh board display
    
    # Unicode chess piece symbols (fallback when PNG not available)
    UNICODE_PIECES = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',  # White
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'   # Black
    }
    
    def __init__(self):
        """Initialize the chess view."""
        super().__init__()
        self.setWindowTitle("Chess Desktop Application")
        self.setMinimumSize(600, 600)
        
        # Piece image folder path
        self.piece_folder = "assets/pieces"
        self.piece_images = {}  # Cache for piece images
        
        # Ensure assets folder exists
        os.makedirs(self.piece_folder, exist_ok=True)
        
        # Piece display settings (from settings.json or defaults) - MUST be before _check_and_download_pieces
        self.piece_color_white = "#FFFFFF"  # White pieces color
        self.piece_color_black = "#000000"  # Black pieces color
        self.piece_bold = True  # Bold pieces
        self.use_unicode_only = True  # Use Unicode only, skip image download
        self.piece_size_factor = 100  # Size factor in percentage (100 = normal, 150 = 1.5x, etc.)
        
        # Load piece display settings
        self._load_piece_settings()
        
        # Check for pieces and download if missing (on first run)
        self._check_and_download_pieces()
        
        # Game mode: "human" (human vs human) or "ai" (human vs AI)
        self.game_mode = "human"
        
        # Selected squares for move input
        self.selected_square = None
        self.highlighted_squares = []
        
        # Move history
        self.move_history_list = None
        
        # Set window icon if available
        try:
            self.setWindowIcon(QIcon("assets/icon.ico"))
        except:
            pass
        
        # Apply blue-gray theme
        self._apply_theme()
        
        # Create toolbar (settings already loaded)
        self._create_toolbar()
        
        # Create central widget and board
        self._create_board()
        
        # Create status bar
        self._create_status_bar()
    
    def _apply_theme(self):
        """Apply blue-gray theme using Qt StyleSheets."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b3e50;
            }
            QWidget {
                background-color: #34495e;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
                color: #95a5a6;
            }
            QComboBox {
                background-color: #34495e;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 4px;
                padding: 4px;
                min-width: 100px;
            }
            QComboBox:hover {
                border-color: #2980b9;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #34495e;
                color: #ecf0f1;
                selection-background-color: #3498db;
            }
            QLabel {
                color: #ecf0f1;
            }
            QToolBar {
                background-color: #34495e;
                border: none;
                spacing: 5px;
            }
            QStatusBar {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
        """)
    
    def _create_toolbar(self):
        """Create the toolbar with game controls."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # New Game button
        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self._on_new_game_clicked)
        toolbar.addWidget(new_game_btn)
        
        # Undo button
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self._on_undo_clicked)
        toolbar.addWidget(self.undo_btn)
        
        toolbar.addSeparator()
        
        # Mode toggle button
        self.mode_btn = QPushButton("Mode: Human vs Human")
        self.mode_btn.clicked.connect(self._on_mode_toggle)
        toolbar.addWidget(self.mode_btn)
        
        toolbar.addSeparator()
        
        # Difficulty dropdown
        difficulty_label = QLabel("Difficulty:")
        toolbar.addWidget(difficulty_label)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy (Depth 1)", "Medium (Depth 2)", "Hard (Depth 3)", "Expert (Depth 4)"])
        self.difficulty_combo.setCurrentIndex(1)  # Default to Medium
        self.difficulty_combo.currentIndexChanged.connect(self._on_difficulty_changed)
        toolbar.addWidget(self.difficulty_combo)
        
        toolbar.addSeparator()
        
        # Piece color controls
        color_label = QLabel("Piece Colors:")
        toolbar.addWidget(color_label)
        
        # White piece color selector
        self.white_color_combo = QComboBox()
        white_colors = ["White (#FFFFFF)", "Light Gray (#E0E0E0)", "Yellow (#FFFF00)", "Cyan (#00FFFF)", "Pink (#FFC0CB)"]
        self.white_color_combo.addItems(white_colors)
        # Set current index based on loaded settings
        white_index = self._get_color_index(self.piece_color_white, [0, 1, 2, 3, 4], ["#FFFFFF", "#E0E0E0", "#FFFF00", "#00FFFF", "#FFC0CB"])
        self.white_color_combo.setCurrentIndex(white_index)
        self.white_color_combo.currentIndexChanged.connect(self._on_white_color_changed)
        toolbar.addWidget(self.white_color_combo)
        
        # Black piece color selector
        self.black_color_combo = QComboBox()
        black_colors = ["Black (#000000)", "Dark Gray (#404040)", "Blue (#0000FF)", "Red (#FF0000)", "Green (#008000)"]
        self.black_color_combo.addItems(black_colors)
        # Set current index based on loaded settings
        black_index = self._get_color_index(self.piece_color_black, [0, 1, 2, 3, 4], ["#000000", "#404040", "#0000FF", "#FF0000", "#008000"])
        self.black_color_combo.setCurrentIndex(black_index)
        self.black_color_combo.currentIndexChanged.connect(self._on_black_color_changed)
        toolbar.addWidget(self.black_color_combo)
        
        toolbar.addSeparator()
        
        # Piece size control
        size_label = QLabel("Piece Size:")
        toolbar.addWidget(size_label)
        
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setMinimum(50)
        self.size_spinbox.setMaximum(200)
        self.size_spinbox.setSuffix("%")
        self.size_spinbox.setValue(self.piece_size_factor)
        self.size_spinbox.setToolTip("Adjust piece icon size (50% to 200%)")
        self.size_spinbox.valueChanged.connect(self._on_size_changed)
        toolbar.addWidget(self.size_spinbox)
        
        toolbar.addSeparator()
        
        # Load piece folder button
        load_pieces_btn = QPushButton("Load Piece Folder")
        load_pieces_btn.clicked.connect(self._on_load_piece_folder)
        toolbar.addWidget(load_pieces_btn)
    
    def _create_board(self):
        """Create the chess board with grid layout."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        central_widget.setLayout(main_layout)
        
        # Board container widget
        board_container = QWidget()
        board_layout = QVBoxLayout()
        board_container.setLayout(board_layout)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(0)
        
        # Top coordinates (A-H)
        top_coords = QHBoxLayout()
        top_coords.addWidget(QLabel(""))  # Space for rank numbers
        for file in range(8):
            coord_label = QLabel(chr(ord('a') + file).upper())
            coord_label.setAlignment(Qt.AlignCenter)
            coord_label.setMinimumWidth(50)
            coord_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            top_coords.addWidget(coord_label)
        top_coords.addWidget(QLabel(""))  # Space for rank numbers
        board_layout.addLayout(top_coords)
        
        # Board grid with squares
        board_widget = QWidget()
        self.board_grid = QGridLayout()
        self.board_grid.setContentsMargins(0, 0, 0, 0)
        self.board_grid.setSpacing(0)
        board_widget.setLayout(self.board_grid)
        
        # Create squares
        self.squares = []
        for rank in range(8):
            row = []
            # Left rank number (8-1)
            rank_label = QLabel(str(8 - rank))
            rank_label.setAlignment(Qt.AlignCenter)
            rank_label.setMinimumWidth(20)
            rank_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.board_grid.addWidget(rank_label, rank, 0)
            
            # Chess squares
            for file in range(8):
                is_light = (rank + file) % 2 == 0
                square = SquareWidget(rank, file, is_light)
                square.clicked.connect(self.on_square_clicked)
                self.board_grid.addWidget(square, rank, file + 1)
                row.append(square)
            
            # Right rank number (8-1)
            rank_label = QLabel(str(8 - rank))
            rank_label.setAlignment(Qt.AlignCenter)
            rank_label.setMinimumWidth(20)
            rank_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.board_grid.addWidget(rank_label, rank, 9)
            
            self.squares.append(row)
        
        board_layout.addWidget(board_widget)
        
        # Bottom coordinates (A-H)
        bottom_coords = QHBoxLayout()
        bottom_coords.addWidget(QLabel(""))  # Space for rank numbers
        for file in range(8):
            coord_label = QLabel(chr(ord('a') + file).upper())
            coord_label.setAlignment(Qt.AlignCenter)
            coord_label.setMinimumWidth(50)
            coord_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            bottom_coords.addWidget(coord_label)
        bottom_coords.addWidget(QLabel(""))  # Space for rank numbers
        board_layout.addLayout(bottom_coords)
        
        # Add board container directly to main layout (no splitter, no move history)
        main_layout.addWidget(board_container)
    
    def _create_move_history_panel(self):
        """Create the move history panel."""
        history_widget = QWidget()
        history_layout = QVBoxLayout()
        history_widget.setLayout(history_layout)
        
        # Title
        title = QLabel("Move History")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        history_layout.addWidget(title)
        
        # Move history list
        self.move_history_list = QListWidget()
        self.move_history_list.itemClicked.connect(self._on_move_history_clicked)
        self.move_history_list.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #34495e;
            }
        """)
        history_layout.addWidget(self.move_history_list)
        
        return history_widget
    
    def _on_move_history_clicked(self, item):
        """Handle move history item click."""
        row = self.move_history_list.row(item)
        self.move_history_clicked.emit(row)
    
    def update_move_history(self, moves):
        """
        Update the move history display.
        
        Args:
            moves (list): List of tuples (move_number, white_move, black_move, algebraic_notation)
        """
        if not self.move_history_list:
            return
        
        self.move_history_list.clear()
        
        for move_data in moves:
            if len(move_data) == 4:
                move_num, white_move, black_move, notation = move_data
                if black_move:
                    text = f"{move_num}. {white_move} {black_move}"
                else:
                    text = f"{move_num}. {white_move}"
                self.move_history_list.addItem(text)
            else:
                # Fallback format
                self.move_history_list.addItem(str(move_data))
    
    def show_promotion_dialog(self, is_white=True):
        """
        Show promotion dialog and return selected piece.
        
        Args:
            is_white (bool): True if promoting white pawn
            
        Returns:
            int or None: Selected piece type (chess.QUEEN, etc.) or None if cancelled
        """
        dialog = PromotionDialog(self, is_white)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.get_selected_piece()
        return None
    
    def show_end_of_game_dialog(self, result_type, message):
        """
        Show end-of-game dialog.
        
        Args:
            result_type (str): Type of result (checkmate, stalemate, draw)
            message (str): Result message
            
        Returns:
            str or None: User choice ("new_game" or "close") or None if cancelled
        """
        dialog = EndOfGameDialog(self, result_type, message)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.get_choice()
        return None
    
    def _create_status_bar(self):
        """Create the status bar."""
        self.statusBar().showMessage("White to move")
    
    def resizeEvent(self, event):
        """
        Handle window resize to maintain square aspect ratio.
        
        Args:
            event: Resize event
        """
        super().resizeEvent(event)
        # Calculate square size based on available space
        # This maintains square aspect ratio
        if hasattr(self, 'board_grid') and self.squares:
            # Get central widget size
            central = self.centralWidget()
            if central:
                available_width = central.width() - 80  # Account for coordinates and margins
                available_height = central.height() - 80  # Account for coordinates and margins
                square_size = min(available_width // 8, available_height // 8)
                square_size = max(50, square_size)  # Minimum size
                
                # Set square sizes to maintain square aspect
                for row in self.squares:
                    for square in row:
                        square.setMinimumSize(square_size, square_size)
                        square.setMaximumSize(square_size, square_size)
                        
                # Update piece images if they're pixmaps
                self._refresh_piece_images()
    
    def _refresh_piece_images(self):
        """Refresh piece images after resize."""
        if not hasattr(self, 'squares'):
            return
        
        for row in self.squares:
            for square in row:
                if square.piece_symbol:
                    piece_image = self._load_piece_image(square.piece_symbol)
                    if isinstance(piece_image, QPixmap):
                        square.setPixmap(piece_image.scaled(
                            square.size(),
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        ))
    
    def _load_piece_settings(self):
        """Load piece display settings from settings.json."""
        try:
            import json
            if os.path.exists("settings.json"):
                with open("settings.json", 'r') as f:
                    settings = json.load(f)
                    self.piece_color_white = settings.get("piece_color_white", "#FFFFFF")
                    self.piece_color_black = settings.get("piece_color_black", "#000000")
                    self.piece_bold = settings.get("piece_bold", True)
                    self.use_unicode_only = settings.get("use_unicode_only", True)
                    self.piece_size_factor = settings.get("piece_size_factor", 100)
        except Exception as e:
            # Use defaults if settings file doesn't exist or error
            pass
    
    def _load_piece_image(self, piece_char):
        """
        Load piece image from file or return Unicode fallback.
        Now prioritizes Unicode if use_unicode_only is True.
        
        Args:
            piece_char (str): Piece character (K, Q, R, B, N, P or lowercase)
            
        Returns:
            str: Unicode symbol (always returns Unicode now)
        """
        # If use_unicode_only is True, skip image loading
        if self.use_unicode_only:
            unicode_symbol = self.UNICODE_PIECES.get(piece_char, '')
            return unicode_symbol
        
        # Check cache first
        if piece_char in self.piece_images:
            cached = self.piece_images[piece_char]
            if isinstance(cached, str):
                return cached  # Already Unicode
            return cached  # Pixmap
        
        # Try to load PNG image (only if not unicode_only)
        piece_name_map = {
            'K': 'white_king', 'Q': 'white_queen', 'R': 'white_rook',
            'B': 'white_bishop', 'N': 'white_knight', 'P': 'white_pawn',
            'k': 'black_king', 'q': 'black_queen', 'r': 'black_rook',
            'b': 'black_bishop', 'n': 'black_knight', 'p': 'black_pawn'
        }
        
        piece_name = piece_name_map.get(piece_char)
        if piece_name and self.piece_folder:
            # Try common extensions (PNG preferred, then SVG)
            for ext in ['.png', '.svg', '.jpg', '.jpeg']:
                image_path = os.path.join(self.piece_folder, f"{piece_name}{ext}")
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        self.piece_images[piece_char] = pixmap
                        return pixmap
        
        # Fallback to Unicode
        unicode_symbol = self.UNICODE_PIECES.get(piece_char, '')
        self.piece_images[piece_char] = unicode_symbol
        return unicode_symbol
    
    def _get_piece_color(self, piece_char):
        """Get color for a piece based on settings."""
        if piece_char.isupper():
            return self.piece_color_white  # White pieces
        else:
            return self.piece_color_black  # Black pieces
    
    def _get_color_index(self, color_value, indices, color_list):
        """Get combo box index for a given color value."""
        try:
            return color_list.index(color_value.upper())
        except (ValueError, AttributeError):
            return 0  # Default to first option
    
    def on_square_clicked(self, rank, file):
        """
        Handle square click event.
        
        Args:
            rank (int): Rank (0-7)
            file (int): File (0-7)
        """
        self.square_clicked.emit(rank, file)
    
    def update_board_from_fen(self, fen):
        """
        Update the board display from a FEN string.
        
        Args:
            fen (str): FEN string representing the chess position
        """
        try:
            board = chess.Board(fen)
            
            # Clear highlights
            self.highlight_squares([])
            self.selected_square = None
            
            # Update each square
            for rank in range(8):
                for file in range(8):
                    square = self.squares[rank][file]
                    chess_square = chess.square(file, 7 - rank)  # Convert to chess square
                    piece = board.piece_at(chess_square)
                    
                    # IMPORTANT: Preserve square background color (uniform dark)
                    # Only update pieces, not square colors
                    
                    if piece:
                        piece_char = piece.symbol()
                        
                        if self.use_unicode_only or not isinstance(self._load_piece_image(piece_char), QPixmap):
                            # Display as Unicode symbol with color, bold, and size
                            unicode_symbol = self.UNICODE_PIECES.get(piece_char, '')
                            piece_color = self._get_piece_color(piece_char)
                            square.set_piece(unicode_symbol, piece_color, self.piece_bold, self.piece_size_factor)
                            square.piece_symbol = piece_char  # Store for refresh
                        else:
                            # Display as image (only if not unicode_only and image exists)
                            piece_image = self._load_piece_image(piece_char)
                            if isinstance(piece_image, QPixmap):
                                square.setPixmap(piece_image.scaled(
                                    square.size(),
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation
                                ))
                                square.setText("")
                                square.piece_symbol = piece_char  # Store for refresh
                    else:
                        square.set_piece(None)
                        square.setPixmap(QPixmap())
                        square.piece_symbol = None
                    
                    # Ensure square maintains uniform dark background after piece update
                    if not square.is_highlighted:
                        square._update_color()
            
            # Update status
            turn = "White" if board.turn == chess.WHITE else "Black"
            status = f"{turn} to move"
            
            if board.is_checkmate():
                status = f"Checkmate! {'Black' if board.turn == chess.WHITE else 'White'} wins!"
            elif board.is_stalemate():
                status = "Stalemate - Draw"
            elif board.is_check():
                status = f"{turn} is in check!"
            
            self.statusBar().showMessage(status)
            
            # Force font size update after layout is complete
            # Use QTimer to delay slightly to ensure squares have their final size
            QTimer.singleShot(100, self._update_all_font_sizes)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update board from FEN: {str(e)}")
    
    def _update_all_font_sizes(self):
        """Force update font sizes for all squares with pieces."""
        if hasattr(self, 'squares'):
            for row in self.squares:
                for square in row:
                    if hasattr(square, 'piece_symbol') and square.piece_symbol:
                        square._update_font_size()
    
    def highlight_squares(self, squares):
        """
        Highlight specified squares on the board.
        
        Args:
            squares (list): List of (rank, file) tuples or chess square indices
        """
        # Clear previous highlights
        for row in self.squares:
            for square in row:
                square.set_highlight(False)
        
        # Highlight new squares
        self.highlighted_squares = []
        for square_ref in squares:
            if isinstance(square_ref, tuple):
                rank, file = square_ref
            elif isinstance(square_ref, int):
                # Convert chess square index to rank, file
                file = chess.square_file(square_ref)
                rank = 7 - chess.square_rank(square_ref)
            else:
                continue
            
            if 0 <= rank < 8 and 0 <= file < 8:
                self.squares[rank][file].set_highlight(True)
                self.highlighted_squares.append((rank, file))
    
    def _on_new_game_clicked(self):
        """Handle new game button click."""
        reply = QMessageBox.question(
            self, "New Game",
            "Start a new game?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.new_game_requested.emit()
    
    def _on_undo_clicked(self):
        """Handle undo button click."""
        self.undo_requested.emit()
    
    def _on_mode_toggle(self):
        """Handle mode toggle button click."""
        if self.game_mode == "human":
            self.game_mode = "ai"
            self.mode_btn.setText("Mode: Human vs AI")
        else:
            self.game_mode = "human"
            self.mode_btn.setText("Mode: Human vs Human")
        self.mode_toggled.emit(self.game_mode)
    
    def _on_difficulty_changed(self, index):
        """Handle difficulty dropdown change."""
        depth = index + 1  # Easy=1, Medium=2, Hard=3, Expert=4
        self.difficulty_changed.emit(depth)
    
    def _on_white_color_changed(self, index):
        """Handle white piece color change."""
        color_map = {
            0: "#FFFFFF",  # White
            1: "#E0E0E0",  # Light Gray
            2: "#FFFF00",  # Yellow
            3: "#00FFFF",  # Cyan
            4: "#FFC0CB"   # Pink
        }
        self.piece_color_white = color_map.get(index, "#FFFFFF")
        self._save_piece_settings()
        # Refresh board to apply new colors
        self._refresh_board_colors()
        # Request full board refresh from controller
        self.refresh_board_requested.emit()
    
    def _on_black_color_changed(self, index):
        """Handle black piece color change."""
        color_map = {
            0: "#000000",  # Black
            1: "#404040",  # Dark Gray
            2: "#0000FF",  # Blue
            3: "#FF0000",  # Red
            4: "#008000"   # Green
        }
        self.piece_color_black = color_map.get(index, "#000000")
        self._save_piece_settings()
        # Refresh board to apply new colors
        self._refresh_board_colors()
        # Request full board refresh from controller
        self.refresh_board_requested.emit()
    
    def _on_size_changed(self, value):
        """Handle piece size change."""
        self.piece_size_factor = value
        self._save_piece_settings()
        # Refresh board to apply new size
        self._refresh_board_colors()
        # Request full board refresh from controller
        self.refresh_board_requested.emit()
    
    def _save_piece_settings(self):
        """Save piece display settings to settings.json."""
        try:
            import json
            # Load existing settings
            settings = {}
            if os.path.exists("settings.json"):
                with open("settings.json", 'r') as f:
                    settings = json.load(f)
            
            # Update piece settings
            settings["piece_color_white"] = self.piece_color_white
            settings["piece_color_black"] = self.piece_color_black
            settings["piece_bold"] = self.piece_bold
            settings["use_unicode_only"] = self.use_unicode_only
            settings["piece_size_factor"] = self.piece_size_factor
            
            # Save settings
            with open("settings.json", 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            pass  # Silently fail
    
    def _refresh_board_colors(self):
        """Refresh board to apply new piece colors and size."""
        # Update each square that has a piece with new colors and size
        # IMPORTANT: Do NOT change square background colors, only update pieces
        # set_piece() will automatically call _update_color() which preserves piece color
        if hasattr(self, 'squares'):
            for row in self.squares:
                for square in row:
                    if hasattr(square, 'piece_symbol') and square.piece_symbol:
                        piece_char = square.piece_symbol
                        piece_color = self._get_piece_color(piece_char)
                        unicode_symbol = self.UNICODE_PIECES.get(piece_char, '')
                        # set_piece will handle updating both piece and square colors
                        square.set_piece(unicode_symbol, piece_color, self.piece_bold, self.piece_size_factor)
    
    def _check_and_download_pieces(self):
        """Check if piece images exist and download if missing."""
        # Skip download if using Unicode only
        if self.use_unicode_only:
            return
        
        try:
            import sys
            import os
            # Add parent directory to path for imports
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from utils.asset_downloader import check_pieces_folder, ensure_default_pieces
            
            # Check what pieces are available
            piece_status = check_pieces_folder(self.piece_folder)
            missing_count = sum(1 for exists in piece_status.values() if not exists)
            
            if missing_count > 0:
                # Ask user if they want to download
                reply = QMessageBox.question(
                    self,
                    "Missing Chess Pieces",
                    f"{missing_count} chess piece images are missing.\n\n"
                    "Would you like to download default pieces from Wikimedia Commons?\n"
                    "(This is a one-time download, open-license images)",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.Yes:
                    self._download_pieces_with_progress()
        except ImportError:
            # Asset downloader not available, skip
            pass
        except Exception as e:
            # Silently fail on startup
            pass
    
    def _download_pieces_with_progress(self):
        """Download pieces with progress dialog."""
        try:
            import sys
            import os
            # Add parent directory to path for imports
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            from utils.asset_downloader import ensure_default_pieces
            
            progress = QProgressDialog("Downloading chess pieces...", "Cancel", 0, 12, self)
            progress.setWindowTitle("Downloading Assets")
            progress.setModal(True)
            progress.show()
            
            def progress_callback(message):
                progress.setLabelText(message)
                progress.setValue(progress.value() + 1)
                QApplication.processEvents()
            
            success = ensure_default_pieces(self.piece_folder, progress_callback)
            progress.close()
            
            if success:
                # Clear cache and refresh
                self.piece_images.clear()
                self.statusBar().showMessage("Chess pieces downloaded successfully!", 5000)
                # Refresh board display if controller is ready
                if hasattr(self, 'squares'):
                    self._refresh_piece_images()
            else:
                QMessageBox.warning(
                    self,
                    "Download Incomplete",
                    "Some pieces failed to download.\n"
                    "The application will use Unicode symbols as fallback."
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Download Error",
                f"Failed to download pieces: {str(e)}\n"
                "The application will use Unicode symbols as fallback."
            )
    
    def _on_load_piece_folder(self):
        """Handle load piece folder button click."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Piece Images Folder",
            self.piece_folder or "."
        )
        if folder:
            # Validate folder contains piece images
            try:
                import sys
                import os
                # Add parent directory to path for imports
                parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)
                from utils.asset_downloader import check_pieces_folder
                piece_status = check_pieces_folder(folder)
                found_count = sum(1 for exists in piece_status.values() if exists)
                total_pieces = len(piece_status)
                
                if found_count == 0:
                    # No pieces found - offer to download
                    reply = QMessageBox.question(
                        self,
                        "No Pieces Found",
                        f"No chess piece images found in:\n{folder}\n\n"
                        "Would you like to download default pieces?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )
                    if reply == QMessageBox.Yes:
                        self.piece_folder = folder
                        self._download_pieces_with_progress()
                    else:
                        return
                elif found_count < total_pieces:
                    # Some pieces missing
                    missing = total_pieces - found_count
                    reply = QMessageBox.question(
                        self,
                        "Some Pieces Missing",
                        f"Found {found_count}/{total_pieces} pieces in:\n{folder}\n\n"
                        f"{missing} pieces are missing. Would you like to download them?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )
                    if reply == QMessageBox.Yes:
                        self.piece_folder = folder
                        self._download_pieces_with_progress()
                    else:
                        # Use what we have
                        self.piece_folder = folder
                        self.piece_images.clear()
                        self.piece_folder_loaded.emit(folder)
                        self.statusBar().showMessage(
                            f"Loaded {found_count}/{total_pieces} pieces from folder", 5000
                        )
                else:
                    # All pieces found
                    self.piece_folder = folder
                    self.piece_images.clear()
                    self.piece_folder_loaded.emit(folder)
                    self.statusBar().showMessage(
                        f"Successfully loaded all {found_count} pieces from folder", 5000
                    )
            except ImportError:
                # Fallback if downloader not available
                self.piece_folder = folder
                self.piece_images.clear()
                self.piece_folder_loaded.emit(folder)
                self.statusBar().showMessage(f"Piece folder set to: {folder}", 5000)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Error validating folder: {str(e)}"
                )
    
    def set_undo_enabled(self, enabled):
        """
        Enable or disable the undo button.
        
        Args:
            enabled (bool): True to enable, False to disable
        """
        self.undo_btn.setEnabled(enabled)
    
    def show_game_over_message(self, result):
        """
        Show a message box when the game is over.
        
        Args:
            result (str): Game result message
        """
        QMessageBox.information(self, "Game Over", result)
