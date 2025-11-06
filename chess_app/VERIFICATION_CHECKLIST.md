# Verification Checklist - Chess Desktop Application

This checklist verifies that the chess application is complete and functional before distribution.

## Pre-Verification Setup

### 1. Environment Check
- [ ] Python 3.10 or higher is installed
- [ ] All dependencies installed: `pip install PyQt5 python-chess pyinstaller`
- [ ] Working directory is `chess_app/`
- [ ] All required files are present (see `FINAL_PACKAGE.md`)

### 2. File Verification
- [ ] `main.py` exists
- [ ] `model/chess_model.py` exists
- [ ] `model/ai_engine.py` exists
- [ ] `view/chess_view.py` exists
- [ ] `controller/chess_controller.py` exists
- [ ] `utils/asset_downloader.py` exists
- [ ] `assets/icon.ico` exists
- [ ] `settings.json` exists
- [ ] `build_exe.bat` exists

---

## Verification Test 1: GUI Launch and Board Display

**Test:** `python main.py` launches the GUI and board displays starting pieces

### Steps:
1. Open terminal/command prompt
2. Navigate to `chess_app/` directory
3. Run: `python main.py`
4. Verify application launches

### Expected Results:
- [ ] Application window opens without errors
- [ ] No console errors appear
- [ ] Main window displays with chess board
- [ ] Chess board shows 8x8 grid
- [ ] Board coordinates visible (A-H, 1-8)
- [ ] Starting position pieces displayed:
  - [ ] White pieces on rank 1 (pawns) and rank 2 (pieces)
  - [ ] Black pieces on rank 7 (pawns) and rank 8 (pieces)
- [ ] Toolbar visible with buttons
- [ ] Move history panel visible on side
- [ ] Status bar shows "White to move"

### Pass Criteria:
✅ Window opens, board displays correctly, all pieces visible in starting position

### If Failed:
- Check Python version: `python --version`
- Verify dependencies: `pip list | grep -i pyqt5`
- Check for import errors in console
- Verify `assets/icon.ico` exists (or remove icon requirement)

---

## Verification Test 2: Human vs Human Mode Moves

**Test:** Human vs Human mode moves work for both colors

### Steps:
1. Launch application: `python main.py`
2. Verify mode is "Human vs Human" (or toggle if needed)
3. Make white move: Click white pawn (e2), click destination (e4)
4. Make black move: Click black pawn (e7), click destination (e5)

### Expected Results:
- [ ] White move executes successfully (e2-e4)
- [ ] Board updates showing pawn on e4
- [ ] Status bar updates to "Black to move"
- [ ] Legal moves highlight when piece selected
- [ ] Black move executes successfully (e7-e5)
- [ ] Board updates showing black pawn on e5
- [ ] Status bar updates to "White to move"
- [ ] Move history panel shows moves: "1. e4 e5"
- [ ] Can make additional moves for both colors

### Additional Tests:
- [ ] Invalid moves are rejected
- [ ] Clicking opponent's piece selects it (if current player's turn)
- [ ] Clicking empty square clears selection
- [ ] Multiple moves can be made in sequence

### Pass Criteria:
✅ Both white and black can make moves, board updates correctly, moves appear in history

### If Failed:
- Check controller move handling
- Verify model move validation
- Check view update methods
- Review console for error messages

---

## Verification Test 3: Human vs Computer Mode

**Test:** After human white move, AI plays a legal black move

### Steps:
1. Launch application: `python main.py`
2. Toggle mode to "Human vs AI" (click Mode button)
3. Verify mode shows "Mode: Human vs AI"
4. Make white move: Click e2 pawn, click e4
5. Wait for AI move (should happen automatically)

### Expected Results:
- [ ] Mode toggles to "Human vs AI"
- [ ] White move executes (e2-e4)
- [ ] AI automatically makes a move within 5 seconds
- [ ] AI move is legal (black piece moves)
- [ ] Board updates showing AI's move
- [ ] Status bar shows "White to move" after AI move
- [ ] Move history shows both moves: "1. e4 <AI_MOVE>"
- [ ] AI move is visible on board
- [ ] Can continue making moves (human -> AI -> human cycle)

### Additional Tests:
- [ ] AI responds to different human moves
- [ ] AI move quality is reasonable (not obvious blunders)
- [ ] AI difficulty affects move quality (test different levels)
- [ ] AI doesn't make invalid moves

### Pass Criteria:
✅ AI automatically makes legal moves after human moves, game continues in alternating turns

### If Failed:
- Check AI engine initialization
- Verify AI engine depth setting
- Check controller AI move triggering
- Review AI engine code for errors
- Check console for AI-related errors

---

## Verification Test 4: Promotion Dialog

**Test:** Promotion dialog appears and works

### Steps:
1. Launch application: `python main.py`
2. Load a position with pawn ready to promote:
   - Use "Load Game" or manually set up position
   - Or play to position where pawn can promote
3. Move pawn to promotion square (e.g., e7 to e8 for white)
4. Promotion dialog should appear
5. Select a promotion piece (Queen, Rook, Bishop, or Knight)
6. Click OK or select piece button

### Expected Results:
- [ ] Promotion dialog appears when pawn reaches last rank
- [ ] Dialog shows 4 options: Queen, Rook, Bishop, Knight
- [ ] Options display with Unicode symbols
- [ ] Default selection is Queen
- [ ] Can click different pieces to select
- [ ] Selected piece is highlighted
- [ ] Clicking OK/selecting piece executes promotion
- [ ] Board updates showing promoted piece (e.g., Queen on e8)
- [ ] Move history shows promotion notation (e.g., "e8=Q")

### Alternative Test (if hard to reach promotion):
Create a test FEN with pawn on 7th rank:
```python
# In Python console or test script:
from model.chess_model import ChessModel
model = ChessModel()
model.load_fen("rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")
# Then in GUI, pawn on g7 can promote
```

### Pass Criteria:
✅ Promotion dialog appears, all 4 options work, promotion executes correctly

### If Failed:
- Check promotion detection in controller
- Verify dialog class implementation
- Check move execution with promotion
- Review console for errors

---

## Verification Test 5: Undo Functionality

**Test:** Undo works (including undo AI move)

### Test 5A: Undo in Human vs Human Mode

#### Steps:
1. Launch application: `python main.py`
2. Make several moves (e.g., e4, e5, Nf3, Nc6)
3. Click "Undo" button

#### Expected Results:
- [ ] Undo button becomes enabled after first move
- [ ] Clicking Undo reverts last move
- [ ] Board returns to previous position
- [ ] Move history updates (removes last move)
- [ ] Can undo multiple moves sequentially
- [ ] Undo button disables when no moves to undo

### Test 5B: Undo in Human vs AI Mode

#### Steps:
1. Launch application: `python main.py`
2. Toggle to "Human vs AI" mode
3. Make white move (e.g., e4)
4. Wait for AI to move
5. Click "Undo" button

#### Expected Results:
- [ ] Undo button is enabled after moves
- [ ] Clicking Undo removes AI's move
- [ ] Clicking Undo again removes human's move
- [ ] Board returns to position before both moves
- [ ] Both moves removed from history
- [ ] Can continue playing after undo

### Additional Tests:
- [ ] Undo works at any point in game
- [ ] Undo doesn't break game state
- [ ] Can make new moves after undo
- [ ] Undo doesn't cause errors or crashes

### Pass Criteria:
✅ Undo works in both modes, removes correct moves, maintains game state integrity

### If Failed:
- Check undo logic in controller
- Verify move stack tracking
- Check model undo_move() method
- Review move history management

---

## Verification Test 6: Executable Build and Launch

**Test:** `build_exe.bat` runs and produces `dist/ChessApp.exe` that opens the app on Windows

### Step 1: Build Executable

#### Steps:
1. Open terminal in `chess_app/` directory
2. Run: `build_exe.bat`
3. Wait for build to complete

#### Expected Results:
- [ ] Build script runs without errors
- [ ] PyInstaller executes successfully
- [ ] No critical errors in build output
- [ ] Build completes with "Build completed successfully" message
- [ ] `dist/ChessApp.exe` file is created
- [ ] File size is reasonable (50-150 MB typical)

### Step 2: Test Executable

#### Steps:
1. Navigate to `dist/` folder
2. Double-click `ChessApp.exe` (or run from command line)
3. Verify application launches

#### Expected Results:
- [ ] Executable runs without errors
- [ ] Application window opens
- [ ] No console window appears (if using --windowed)
- [ ] Chess board displays correctly
- [ ] All features work (same as development mode)
- [ ] Assets are accessible (pieces, settings)
- [ ] Application doesn't require Python installation

### Step 3: Feature Verification in Executable

#### Steps:
1. Test making moves
2. Test AI mode
3. Test promotion
4. Test undo
5. Test save/load

#### Expected Results:
- [ ] All features work identically to development mode
- [ ] No file path errors
- [ ] Assets load correctly
- [ ] Settings save/load work
- [ ] No console errors

### Pass Criteria:
✅ Build succeeds, executable runs, all features work, no Python required

### If Failed:

#### Build Issues:
- Check PyInstaller installation: `pip show pyinstaller`
- Verify `--add-data` syntax (semicolon on Windows)
- Check for missing hidden imports
- Review build script for errors

#### Runtime Issues:
- Remove `--windowed` to see error messages
- Check if assets are included
- Verify file paths in code use `sys._MEIPASS`
- Check for missing dependencies

---

## Comprehensive Feature Verification

After passing all 6 main tests, verify:

### Basic Features
- [ ] New Game button works
- [ ] Mode toggle works
- [ ] Difficulty dropdown works
- [ ] Load piece folder works
- [ ] Save game works
- [ ] Load game works

### Game Features
- [ ] Checkmate detection works
- [ ] Stalemate detection works
- [ ] End-of-game dialog appears
- [ ] End-of-game "New Game" works
- [ ] End-of-game "Close" works

### UI Features
- [ ] Move history panel displays moves
- [ ] Clicking move history navigates to position
- [ ] Square highlighting works
- [ ] Status bar updates correctly
- [ ] Window resize works
- [ ] Piece images display (or Unicode fallback)

### Advanced Features
- [ ] Castling works (if applicable)
- [ ] En passant works (if applicable)
- [ ] Settings persist between sessions
- [ ] Asset download works (if internet available)

---

## Final Verification Summary

### Quick Test Script

Run these commands in sequence:

```bash
# 1. Test GUI launch
python main.py
# (Manually verify: window opens, board displays)

# 2. Test Human vs Human
# (Make moves for both colors)

# 3. Test Human vs AI
# (Make move, verify AI responds)

# 4. Test Promotion
# (Move pawn to promotion square)

# 5. Test Undo
# (Make moves, click undo)

# 6. Test Build
build_exe.bat
dist\ChessApp.exe
# (Verify executable runs)
```

### Success Criteria

All 6 verification tests must pass:
- ✅ Test 1: GUI Launch and Board Display
- ✅ Test 2: Human vs Human Mode
- ✅ Test 3: Human vs Computer Mode
- ✅ Test 4: Promotion Dialog
- ✅ Test 5: Undo Functionality
- ✅ Test 6: Executable Build and Launch

### Sign-Off

Once all tests pass:
- [ ] Application is ready for distribution
- [ ] Executable can be shared
- [ ] Documentation is complete
- [ ] All features verified working

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Import errors | Check dependencies: `pip install PyQt5 python-chess` |
| GUI doesn't open | Check Python version (3.10+), verify PyQt5 installed |
| AI doesn't move | Check AI mode is enabled, verify AI engine initialized |
| Promotion not working | Check pawn is on 7th/2nd rank, verify dialog code |
| Undo doesn't work | Check move stack tracking, verify undo logic |
| Build fails | Check PyInstaller installed, verify `--add-data` syntax |
| Executable doesn't run | Remove `--windowed` to see errors, check assets included |

---

**Last Updated:** After Step 10 completion
**Verification Status:** Ready for testing

