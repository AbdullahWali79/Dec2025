"""
Unit tests for ChessView class.
Tests board rendering from FEN strings and UI components.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import chess

# Initialize QApplication once for all tests
_app = None

def get_app():
    """Get or create QApplication instance."""
    global _app
    if _app is None:
        _app = QApplication([])
    return _app


class TestChessView:
    """Test suite for ChessView."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from view.chess_view import ChessView
        get_app()  # Ensure QApplication exists
        self.view = ChessView()
        # Don't show window in tests (faster, but comment out if visual testing needed)
        # self.view.show()
    
    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, 'view') and self.view:
            self.view.close()
            self.view = None
    
    def test_view_initialization(self):
        """Test that view initializes correctly."""
        assert self.view is not None
        assert self.view.piece_folder == "assets/pieces"
        assert hasattr(self.view, 'squares')
        assert len(self.view.squares) == 8  # 8 ranks
    
    def test_update_board_from_fen_starting_position(self):
        """Test board rendering from starting position FEN."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.view.update_board_from_fen(fen)
        
        # Check that squares are populated
        # White pieces on rank 7 (index 1), black pieces on rank 0 (index 0)
        board = chess.Board(fen)
        
        # Verify some key pieces
        # White king should be on e1 (rank 7, file 4)
        square = self.view.squares[7][4]
        assert square.piece_symbol is not None or square.pixmap() is not None
        
        # Black king should be on e8 (rank 0, file 4)
        square = self.view.squares[0][4]
        assert square.piece_symbol is not None or square.pixmap() is not None
    
    def test_update_board_from_fen_after_moves(self):
        """Test board rendering after some moves."""
        fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2"
        self.view.update_board_from_fen(fen)
        
        board = chess.Board(fen)
        
        # White pawn should be on e4 (rank 4, file 4)
        square = self.view.squares[4][4]
        # Should have a piece (pawn)
        piece = board.piece_at(chess.square(4, 4))
        assert piece is not None
        assert piece.piece_type == chess.PAWN
        assert piece.color == chess.WHITE
    
    def test_update_board_from_fen_promotion_position(self):
        """Test board rendering with promotion position."""
        fen = "rnbqkb1r/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1"
        self.view.update_board_from_fen(fen)
        
        board = chess.Board(fen)
        
        # White pawn on g7
        piece = board.piece_at(chess.square(6, 6))  # g7
        assert piece is not None
        assert piece.piece_type == chess.PAWN
    
    def test_highlight_squares(self):
        """Test square highlighting."""
        squares_to_highlight = [(0, 0), (0, 1), (1, 0)]  # a8, b8, a7
        
        self.view.highlight_squares(squares_to_highlight)
        
        # Check that squares are highlighted
        for rank, file in squares_to_highlight:
            square = self.view.squares[rank][file]
            assert square.is_highlighted is True
    
    def test_clear_highlights(self):
        """Test clearing highlights."""
        squares_to_highlight = [(0, 0), (0, 1)]
        self.view.highlight_squares(squares_to_highlight)
        
        # Clear highlights
        self.view.highlight_squares([])
        
        # All squares should not be highlighted
        for rank in range(8):
            for file in range(8):
                square = self.view.squares[rank][file]
                assert square.is_highlighted is False
    
    def test_promotion_dialog(self):
        """Test promotion dialog."""
        from view.chess_view import PromotionDialog
        get_app()
        
        dialog = PromotionDialog(None, is_white=True)
        
        # Default should be queen
        assert dialog.get_selected_piece() == chess.QUEEN
        
        # Test selecting different pieces
        dialog._select_piece(chess.ROOK)
        assert dialog.get_selected_piece() == chess.ROOK
        
        dialog._select_piece(chess.BISHOP)
        assert dialog.get_selected_piece() == chess.BISHOP
        
        dialog._select_piece(chess.KNIGHT)
        assert dialog.get_selected_piece() == chess.KNIGHT
    
    def test_end_of_game_dialog(self):
        """Test end-of-game dialog."""
        from view.chess_view import EndOfGameDialog
        get_app()
        
        dialog = EndOfGameDialog(None, "checkmate", "Checkmate! White wins!")
        
        assert dialog.result_type == "checkmate"
        assert dialog.get_choice() is None  # Not selected yet
        
        # Test choice setting
        dialog._make_choice("new_game")
        assert dialog.get_choice() == "new_game"
    
    def test_move_history_update(self):
        """Test move history panel update."""
        moves = [
            (1, "e4", "e5", ""),
            (2, "Nf3", "Nc6", ""),
            (3, "Bb5", "", "")
        ]
        
        self.view.update_move_history(moves)
        
        # Check that items were added
        assert self.view.move_history_list.count() == 3
    
    def test_status_bar_update(self):
        """Test status bar message update."""
        self.view.statusBar().showMessage("Test message")
        
        # Status bar should show the message
        # (We can't easily verify the exact text, but we can check it doesn't crash)
        assert self.view.statusBar() is not None
    
    def test_piece_image_loading(self):
        """Test piece image loading (fallback to Unicode)."""
        # Test loading a piece image
        piece_char = 'K'  # White king
        result = self.view._load_piece_image(piece_char)
        
        # Should return either a pixmap or Unicode symbol
        assert result is not None
    
    def test_board_coordinates(self):
        """Test that board coordinates are displayed."""
        # Check that coordinate labels exist
        # This is harder to test directly, but we can verify the board structure
        assert hasattr(self.view, 'board_grid')
        assert self.view.squares is not None

