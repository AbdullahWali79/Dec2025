# Quick Start Guide - Chess Desktop Application

Get the chess application running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install PyQt5 python-chess
```

## Step 2: Run the Application

```bash
python main.py
```

## Step 3: Play Chess!

### Basic Controls

- **Select Piece**: Click on a piece
- **Make Move**: Click on destination square
- **Undo**: Click "Undo" button
- **New Game**: Click "New Game" button
- **Toggle Mode**: Click "Mode" button (Human vs Human / Human vs AI)
- **Change Difficulty**: Use "Difficulty" dropdown (in AI mode)

### Game Modes

1. **Human vs Human**: Both players use mouse to make moves
2. **Human vs AI**: Play against computer (AI plays as black by default)

### Special Features

- **Promotion**: When pawn reaches last rank, dialog appears to choose piece
- **Move History**: Click any move in history panel to jump to that position
- **Save/Load**: Use File menu or controller methods to save/load games

## Building Executable

### Prerequisites
```bash
pip install pyinstaller
```

### Build
```bash
build_exe.bat
```

### Run Executable
```bash
dist\ChessApp.exe
```

## Verification

Run these quick tests to verify everything works:

1. ✅ Application launches: `python main.py`
2. ✅ Can make moves (click piece, click destination)
3. ✅ AI mode works (toggle mode, make move, AI responds)
4. ✅ Promotion works (move pawn to last rank)
5. ✅ Undo works (make moves, click undo)
6. ✅ Build works: `build_exe.bat` creates `dist\ChessApp.exe`

## Need Help?

- **Full Documentation**: See `README.md`
- **Build Instructions**: See `BUILD_INSTRUCTIONS.md`
- **Verification**: See `VERIFICATION_CHECKLIST.md`
- **Troubleshooting**: Check console output for errors

## Common Issues

**Q: "No module named 'PyQt5'"**
```bash
pip install PyQt5
```

**Q: "No module named 'chess'"**
```bash
pip install python-chess
```

**Q: Pieces don't show**
- Application uses Unicode fallback if images missing
- First run will offer to download pieces automatically

**Q: AI doesn't move**
- Check mode is set to "Human vs AI"
- Verify difficulty is set
- Wait a few seconds (AI may take time to think)

**Q: Can't make moves**
- Click piece first (it will highlight)
- Then click destination square
- Invalid moves will be rejected

---

**Enjoy playing chess!** ♟️

