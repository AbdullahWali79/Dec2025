"""
Chess Model - Handles game logic and state management.
Uses python-chess library for chess rules and game state.
"""

import chess


class ChessModel:
    """
    Manages the chess game state and logic using python-chess.
    
    Attributes:
        board (chess.Board): The chess board object representing the current game state.
        move_history (list): List of moves made in the current game.
    """
    
    def __init__(self):
        """Initialize a new chess game with starting position."""
        self.board = chess.Board()
        self.move_history = []
    
    def new_game(self):
        """
        Reset the game to the initial starting position.
        
        Clears the board and move history, starting a fresh game.
        """
        self.board.reset()
        self.move_history.clear()
    
    def load_fen(self, fen):
        """
        Load a chess position from a FEN (Forsyth-Edwards Notation) string.
        
        Args:
            fen (str): FEN string representing the chess position.
            
        Returns:
            bool: True if FEN was loaded successfully, False otherwise.
        """
        try:
            self.board = chess.Board(fen)
            self.move_history.clear()  # Clear history when loading new position
            return True
        except ValueError:
            return False
    
    def get_fen(self):
        """
        Get the current board position in FEN notation.
        
        Returns:
            str: FEN string representing the current position.
        """
        return self.board.fen()
    
    def legal_moves(self):
        """
        Get all legal moves for the current position.
        
        Returns:
            list: List of chess.Move objects representing all legal moves.
        """
        return list(self.board.legal_moves)
    
    def push_move(self, move):
        """
        Make a move on the chess board.
        
        Args:
            move: A chess.Move object or UCI string (e.g., "e2e4").
            
        Returns:
            bool: True if move was legal and executed, False otherwise.
        """
        try:
            # Convert string to Move object if needed
            if isinstance(move, str):
                move = chess.Move.from_uci(move)
            
            # Check if move is legal
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move)
                return True
            else:
                return False
        except (chess.InvalidMoveError, chess.IllegalMoveError, ValueError):
            return False
    
    def undo_move(self):
        """
        Undo the last move made.
        
        Returns:
            bool: True if a move was undone, False if no moves to undo.
        """
        if self.board.move_stack:
            self.board.pop()
            if self.move_history:
                self.move_history.pop()
            return True
        return False
    
    def is_checkmate(self):
        """
        Check if the current position is checkmate.
        
        Returns:
            bool: True if the current player is in checkmate, False otherwise.
        """
        return self.board.is_checkmate()
    
    def is_stalemate(self):
        """
        Check if the current position is stalemate.
        
        Returns:
            bool: True if the current position is stalemate, False otherwise.
        """
        return self.board.is_stalemate()
    
    def is_game_over(self):
        """
        Check if the game is over (checkmate, stalemate, or other end conditions).
        
        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.board.is_game_over()
    
    def available_promotions(self, from_square, to_square):
        """
        Get available promotion options for a pawn move.
        
        Args:
            from_square (str or int): Source square (e.g., "e7" or chess.E7).
            to_square (str or int): Destination square (e.g., "e8" or chess.E8).
            
        Returns:
            list: List of chess.Piece objects representing available promotion options.
                  Returns empty list if move is not a promotion or is illegal.
        """
        try:
            # Convert squares to chess.Square objects if needed
            if isinstance(from_square, str):
                from_square = chess.parse_square(from_square)
            if isinstance(to_square, str):
                to_square = chess.parse_square(to_square)
            
            # Create move to check if it's a promotion
            move = chess.Move(from_square, to_square)
            
            # Check if this is a promotion move
            if move in self.board.legal_moves:
                # Check if move promotes by checking if it's in the promotion squares
                if to_square in [chess.A8, chess.B8, chess.C8, chess.D8, 
                                 chess.E8, chess.F8, chess.G8, chess.H8,
                                 chess.A1, chess.B1, chess.C1, chess.D1,
                                 chess.E1, chess.F1, chess.G1, chess.H1]:
                    # Check if it's a pawn moving to promotion square
                    piece = self.board.piece_at(from_square)
                    if piece and piece.piece_type == chess.PAWN:
                        # Return available promotion pieces (Queen, Rook, Bishop, Knight)
                        promotions = []
                        for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
                            promo_move = chess.Move(from_square, to_square, promotion=piece_type)
                            if promo_move in self.board.legal_moves:
                                promotions.append(chess.Piece(piece_type, self.board.turn))
                        return promotions
            
            return []
        except (ValueError, AttributeError):
            return []


if __name__ == "__main__":
    # Minimal example usage
    print("=== Chess Model Example ===\n")
    
    # Create a new game model
    model = ChessModel()
    
    # Start a new game
    model.new_game()
    print("1. New game started")
    print(f"   FEN: {model.get_fen()}\n")
    
    # Make some moves
    print("2. Making moves:")
    moves = ["e2e4", "e7e5", "g1f3", "b8c6"]
    for move_uci in moves:
        success = model.push_move(move_uci)
        if success:
            print(f"   {move_uci}: Success")
        else:
            print(f"   {move_uci}: Failed")
    
    print(f"\n   Current FEN: {model.get_fen()}\n")
    
    # Show move history
    print("3. Move history:")
    for i, move in enumerate(model.move_history, 1):
        print(f"   Move {i}: {move}")
    
    print(f"\n   Total moves: {len(model.move_history)}\n")
    
    # Show legal moves
    print("4. Legal moves for current position:")
    legal = model.legal_moves()
    print(f"   Total legal moves: {len(legal)}")
    print(f"   First 10 moves: {[str(m) for m in legal[:10]]}\n")
    
    # Check game status
    print("5. Game status:")
    print(f"   Is checkmate: {model.is_checkmate()}")
    print(f"   Is stalemate: {model.is_stalemate()}")
    print(f"   Is game over: {model.is_game_over()}\n")
    
    # Test FEN loading
    print("6. Loading position from FEN:")
    test_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    if model.load_fen(test_fen):
        print(f"   Loaded FEN: {test_fen}")
        print(f"   Current FEN: {model.get_fen()}")
        print(f"   Match: {model.get_fen() == test_fen}\n")
