"""
Chess Controller - Coordinates between Model, View, and AIEngine.
Handles user input, move validation, AI moves, and game state management.
"""

import os
import json
import chess
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from model.chess_model import ChessModel
from model.ai_engine import AIEngine
from view.chess_view import ChessView


class ChessController:
    """
    Coordinates interactions between the Model, View, and AIEngine.
    Manages game flow, move validation, AI gameplay, and persistence.
    """
    
    def __init__(self, model: ChessModel, view: ChessView):
        """
        Initialize the controller with model and view.
        
        Args:
            model: ChessModel instance
            view: ChessView instance
        """
        self.model = model
        self.view = view
        
        # AI engine (initialized when needed)
        self.ai_engine = None
        self.ai_depth = 2  # Default medium difficulty
        self.game_mode = "human"  # "human" or "ai"
        self.ai_plays_as = chess.BLACK  # AI plays as black by default
        
        # Move selection state
        self.selected_square = None
        self.legal_moves_from_selected = []
        
        # Track moves for undo (to handle AI moves)
        self.move_stack = []  # Track (move, is_ai_move) pairs
        
        # Move history for navigation
        self.move_history = []  # List of (move, fen, notation) tuples
        self.current_position_index = -1  # Current position in history
        
        # Load settings
        self.settings = self._load_settings()
        self._apply_settings()
        
        # Connect view signals to controller methods
        self._connect_signals()
        
        # Initialize the display
        self._update_display()
    
    def _connect_signals(self):
        """Connect all view signals to controller methods."""
        self.view.square_clicked.connect(self._on_square_clicked)
        self.view.new_game_requested.connect(self._on_new_game)
        self.view.undo_requested.connect(self._on_undo)
        self.view.mode_toggled.connect(self._on_mode_toggle)
        self.view.difficulty_changed.connect(self._on_difficulty_changed)
        self.view.piece_folder_loaded.connect(self._on_piece_folder_loaded)
        self.view.move_history_clicked.connect(self._on_move_history_clicked)
        self.view.refresh_board_requested.connect(self._update_display)
    
    def _on_square_clicked(self, rank, file):
        """
        Handle square click from the view.
        
        Implements two-click move selection:
        1. First click: select piece and show legal moves
        2. Second click: make move if legal
        
        Args:
            rank (int): Rank (0-7, where 0 is rank 8)
            file (int): File (0-7, where 0 is file a)
        """
        # Convert view coordinates to chess square
        chess_square = chess.square(file, 7 - rank)
        board = self.model.board
        
        # Check if it's the current player's turn
        if board.is_game_over():
            return
        
        current_turn = board.turn
        
        # If we have a selected square, try to make a move
        if self.selected_square is not None:
            from_square = self.selected_square
            to_square = chess_square
            
            # Check if this is a legal move
            # First, try to find an exact matching move (including promotions)
            matching_moves = [
                m for m in self.legal_moves_from_selected
                if m.from_square == from_square and m.to_square == to_square
            ]
            
            if not matching_moves:
                # No legal move to this square
                move = None
            elif len(matching_moves) == 1:
                # Single move (no promotion or only one promotion variant)
                move = matching_moves[0]
            else:
                # Multiple moves - must be promotion variants
                # Show promotion dialog
                piece = board.piece_at(from_square)
                is_white = piece.color == chess.WHITE if piece else True
                promotion_type = self.view.show_promotion_dialog(is_white)
                
                if promotion_type:
                    # Find move with selected promotion
                    move = next(
                        (m for m in matching_moves if m.promotion == promotion_type),
                        None
                    )
                    if not move:
                        # Fallback to queen
                        move = next(
                            (m for m in matching_moves if m.promotion == chess.QUEEN),
                            matching_moves[0]
                        )
                else:
                    # User cancelled - don't make move
                    return
            
            # Try to make the move
            if move and move in self.legal_moves_from_selected:
                self._make_move(move)
                # Clear selection
                self.selected_square = None
                self.legal_moves_from_selected = []
                self.view.highlight_squares([])
            else:
                # Invalid move - clear selection and start new selection
                self.selected_square = None
                self.legal_moves_from_selected = []
                self.view.highlight_squares([])
                # Try to select this square instead
                self._select_square(chess_square, current_turn)
        else:
            # First click - select square
            self._select_square(chess_square, current_turn)
    
    def _select_square(self, chess_square, current_turn):
        """
        Select a square and show legal moves.
        
        Args:
            chess_square (int): Chess square index
            current_turn (bool): Current player's turn (True=White, False=Black)
        """
        board = self.model.board
        piece = board.piece_at(chess_square)
        
        # Only allow selecting pieces of the current player
        if piece and piece.color == current_turn:
            self.selected_square = chess_square
            # Get legal moves from this square
            self.legal_moves_from_selected = [
                move for move in board.legal_moves
                if move.from_square == chess_square
            ]
            
            # Highlight selected square and legal moves
            highlight_squares = [chess_square]
            for move in self.legal_moves_from_selected:
                highlight_squares.append(move.to_square)
            
            self.view.highlight_squares(highlight_squares)
        else:
            # Clear selection if clicking on empty square or opponent's piece
            self.selected_square = None
            self.legal_moves_from_selected = []
            self.view.highlight_squares([])
    
    def _make_move(self, move):
        """
        Make a move through the model.
        
        Args:
            move (chess.Move): Move to make
        """
        # Get notation before pushing the move
        board = self.model.board
        notation = self._get_move_notation(move, board)
        
        if self.model.push_move(move):
            # Track this as a human move
            self.move_stack.append((move, False))
            
            # Add to move history
            self.move_history.append((move, self.model.get_fen(), notation))
            self.current_position_index = len(self.move_history) - 1
            
            # Update display
            self._update_display()
            
            # Check if game is over
            if self.model.is_game_over():
                self._handle_game_over()
            else:
                # If in AI mode and it's AI's turn, trigger AI move
                if self.game_mode == "ai" and self._should_ai_move():
                    self._make_ai_move()
        else:
            QMessageBox.warning(self.view, "Invalid Move", "The selected move is not legal.")
    
    def _should_ai_move(self):
        """Check if AI should make a move."""
        if not self.ai_engine:
            return False
        
        board = self.model.board
        if board.is_game_over():
            return False
        
        # Check if it's AI's turn
        return board.turn == self.ai_plays_as
    
    def _make_ai_move(self):
        """
        Have the AI make a move.
        Called after human move when it's AI's turn.
        """
        board = self.model.board
        ai_move = self.ai_engine.select_move(board)
        
        if ai_move:
            # Get notation before pushing the move
            notation = self._get_move_notation(ai_move, board)
            
            if self.model.push_move(ai_move):
                # Track this as an AI move
                self.move_stack.append((ai_move, True))
                
                # Add to move history
                self.move_history.append((ai_move, self.model.get_fen(), notation))
                self.current_position_index = len(self.move_history) - 1
                
                self._update_display()
                
                # Check if game is over
                if self.model.is_game_over():
                    self._handle_game_over()
            else:
                QMessageBox.warning(self.view, "AI Error", "AI selected an invalid move.")
        else:
            # No legal moves for AI
            self._handle_game_over()
    
    def _get_move_notation(self, move, board):
        """
        Get algebraic notation for a move.
        
        Args:
            move (chess.Move): The move
            board (chess.Board): Board before the move (to get piece info)
            
        Returns:
            str: Algebraic notation
        """
        # Use python-chess built-in SAN conversion
        try:
            # board.san() requires the board to be in the state before the move
            # So we use the current board state
            san = board.san(move)
            return san
        except:
            # Fallback to UCI
            return move.uci()
    
    def _on_new_game(self):
        """Handle new game request."""
        self.model.new_game()
        self.selected_square = None
        self.legal_moves_from_selected = []
        self.move_stack = []
        self.move_history = []
        self.current_position_index = -1
        self.view.highlight_squares([])
        self._update_display()
    
    def _on_undo(self):
        """
        Handle undo request.
        Undoes both human and AI moves appropriately.
        """
        if not self.move_stack:
            QMessageBox.information(self.view, "Undo", "No moves to undo.")
            return
        
        # Undo moves until we get back to a human move (or start)
        # In Human vs Human: undo one move
        # In Human vs AI: undo both human and AI move
        if self.game_mode == "ai":
            # Undo AI move if it was the last move
            if self.move_stack and self.move_stack[-1][1]:  # Last move was AI
                self.model.undo_move()
                self.move_stack.pop()
            
            # Undo human move
            if self.move_stack and not self.move_stack[-1][1]:  # Last move was human
                self.model.undo_move()
                self.move_stack.pop()
        else:
            # Human vs Human: undo one move
            if self.move_stack:
                self.model.undo_move()
                self.move_stack.pop()
        
        # Clear selection
        self.selected_square = None
        self.legal_moves_from_selected = []
        self.view.highlight_squares([])
        self._update_display()
    
    def _on_mode_toggle(self, mode):
        """
        Handle game mode toggle.
        
        Args:
            mode (str): "human" or "ai"
        """
        self.game_mode = mode
        
        # Initialize AI engine if switching to AI mode
        if mode == "ai" and not self.ai_engine:
            self.ai_engine = AIEngine(depth=self.ai_depth)
        
        # If game is in progress and it's AI's turn, make AI move
        if mode == "ai" and self._should_ai_move():
            self._make_ai_move()
        elif mode == "human":
            # Clear any pending AI state
            pass
        
        self._update_display()
    
    def _on_difficulty_changed(self, depth):
        """
        Handle difficulty change.
        
        Args:
            depth (int): AI search depth (1-4)
        """
        self.ai_depth = depth
        if self.ai_engine:
            self.ai_engine.depth = depth
    
    def _on_piece_folder_loaded(self, folder_path):
        """
        Handle piece folder load.
        
        Args:
            folder_path (str): Path to piece images folder
        """
        # Piece folder is already updated in view
        # Just refresh the board display
        self._update_display()
    
    def _update_display(self):
        """Update the view with current board state."""
        # Update board from FEN
        fen = self.model.get_fen()
        self.view.update_board_from_fen(fen)
        
        # Update undo button state
        has_moves = len(self.move_stack) > 0
        self.view.set_undo_enabled(has_moves)
        
        # Update move history display
        self._update_move_history_display()
    
    def _update_move_history_display(self):
        """Update the move history panel in the view."""
        # Format moves for display
        formatted_moves = []
        move_num = 1
        
        for i in range(0, len(self.move_history), 2):
            white_move_data = self.move_history[i] if i < len(self.move_history) else None
            black_move_data = self.move_history[i + 1] if i + 1 < len(self.move_history) else None
            
            if white_move_data:
                white_notation = white_move_data[2]  # notation
                black_notation = black_move_data[2] if black_move_data else ""
                formatted_moves.append((move_num, white_notation, black_notation, ""))
                move_num += 1
        
        self.view.update_move_history(formatted_moves)
    
    def _on_move_history_clicked(self, index):
        """Handle click on move history item to jump to that position."""
        # Calculate which move was clicked
        # Each move in history represents one position
        if 0 <= index < len(self.move_history):
            # Jump to this position
            target_fen = self.move_history[index][1]  # Get FEN from history
            self.model.load_fen(target_fen)
            self.current_position_index = index
            self._update_display()
            
            # Clear selection
            self.selected_square = None
            self.legal_moves_from_selected = []
            self.view.highlight_squares([])
    
    def _handle_game_over(self):
        """Handle game over state."""
        board = self.model.board
        
        if board.is_checkmate():
            winner = "Black" if board.turn == chess.WHITE else "White"
            message = f"Checkmate! {winner} wins!"
            result_type = "checkmate"
        elif board.is_stalemate():
            message = "Stalemate - Draw"
            result_type = "stalemate"
        elif board.is_insufficient_material():
            message = "Draw - Insufficient Material"
            result_type = "draw"
        else:
            message = "Game Over"
            result_type = "draw"
        
        # Show end-of-game dialog
        choice = self.view.show_end_of_game_dialog(result_type, message)
        
        if choice == "new_game":
            self._on_new_game()
        elif choice == "close":
            # Close application
            self.view.close()
    
    # Save/Load functions
    
    def save_game(self, file_path=None):
        """
        Save current game position to a FEN text file.
        
        Args:
            file_path (str, optional): Path to save file. If None, shows dialog.
            
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        if file_path is None:
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Save Game Position",
                "",
                "FEN Files (*.fen);;Text Files (*.txt);;All Files (*)"
            )
        
        if not file_path:
            return False
        
        try:
            fen = self.model.get_fen()
            with open(file_path, 'w') as f:
                f.write(fen)
                f.write('\n')  # Add newline for readability
            
            QMessageBox.information(
                self.view,
                "Save Game",
                f"Game position saved to:\n{file_path}"
            )
            return True
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Save Error",
                f"Failed to save game:\n{str(e)}"
            )
            return False
    
    def load_game(self, file_path=None):
        """
        Load a game position from a FEN text file.
        
        Args:
            file_path (str, optional): Path to load file. If None, shows dialog.
            
        Returns:
            bool: True if loaded successfully, False otherwise.
        """
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self.view,
                "Load Game Position",
                "",
                "FEN Files (*.fen);;Text Files (*.txt);;All Files (*)"
            )
        
        if not file_path:
            return False
        
        try:
            with open(file_path, 'r') as f:
                fen = f.read().strip()
            
            if self.model.load_fen(fen):
                # Reset move tracking
                self.selected_square = None
                self.legal_moves_from_selected = []
                self.move_stack = []
                self.view.highlight_squares([])
                self._update_display()
                
                QMessageBox.information(
                    self.view,
                    "Load Game",
                    f"Game position loaded from:\n{file_path}"
                )
                return True
            else:
                QMessageBox.warning(
                    self.view,
                    "Load Error",
                    "Invalid FEN string in file."
                )
                return False
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Load Error",
                f"Failed to load game:\n{str(e)}"
            )
            return False
    
    # Settings management
    
    def _load_settings(self):
        """
        Load settings from settings.json.
        
        Returns:
            dict: Settings dictionary, or default settings if file doesn't exist.
        """
        default_settings = {
            "window_width": 800,
            "window_height": 600,
            "board_theme": "classic",
            "sound_enabled": False,
            "auto_save": True,
            "difficulty": "medium"
        }
        
        settings_file = "settings.json"
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(settings)
                    return default_settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return default_settings
        
        return default_settings
    
    def _save_settings(self):
        """Save current settings to settings.json."""
        settings_file = "settings.json"
        
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            QMessageBox.warning(
                self.view,
                "Settings Error",
                f"Failed to save settings: {str(e)}"
            )
    
    def _apply_settings(self):
        """Apply loaded settings to the application."""
        # Set window size
        if "window_width" in self.settings and "window_height" in self.settings:
            self.view.resize(
                self.settings["window_width"],
                self.settings["window_height"]
            )
        
        # Set difficulty
        difficulty_map = {
            "easy": 1,
            "medium": 2,
            "hard": 3,
            "expert": 4
        }
        difficulty_str = self.settings.get("difficulty", "medium").lower()
        self.ai_depth = difficulty_map.get(difficulty_str, 2)
        if self.view.difficulty_combo:
            index = self.ai_depth - 1
            if 0 <= index < self.view.difficulty_combo.count():
                self.view.difficulty_combo.setCurrentIndex(index)
    
    def update_setting(self, key, value):
        """
        Update a setting and save to file.
        
        Args:
            key (str): Setting key
            value: Setting value
        """
        self.settings[key] = value
        self._save_settings()
    
    def get_setting(self, key, default=None):
        """
        Get a setting value.
        
        Args:
            key (str): Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def save_settings(self):
        """Public method to save settings."""
        self._save_settings()
    
    def load_settings(self):
        """Public method to reload settings."""
        self.settings = self._load_settings()
        self._apply_settings()
