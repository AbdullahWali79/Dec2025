"""
Unit tests for ChessModel class.
Tests legal move generation, castling, en passant, promotion, and checkmate detection.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.chess_model import ChessModel
import chess


class TestChessModel:
    """Test suite for ChessModel."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.model = ChessModel()
    
    def test_new_game(self):
        """Test that new_game() resets to starting position."""
        # Make some moves
        self.model.push_move("e2e4")
        self.model.push_move("e7e5")
        
        # Reset
        self.model.new_game()
        
        # Verify starting position
        assert self.model.get_fen().startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")
        assert len(self.model.move_history) == 0
    
    def test_legal_moves_starting_position(self):
        """Test legal moves generation in starting position."""
        legal_moves = self.model.legal_moves()
        
        # Starting position should have 20 legal moves
        assert len(legal_moves) == 20
        
        # Check that e2e4 is a legal move
        e4_move = chess.Move.from_uci("e2e4")
        assert e4_move in legal_moves
    
    def test_push_move_valid(self):
        """Test pushing a valid move."""
        result = self.model.push_move("e2e4")
        
        assert result is True
        assert len(self.model.move_history) == 1
        assert self.model.get_fen().startswith("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq")
    
    def test_push_move_invalid(self):
        """Test pushing an invalid move."""
        result = self.model.push_move("e2e5")  # Invalid: pawn can't move 3 squares in starting position
        
        assert result is False
        assert len(self.model.move_history) == 0
    
    def test_undo_move(self):
        """Test undoing a move."""
        self.model.push_move("e2e4")
        self.model.push_move("e7e5")
        
        initial_fen = self.model.get_fen()
        self.model.undo_move()
        
        # Should be back to after first move
        assert len(self.model.move_history) == 1
        assert self.model.get_fen() != initial_fen
    
    def test_undo_no_moves(self):
        """Test undoing when no moves exist."""
        result = self.model.undo_move()
        assert result is False
    
    def test_castling_kingside(self):
        """Test kingside castling."""
        # Set up position for castling
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1"
        self.model.load_fen(fen)
        
        # White can castle kingside
        legal_moves = self.model.legal_moves()
        castling_move = chess.Move.from_uci("e1g1")
        
        # Check if castling is in legal moves
        castling_moves = [m for m in legal_moves if m.from_square == chess.E1 and m.to_square == chess.G1]
        assert len(castling_moves) > 0
    
    def test_castling_queenside(self):
        """Test queenside castling."""
        # Set up position for queenside castling
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3KBNR w KQkq - 0 1"
        self.model.load_fen(fen)
        
        # White can castle queenside
        legal_moves = self.model.legal_moves()
        castling_move = chess.Move.from_uci("e1c1")
        
        # Check if castling is in legal moves
        castling_moves = [m for m in legal_moves if m.from_square == chess.E1 and m.to_square == chess.C1]
        assert len(castling_moves) > 0
    
    def test_en_passant(self):
        """Test en passant capture."""
        # Set up position for en passant
        # White pawn on e5, Black pawn on d5 (just moved)
        fen = "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
        self.model.load_fen(fen)
        
        legal_moves = self.model.legal_moves()
        
        # En passant move should be legal
        en_passant_moves = [
            m for m in legal_moves 
            if m.from_square == chess.E5 and m.to_square == chess.D6 and m.ep_square == chess.D6
        ]
        assert len(en_passant_moves) > 0
    
    def test_promotion_available(self):
        """Test promotion detection."""
        # Set up position with pawn on 7th rank
        fen = "rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1"
        self.model.load_fen(fen)
        
        # Check promotions from g7
        promotions = self.model.available_promotions("g7", "g8")
        
        # Should have 4 promotion options
        assert len(promotions) == 4
        assert any(p.piece_type == chess.QUEEN for p in promotions)
        assert any(p.piece_type == chess.ROOK for p in promotions)
        assert any(p.piece_type == chess.BISHOP for p in promotions)
        assert any(p.piece_type == chess.KNIGHT for p in promotions)
    
    def test_promotion_execution(self):
        """Test executing a promotion move."""
        # Set up position with pawn ready to promote
        fen = "rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1"
        self.model.load_fen(fen)
        
        # Promote to queen
        promotion_move = chess.Move(chess.G7, chess.G8, promotion=chess.QUEEN)
        result = self.model.push_move(promotion_move)
        
        assert result is True
        
        # Check that queen is on g8
        board = self.model.get_board()
        piece = board.piece_at(chess.G8)
        assert piece is not None
        assert piece.piece_type == chess.QUEEN
        assert piece.color == chess.WHITE
    
    def test_checkmate_detection(self):
        """Test checkmate detection."""
        # Fool's mate position
        fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        self.model.load_fen(fen)
        
        assert self.model.is_checkmate() is True
        assert self.model.is_game_over() is True
    
    def test_stalemate_detection(self):
        """Test stalemate detection."""
        # Stalemate position
        fen = "8/8/8/8/8/5k2/5p2/5K2 w - - 0 1"
        self.model.load_fen(fen)
        
        assert self.model.is_stalemate() is True
        assert self.model.is_game_over() is True
    
    def test_check_detection(self):
        """Test that check is detected but not checkmate."""
        # Position where white is in check but not checkmate
        fen = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2p/RNBQKBNR w KQkq - 0 1"
        self.model.load_fen(fen)
        
        board = self.model.get_board()
        assert board.is_check() is True
        assert self.model.is_checkmate() is False
        assert self.model.is_game_over() is False
    
    def test_load_fen(self):
        """Test loading position from FEN."""
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        result = self.model.load_fen(fen)
        
        assert result is True
        assert self.model.get_fen() == fen
    
    def test_load_invalid_fen(self):
        """Test loading invalid FEN string."""
        invalid_fen = "invalid fen string"
        result = self.model.load_fen(invalid_fen)
        
        assert result is False
    
    def test_get_fen(self):
        """Test getting FEN string."""
        fen = self.model.get_fen()
        
        # Should be starting position FEN
        assert fen.startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        assert "w KQkq" in fen
    
    def test_move_sequence(self):
        """Test a sequence of moves."""
        moves = ["e2e4", "e7e5", "g1f3", "b8c6"]
        
        for move in moves:
            result = self.model.push_move(move)
            assert result is True
        
        assert len(self.model.move_history) == 4
        assert self.model.is_game_over() is False

