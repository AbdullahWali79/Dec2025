# Packaging Checklist - Chess Desktop Application

This checklist helps verify that the packaged executable works correctly and includes all necessary files.

## Pre-Build Checklist

Before building the executable, verify:

- [ ] All dependencies are installed: `pip install PyQt5 python-chess pyinstaller`
- [ ] Application runs correctly in development mode: `python main.py`
- [ ] `assets/icon.ico` exists (or remove `--icon` flag from build script)
- [ ] `assets/pieces/` folder exists (or will be created at runtime)
- [ ] `settings.json` exists (or will be created at runtime)
- [ ] All required Python files are present:
  - [ ] `main.py`
  - [ ] `model/chess_model.py`
  - [ ] `model/ai_engine.py`
  - [ ] `view/chess_view.py`
  - [ ] `controller/chess_controller.py`
  - [ ] `utils/asset_downloader.py`

## Build Process

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Run Build Script

```bash
# From the chess_app directory
build_exe.bat
```

Or manually:

```bash
pyinstaller --name=ChessApp --onefile --windowed --icon=assets\icon.ico --add-data "assets;assets" --add-data "settings.json;." main.py
```

**Important Windows Path Format:**
- Use semicolon (`;`) in `--add-data` on Windows: `"assets;assets"`
- Use colon (`:`) on Linux/Mac: `"assets:assets"`
- Format: `"source_path;destination_path_in_exe"`

### Step 3: Verify Build Output

After build completes, check:

- [ ] `dist/ChessApp.exe` exists
- [ ] No critical errors in build output
- [ ] File size is reasonable (typically 50-150 MB for PyQt5 apps)

## Post-Build Verification

### File Structure

Verify the executable includes:

- [ ] **Executable**: `dist/ChessApp.exe` (main executable)
- [ ] **Assets folder** should be bundled (check if accessible at runtime)

### Runtime Testing

Run `dist\ChessApp.exe` and verify:

#### Basic Functionality
- [ ] Application starts without errors
- [ ] Main window displays correctly
- [ ] Chess board renders properly
- [ ] No console window appears (if using --windowed)

#### Piece Display
- [ ] Chess pieces display (images or Unicode fallback)
- [ ] Pieces load from `assets/pieces/` folder
- [ ] Fallback to Unicode works if images missing
- [ ] Piece images scale correctly on resize

#### Game Functionality
- [ ] Can make moves (click piece, click destination)
- [ ] Legal moves highlight correctly
- [ ] Invalid moves are rejected
- [ ] Undo button works
- [ ] New Game button works

#### Special Moves
- [ ] Promotion dialog appears when pawn reaches last rank
- [ ] Can select promotion piece (Queen, Rook, Bishop, Knight)
- [ ] Castling works (if applicable)
- [ ] En passant works (if applicable)

#### AI Functionality
- [ ] AI mode toggle works
- [ ] AI makes moves automatically
- [ ] Difficulty settings work
- [ ] AI moves are legal

#### UI Components
- [ ] Toolbar buttons work
- [ ] Mode toggle works
- [ ] Difficulty dropdown works
- [ ] Load piece folder button works
- [ ] Status bar updates correctly
- [ ] Move history panel displays moves
- [ ] Clicking move history navigates to position

#### Dialogs
- [ ] Promotion dialog appears correctly
- [ ] End-of-game dialog appears (checkmate/stalemate/draw)
- [ ] End-of-game dialog "New Game" button works
- [ ] End-of-game dialog "Close" button works
- [ ] File dialogs work (save/load game)

#### Settings
- [ ] Settings load from `settings.json`
- [ ] Settings save correctly
- [ ] Window size persists
- [ ] Difficulty setting persists

#### Asset Loading
- [ ] Custom piece folder loading works
- [ ] Automatic piece download works (if internet available)
- [ ] Graceful fallback if download fails

### Error Handling

Test error scenarios:

- [ ] Missing `assets/pieces/` folder - app still runs (Unicode fallback)
- [ ] Missing `settings.json` - app creates default
- [ ] Invalid FEN file - shows error message
- [ ] Network unavailable - asset download fails gracefully

### Performance

- [ ] Application starts within 5 seconds
- [ ] Moves execute immediately
- [ ] AI responds within reasonable time (< 5 seconds for depth 2)
- [ ] Window resize is smooth
- [ ] No memory leaks (run for extended period)

### File Size and Dependencies

- [ ] Executable size is reasonable (50-150 MB typical for PyQt5)
- [ ] No external DLL dependencies required
- [ ] All Python libraries bundled

## Troubleshooting

### Common Issues

#### Issue: "Failed to execute script main"
**Solution:**
- Check for hidden imports in `build_exe.bat`
- Verify all dependencies are installed
- Try adding `--hidden-import=<module>` for missing modules

#### Issue: Assets not found at runtime
**Solution:**
- Verify `--add-data` syntax is correct (semicolon on Windows)
- Check that assets folder is included in build
- Use `sys._MEIPASS` for accessing bundled files in code

#### Issue: Large executable size
**Solution:**
- This is normal for PyQt5 applications (includes Qt libraries)
- Consider using `--exclude-module` for unused modules
- Use UPX compression if needed (advanced)

#### Issue: Application crashes on startup
**Solution:**
- Remove `--windowed` flag to see error messages
- Check console output for import errors
- Verify all dependencies are included

#### Issue: Icon not showing
**Solution:**
- Verify `assets/icon.ico` exists
- Check icon file format (must be .ico on Windows)
- Try removing `--icon` flag to test without icon

### Testing on Different Systems

If possible, test on:

- [ ] Windows 10
- [ ] Windows 11
- [ ] Different screen resolutions
- [ ] Systems without Python installed

## Distribution

Before distributing:

- [ ] Create a README for end users
- [ ] Include version information
- [ ] Test on clean Windows system (no Python installed)
- [ ] Create installer (optional, using Inno Setup or NSIS)
- [ ] Sign executable (optional, for security)

## Build Command Reference

### Windows (Current)
```bash
pyinstaller --name=ChessApp --onefile --windowed --icon=assets\icon.ico --add-data "assets;assets" --add-data "settings.json;." main.py
```

### Linux/Mac (Alternative)
```bash
pyinstaller --name=ChessApp --onefile --windowed --icon=assets/icon.ico --add-data "assets:assets" --add-data "settings.json:." main.py
```

**Note:** Change semicolon (`;`) to colon (`:`) for `--add-data` on Linux/Mac.

## Quick Test Commands

```bash
# Test in development mode first
python main.py

# Build executable
build_exe.bat

# Test executable
dist\ChessApp.exe

# Check file size
dir dist\ChessApp.exe
```

## Final Checklist

Before release:

- [ ] All tests pass: `pytest tests/`
- [ ] Executable runs without errors
- [ ] All features work correctly
- [ ] Assets are included
- [ ] Settings work correctly
- [ ] No console errors
- [ ] File size is acceptable
- [ ] Documentation is updated

---

**Last Updated:** After Step 9 completion
**Build Script:** `build_exe.bat`
**Output Location:** `dist/ChessApp.exe`

