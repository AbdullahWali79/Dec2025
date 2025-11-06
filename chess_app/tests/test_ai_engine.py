"""
Unit tests for AIEngine class.
Tests that AI returns legal moves and handles various positions.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.ai_engine import AIEngine
import chess


class TestAIEngine:
    """Test suite for AIEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.ai = AIEngine(depth=2)
    
    def test_ai_initialization(self):
        """Test AI engine initialization."""
        assert self.ai.depth == 2
        assert self.ai is not None
    
    def test_ai_select_move_starting_position(self):
        """Test that AI returns a legal move from starting position."""
        board = chess.Board()
        move = self.ai.select_move(board)
        
        assert move is not None
        assert isinstance(move, chess.Move)
        assert move in board.legal_moves
    
    def test_ai_select_move_white(self):
        """Test AI playing as white."""
        board = chess.Board()
        move = self.ai.select_move(board)
        
        # Starting position, white to move
        assert board.turn == chess.WHITE
        assert move is not None
        assert move in board.legal_moves
    
    def test_ai_select_move_black(self):
        """Test AI playing as black."""
        board = chess.Board()
        board.push(chess.Move.from_uci("e2e4"))  # White moves
        
        move = self.ai.select_move(board)
        
        # Now black to move
        assert board.turn == chess.BLACK
        assert move is not None
        assert move in board.legal_moves
    
    def test_ai_handles_game_over(self):
        """Test that AI returns None when game is over."""
        # Checkmate position
        board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
        
        move = self.ai.select_move(board)
        
        assert move is None
    
    def test_ai_handles_no_legal_moves(self):
        """Test AI when no legal moves exist."""
        # Stalemate position
        board = chess.Board("8/8/8/8/8/5k2/5p2/5K2 w - - 0 1")
        
        move = self.ai.select_move(board)
        
        # Should return None (no legal moves)
        assert move is None
    
    def test_ai_different_depths(self):
        """Test AI with different search depths."""
        for depth in [1, 2, 3]:
            ai = AIEngine(depth=depth)
            board = chess.Board()
            move = ai.select_move(board)
            
            assert move is not None
            assert move in board.legal_moves
    
    def test_ai_promotion_handling(self):
        """Test that AI can handle promotion moves."""
        # Position with pawn ready to promote
        board = chess.Board("rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")
        
        move = self.ai.select_move(board)
        
        # Should return a move (may or may not be promotion)
        if move:
            assert move in board.legal_moves
    
    def test_ai_evaluation_function(self):
        """Test that AI evaluation function works."""
        board = chess.Board()
        
        # Should be able to evaluate starting position
        # We can't directly test _evaluate, but we can test that select_move works
        move = self.ai.select_move(board)
        assert move is not None
    
    def test_ai_consistency(self):
        """Test that AI makes moves consistently."""
        board1 = chess.Board()
        board2 = chess.Board()
        
        # Both should be identical starting positions
        move1 = self.ai.select_move(board1)
        move2 = self.ai.select_move(board2)
        
        # Both should be legal moves
        assert move1 is not None
        assert move2 is not None
        assert move1 in board1.legal_moves
        assert move2 in board2.legal_moves
    
    def test_ai_nodes_evaluated(self):
        """Test that nodes_evaluated counter works."""
        board = chess.Board()
        
        # Reset counter
        self.ai.nodes_evaluated = 0
        
        move = self.ai.select_move(board)
        
        # Should have evaluated some nodes
        assert self.ai.get_nodes_evaluated() > 0
    
    def test_ai_in_middle_game(self):
        """Test AI in a middle game position."""
        # A typical middle game position
        fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
        board = chess.Board(fen)
        
        move = self.ai.select_move(board)
        
        assert move is not None
        assert move in board.legal_moves
    
    def test_ai_in_endgame(self):
        """Test AI in an endgame position."""
        # Simplified endgame position
        fen = "8/8/8/8/4K3/8/4k3/8 w - - 0 1"
        board = chess.Board(fen)
        
        move = self.ai.select_move(board)
        
        # Should return a move (or None if no legal moves)
        if move is not None:
            assert move in board.legal_moves

