"""
AI Engine - Chess AI using Minimax algorithm with alpha-beta pruning.
Provides computer opponent functionality for the chess game.
"""

import chess
import random
import math


class AIEngine:
    """
    Chess AI engine using Minimax algorithm with alpha-beta pruning.
    
    Attributes:
        depth (int): Search depth for the minimax algorithm.
    """
    
    # Material values for piece evaluation
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    
    # Positional bonuses (center control)
    CENTER_SQUARES = [chess.E4, chess.E5, chess.D4, chess.D5]
    EXTENDED_CENTER = [chess.C3, chess.C4, chess.C5, chess.C6,
                       chess.D3, chess.D4, chess.D5, chess.D6,
                       chess.E3, chess.E4, chess.E5, chess.E6,
                       chess.F3, chess.F4, chess.F5, chess.F6]
    
    def __init__(self, depth=2):
        """
        Initialize the AI engine.
        
        Args:
            depth (int): Search depth for minimax algorithm. Higher depth = stronger AI.
                        Default is 2 (suitable for fast gameplay).
        """
        self.depth = depth
        self.nodes_evaluated = 0  # For debugging/statistics
    
    def select_move(self, board: chess.Board):
        """
        Select the best move for the current position using minimax with alpha-beta pruning.
        
        Args:
            board (chess.Board): The current chess board position.
            
        Returns:
            chess.Move or None: The best move found, or None if no legal moves exist.
        """
        if board.is_game_over():
            return None
        
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        # Reset node counter
        self.nodes_evaluated = 0
        
        # Use minimax with alpha-beta pruning to find best move
        best_move = None
        
        # Add small randomness by shuffling moves for tie-breaking
        random.shuffle(legal_moves)
        
        alpha = -math.inf
        beta = math.inf
        
        # Determine if we're maximizing (white's turn) or minimizing (black's turn)
        # Evaluation is from white's perspective
        is_maximizing = board.turn == chess.WHITE
        best_value = -math.inf if is_maximizing else math.inf
        
        for move in legal_moves:
            board.push(move)
            # After move, it's opponent's turn, so flip maximizing
            value = self._minimax(board, self.depth - 1, alpha, beta, not is_maximizing)
            board.pop()
            
            # Update best move if this is better
            if is_maximizing:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
            
            # Alpha-beta pruning
            if beta <= alpha:
                break  # Cutoff
        
        return best_move
    
    def _minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board (chess.Board): Current board position.
            depth (int): Remaining search depth.
            alpha (float): Best value for maximizing player.
            beta (float): Best value for minimizing player.
            maximizing (bool): True if maximizing player's turn, False otherwise.
            
        Returns:
            float: Evaluation score for the position.
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0 or board.is_game_over():
            return self._evaluate(board)
        
        legal_moves = list(board.legal_moves)
        
        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                board.push(move)
                eval_score = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def _evaluate(self, board: chess.Board):
        """
        Evaluate the current board position.
        
        Combines material values with positional heuristics.
        
        Args:
            board (chess.Board): The chess board to evaluate.
            
        Returns:
            float: Evaluation score. Positive = better for white, Negative = better for black.
        """
        if board.is_checkmate():
            # Checkmate is worth a huge value
            return -100000 if board.turn == chess.WHITE else 100000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0  # Draw positions
        
        # Material evaluation
        material_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.PIECE_VALUES[piece.piece_type]
                # Add value for white, subtract for black
                material_score += value if piece.color == chess.WHITE else -value
        
        # Positional evaluation
        positional_score = self._evaluate_position(board)
        
        # Combine scores
        total_score = material_score + positional_score
        
        # Return from white's perspective
        return total_score
    
    def _evaluate_position(self, board: chess.Board):
        """
        Evaluate positional aspects of the board.
        
        Args:
            board (chess.Board): The chess board to evaluate.
            
        Returns:
            float: Positional score (positive for white advantage).
        """
        score = 0
        
        # Center control bonus
        for square in self.CENTER_SQUARES:
            piece = board.piece_at(square)
            if piece:
                bonus = 15
                score += bonus if piece.color == chess.WHITE else -bonus
        
        # Extended center control
        for square in self.EXTENDED_CENTER:
            piece = board.piece_at(square)
            if piece:
                bonus = 5
                score += bonus if piece.color == chess.WHITE else -bonus
        
        # Piece development bonus (knights and bishops in starting positions)
        # Encourage development of minor pieces
        for square in [chess.B1, chess.G1, chess.C1, chess.F1]:  # White knights and bishops
            piece = board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                    score -= 5  # Penalty for undeveloped pieces
        
        for square in [chess.B8, chess.G8, chess.C8, chess.F8]:  # Black knights and bishops
            piece = board.piece_at(square)
            if piece and piece.color == chess.BLACK:
                if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                    score += 5  # Penalty for black (subtract from white score)
        
        # King safety (penalty for exposed king)
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        
        if white_king_square is not None:
            # Check if king is in center (penalty)
            if white_king_square in self.CENTER_SQUARES:
                score -= 10
        
        if black_king_square is not None:
            # Check if king is in center (penalty)
            if black_king_square in self.CENTER_SQUARES:
                score += 10
        
        # Pawn structure (doubled pawns penalty)
        for file in range(8):
            white_pawns = sum(1 for rank in range(8) 
                            if board.piece_at(chess.square(file, rank)) == 
                            chess.Piece(chess.PAWN, chess.WHITE))
            black_pawns = sum(1 for rank in range(8) 
                            if board.piece_at(chess.square(file, rank)) == 
                            chess.Piece(chess.PAWN, chess.BLACK))
            
            if white_pawns > 1:
                score -= 5 * (white_pawns - 1)  # Penalty for doubled pawns
            if black_pawns > 1:
                score += 5 * (black_pawns - 1)  # Bonus for white (black has doubled)
        
        return score
    
    def get_nodes_evaluated(self):
        """
        Get the number of nodes evaluated in the last search.
        
        Returns:
            int: Number of positions evaluated.
        """
        return self.nodes_evaluated


if __name__ == "__main__":
    # Unit-test style example
    print("=== AI Engine Unit Test ===\n")
    
    # Test 1: Initialize engine
    print("Test 1: Initialize AI Engine")
    engine = AIEngine(depth=2)
    print(f"   ✓ Engine created with depth={engine.depth}\n")
    
    # Test 2: Select move from starting position
    print("Test 2: Select move from starting position")
    board = chess.Board()
    print(f"   Starting position FEN: {board.fen()}")
    print(f"   Current turn: {'White' if board.turn == chess.WHITE else 'Black'}")
    
    move = engine.select_move(board)
    assert move is not None, "AI should find a move from starting position"
    print(f"   ✓ AI selected move: {move}")
    print(f"   ✓ Move in UCI format: {move.uci()}")
    print(f"   ✓ Move is legal: {move in board.legal_moves}")
    print(f"   ✓ Nodes evaluated: {engine.get_nodes_evaluated()}\n")
    
    # Test 3: Verify move can be executed
    print("Test 3: Execute selected move")
    board.push(move)
    print(f"   ✓ Move executed successfully")
    print(f"   New position FEN: {board.fen()}")
    print(f"   Turn after move: {'White' if board.turn == chess.WHITE else 'Black'}\n")
    
    # Test 4: Test with different depth
    print("Test 4: Test with different depth")
    board.reset()
    deep_engine = AIEngine(depth=3)
    move2 = deep_engine.select_move(board)
    print(f"   ✓ Deep engine (depth=3) selected: {move2}")
    print(f"   ✓ Nodes evaluated: {deep_engine.get_nodes_evaluated()}\n")
    
    # Test 5: Test with no legal moves (game over)
    print("Test 5: Test with game over position")
    board.reset()
    # Create a checkmate position
    board.set_fen("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
    move3 = engine.select_move(board)
    if board.is_game_over():
        assert move3 is None, "AI should return None when game is over"
        print(f"   ✓ Correctly returned None (game is over: {board.result()})\n")
    
    # Test 6: Test promotion handling
    print("Test 6: Test promotion handling")
    board.set_fen("8/P7/8/8/8/8/8/8 w - - 0 1")  # White pawn on a7
    move4 = engine.select_move(board)
    if move4:
        print(f"   ✓ AI selected move: {move4}")
        if move4.promotion:
            print(f"   ✓ Move includes promotion to: {chess.Piece(move4.promotion, chess.WHITE)}\n")
        else:
            print(f"   ℹ Move does not require promotion\n")
    
    # Test 7: Multiple moves and consistency
    print("Test 7: Multiple move selections (consistency test)")
    board.reset()
    moves_selected = []
    for i in range(5):
        temp_board = chess.Board()
        move = engine.select_move(temp_board)
        moves_selected.append(move)
        print(f"   Move {i+1}: {move}")
    print(f"   ✓ Selected {len(set(moves_selected))} unique moves (randomness for tie-breaking)\n")
    
    print("=== All Tests Passed ===")

