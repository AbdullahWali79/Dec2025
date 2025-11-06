# Quick Verification Checklist

Run these 6 tests to verify the application is complete and functional.

## Test 1: GUI Launch and Board Display ✅

**Command:** `python main.py`

**Verify:**
- [ ] Application window opens without errors
- [ ] Chess board displays (8x8 grid)
- [ ] Starting position pieces visible:
  - [ ] White pieces on ranks 1-2
  - [ ] Black pieces on ranks 7-8
- [ ] Board coordinates visible (A-H, 1-8)
- [ ] Toolbar visible
- [ ] Move history panel visible
- [ ] Status bar shows "White to move"

**Expected:** Window opens, board displays correctly with all pieces

---

## Test 2: Human vs Human Mode ✅

**Steps:**
1. Launch: `python main.py`
2. Verify mode is "Human vs Human"
3. Make white move: Click e2 pawn → Click e4
4. Make black move: Click e7 pawn → Click e5

**Verify:**
- [ ] White move executes (e2-e4)
- [ ] Board updates showing pawn on e4
- [ ] Status bar updates to "Black to move"
- [ ] Black move executes (e7-e5)
- [ ] Board updates showing black pawn on e5
- [ ] Move history shows: "1. e4 e5"
- [ ] Can continue making moves

**Expected:** Both players can make moves, board updates, moves in history

---

## Test 3: Human vs Computer Mode ✅

**Steps:**
1. Launch: `python main.py`
2. Click "Mode" button → "Mode: Human vs AI"
3. Make white move: Click e2 → Click e4
4. Wait for AI move (automatic)

**Verify:**
- [ ] Mode changes to "Human vs AI"
- [ ] White move executes
- [ ] AI automatically makes a move within 5 seconds
- [ ] AI move is legal (black piece moves)
- [ ] Board shows AI's move
- [ ] Status bar shows "White to move"
- [ ] Move history shows both moves
- [ ] Can continue (human → AI cycle)

**Expected:** AI automatically makes legal moves after human moves

---

## Test 4: Promotion Dialog ✅

**Steps:**
1. Launch: `python main.py`
2. Set up promotion position (or play to it)
   - Option: Load FEN: `rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1`
3. Move pawn to promotion square (g7 → g8)
4. Promotion dialog appears
5. Select piece (e.g., Queen)
6. Click OK

**Verify:**
- [ ] Promotion dialog appears
- [ ] Shows 4 options: Queen, Rook, Bishop, Knight
- [ ] Options display with symbols
- [ ] Default is Queen
- [ ] Can select different pieces
- [ ] Selection highlights
- [ ] Promotion executes correctly
- [ ] Board shows promoted piece (e.g., Queen on g8)
- [ ] Move history shows promotion notation

**Expected:** Dialog appears, all options work, promotion executes

---

## Test 5: Undo Functionality ✅

### Test 5A: Undo in Human vs Human
**Steps:**
1. Launch: `python main.py`
2. Make 2-3 moves
3. Click "Undo" button

**Verify:**
- [ ] Undo button enabled after moves
- [ ] Undo reverts last move
- [ ] Board returns to previous position
- [ ] Move history updates
- [ ] Can undo multiple moves

### Test 5B: Undo in Human vs AI
**Steps:**
1. Launch: `python main.py`
2. Toggle to "Human vs AI"
3. Make white move
4. Wait for AI move
5. Click "Undo" (should undo AI move)
6. Click "Undo" again (should undo human move)

**Verify:**
- [ ] Undo removes AI move
- [ ] Undo removes human move
- [ ] Board returns to position before both moves
- [ ] Both moves removed from history

**Expected:** Undo works in both modes, removes correct moves

---

## Test 6: Executable Build and Launch ✅

### Step 6A: Build Executable
**Command:** `build_exe.bat`

**Verify:**
- [ ] Build script runs without errors
- [ ] PyInstaller executes successfully
- [ ] Build completes successfully
- [ ] `dist/ChessApp.exe` is created
- [ ] File size is reasonable (50-150 MB)

### Step 6B: Test Executable
**Command:** `dist\ChessApp.exe`

**Verify:**
- [ ] Executable runs without errors
- [ ] Application window opens
- [ ] Chess board displays correctly
- [ ] All features work (same as development mode)
- [ ] No Python installation required

**Expected:** Build succeeds, executable runs, features work

---

## Quick Verification Script

Run these commands in sequence:

```bash
# 1. Test launch
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

## Success Criteria

All 6 tests must pass:
- ✅ Test 1: GUI Launch and Board Display
- ✅ Test 2: Human vs Human Mode
- ✅ Test 3: Human vs Computer Mode
- ✅ Test 4: Promotion Dialog
- ✅ Test 5: Undo Functionality
- ✅ Test 6: Executable Build and Launch

## Sign-Off

Once all tests pass:
- [ ] Application is ready for distribution
- [ ] Executable can be shared
- [ ] Documentation is complete
- [ ] All features verified working

---

**For detailed verification steps, see:** `VERIFICATION_CHECKLIST.md`

