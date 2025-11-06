# Chess Application - Test Checklist

## Overview
This document provides a comprehensive test checklist for the Chess Desktop Application. Use this checklist to ensure all features are properly tested before release.

---

## 1. Model Tests (chess_model.py)

### 1.1 Basic Functionality
- [ ] `new_game()` resets to starting position
- [ ] `new_game()` clears move history
- [ ] `get_fen()` returns correct FEN string
- [ ] `load_fen()` loads valid FEN positions
- [ ] `load_fen()` rejects invalid FEN strings
- [ ] `legal_moves()` returns correct number of moves in starting position (20 moves)
- [ ] `push_move()` accepts valid moves
- [ ] `push_move()` rejects invalid moves
- [ ] `undo_move()` correctly reverts moves
- [ ] `undo_move()` returns False when no moves to undo

### 1.2 Special Moves - Castling
- [ ] Kingside castling is detected as legal when conditions are met
- [ ] Queenside castling is detected as legal when conditions are met
- [ ] Castling is blocked when king has moved
- [ ] Castling is blocked when rook has moved
- [ ] Castling is blocked when squares are attacked
- [ ] Castling is blocked when squares are occupied

### 1.3 Special Moves - En Passant
- [ ] En passant capture is available after pawn double-move
- [ ] En passant move is correctly identified in legal moves
- [ ] En passant can be executed
- [ ] En passant is only available immediately after double-move

### 1.4 Special Moves - Promotion
- [ ] `available_promotions()` returns 4 options (Queen, Rook, Bishop, Knight)
- [ ] Promotion to Queen works correctly
- [ ] Promotion to Rook works correctly
- [ ] Promotion to Bishop works correctly
- [ ] Promotion to Knight works correctly
- [ ] Promotion only available on 8th/1st rank

### 1.5 Game End Conditions
- [ ] `is_checkmate()` correctly detects checkmate
- [ ] `is_stalemate()` correctly detects stalemate
- [ ] `is_game_over()` returns True for checkmate
- [ ] `is_game_over()` returns True for stalemate
- [ ] `is_game_over()` returns True for draw by insufficient material
- [ ] `is_game_over()` returns False for normal positions

### 1.6 Move History
- [ ] Move history tracks all moves correctly
- [ ] Move history is cleared on `new_game()`
- [ ] Move history is cleared on `load_fen()`

---

## 2. AI Engine Tests (ai_engine.py)

### 2.1 Basic Functionality
- [ ] AI engine initializes with correct depth
- [ ] `select_move()` returns a legal move from starting position
- [ ] `select_move()` returns None when game is over
- [ ] `select_move()` returns None when no legal moves exist
- [ ] AI returns legal moves for white
- [ ] AI returns legal moves for black

### 2.2 Search Depth
- [ ] AI works with depth=1
- [ ] AI works with depth=2
- [ ] AI works with depth=3
- [ ] AI works with depth=4
- [ ] Higher depth evaluates more nodes

### 2.3 Edge Cases
- [ ] AI handles promotion positions
- [ ] AI handles checkmate positions (returns None)
- [ ] AI handles stalemate positions (returns None)
- [ ] AI handles middle game positions
- [ ] AI handles endgame positions
- [ ] AI handles positions with only one legal move

### 2.4 Evaluation
- [ ] AI prefers material advantage
- [ ] AI considers positional factors
- [ ] AI avoids obvious blunders (hanging pieces)
- [ ] Nodes evaluated counter works correctly

---

## 3. View Tests (chess_view.py)

### 3.1 Board Rendering
- [ ] Board renders starting position correctly
- [ ] Board renders position after moves correctly
- [ ] Board renders promotion positions correctly
- [ ] Board renders castling positions correctly
- [ ] Board renders en passant positions correctly
- [ ] Board renders checkmate positions correctly
- [ ] Board renders stalemate positions correctly

### 3.2 Piece Display
- [ ] White pieces display correctly
- [ ] Black pieces display correctly
- [ ] Pieces fall back to Unicode when images missing
- [ ] Pieces scale correctly when window resized
- [ ] Custom piece images load correctly

### 3.3 Square Highlighting
- [ ] Selected square highlights correctly
- [ ] Legal moves highlight correctly
- [ ] Highlights clear when selection changes
- [ ] Multiple squares can be highlighted

### 3.4 Dialogs
- [ ] Promotion dialog shows all 4 options
- [ ] Promotion dialog default is Queen
- [ ] Promotion dialog returns selected piece
- [ ] End-of-game dialog shows correct message for checkmate
- [ ] End-of-game dialog shows correct message for stalemate
- [ ] End-of-game dialog shows correct message for draw
- [ ] End-of-game dialog "New Game" button works
- [ ] End-of-game dialog "Close" button works

### 3.5 Move History Panel
- [ ] Move history displays moves correctly
- [ ] Move history shows algebraic notation
- [ ] Move history format: "1. e4 e5"
- [ ] Clicking move history item navigates to position
- [ ] Move history updates after each move
- [ ] Move history clears on new game

### 3.6 UI Components
- [ ] Toolbar buttons work correctly
- [ ] New Game button resets game
- [ ] Undo button works correctly
- [ ] Mode toggle works correctly
- [ ] Difficulty dropdown works correctly
- [ ] Load piece folder dialog works
- [ ] Status bar updates correctly

---

## 4. Controller Tests (chess_controller.py)

### 4.1 Move Handling
- [ ] Two-click move selection works
- [ ] Invalid moves are rejected
- [ ] Legal moves are executed
- [ ] Move updates board correctly
- [ ] Move updates move history

### 4.2 Promotion
- [ ] Promotion dialog appears when promotion needed
- [ ] User can select promotion piece
- [ ] Promotion move executes correctly
- [ ] Cancelling promotion doesn't make move

### 4.3 AI Integration
- [ ] AI moves automatically after human move (in AI mode)
- [ ] AI mode toggle works correctly
- [ ] Difficulty setting affects AI depth
- [ ] AI moves are tracked correctly
- [ ] Undo works correctly with AI moves

### 4.4 Game Flow
- [ ] New game resets everything
- [ ] Undo works in Human vs Human mode
- [ ] Undo works in Human vs AI mode (undoes both moves)
- [ ] End-of-game dialog appears at game end
- [ ] New Game from dialog works
- [ ] Close from dialog works

### 4.5 Save/Load
- [ ] Save game creates FEN file
- [ ] Load game loads FEN file correctly
- [ ] Invalid FEN files are rejected
- [ ] Save/load preserves game state

### 4.6 Settings
- [ ] Settings load on startup
- [ ] Settings save correctly
- [ ] Window size persists
- [ ] Difficulty setting persists

---

## 5. Integration Tests

### 5.1 Full Game Flow
- [ ] Complete game from start to checkmate works
- [ ] Complete game with promotion works
- [ ] Complete game with castling works
- [ ] Complete game with en passant works
- [ ] Game can be saved and loaded mid-game

### 5.2 AI Gameplay
- [ ] Complete game vs AI works
- [ ] AI makes reasonable moves
- [ ] AI responds to human moves
- [ ] Difficulty levels show different AI strength

### 5.3 Move History Navigation
- [ ] Can navigate through move history
- [ ] Board updates when navigating
- [ ] Can return to latest position
- [ ] Navigation preserves game state

---

## 6. Performance Tests

### 6.1 AI Performance
- [ ] AI responds within reasonable time (< 5 seconds for depth 2)
- [ ] AI doesn't freeze UI
- [ ] Higher depth doesn't cause excessive delays

### 6.2 UI Responsiveness
- [ ] Board updates smoothly
- [ ] Window resize is responsive
- [ ] Move history updates quickly
- [ ] Piece images load efficiently

---

## 7. Error Handling

### 7.1 Invalid Input
- [ ] Invalid moves are handled gracefully
- [ ] Invalid FEN strings show error message
- [ ] Missing piece images don't crash app
- [ ] Network errors (asset download) are handled

### 7.2 Edge Cases
- [ ] Game works with no piece images (Unicode fallback)
- [ ] Game works when assets folder missing
- [ ] Game handles rapid clicking
- [ ] Game handles undo at game start

---

## 8. Cross-Platform Tests

### 8.1 Windows
- [ ] Application runs on Windows
- [ ] File dialogs work correctly
- [ ] Path handling works correctly

### 8.2 Linux (if applicable)
- [ ] Application runs on Linux
- [ ] File dialogs work correctly
- [ ] Path handling works correctly

---

## 9. User Experience

### 9.1 Visual
- [ ] Board is visually appealing
- [ ] Pieces are clearly visible
- [ ] Colors have good contrast
- [ ] Coordinates are readable

### 9.2 Usability
- [ ] Move selection is intuitive
- [ ] Promotion dialog is clear
- [ ] End-of-game dialog is informative
- [ ] Move history is easy to use

---

## Running Tests

### Prerequisites
```bash
pip install pytest pytest-qt
```

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_chess_model.py
pytest tests/test_ai_engine.py
pytest tests/test_chess_view.py
```

### Run Specific Test
```bash
pytest tests/test_chess_model.py::TestChessModel::test_legal_moves_starting_position
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pip install pytest-cov
pytest tests/ --cov=model --cov=view --cov=controller
```

---

## Test Results Summary

After running all tests, verify:
- [ ] All model tests pass
- [ ] All AI engine tests pass
- [ ] All view tests pass
- [ ] No critical warnings
- [ ] Code coverage > 80%

---

## Notes

- Tests should be run before each release
- Any failing tests should be fixed before deployment
- New features should include corresponding tests
- Update this checklist when adding new features

