# Build Instructions - Chess Desktop Application

Complete guide for packaging the chess application into a standalone executable.

## Prerequisites

### 1. Install Required Packages

```bash
# Install all dependencies
pip install PyQt5 python-chess pyinstaller

# Or install from requirements file (if exists)
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
# Test that application runs in development mode
python main.py
```

If the application runs correctly, you're ready to build.

## Building the Executable

### Option 1: Using the Build Script (Recommended)

Simply run the batch file:

```bash
build_exe.bat
```

The script will:
1. Check if PyInstaller is installed
2. Clean previous build artifacts
3. Build the executable
4. Show the output location

### Option 2: Manual Build Command

Run PyInstaller directly:

```bash
pyinstaller --name=ChessApp --onefile --windowed --icon=assets\icon.ico --add-data "assets;assets" --add-data "settings.json;." main.py
```

## Understanding the Build Command

### Key Parameters

- `--name=ChessApp` - Name of the executable (output: `ChessApp.exe`)
- `--onefile` - Create a single executable file (all dependencies bundled)
- `--windowed` / `--noconsole` - Hide console window (GUI app only)
- `--icon=assets\icon.ico` - Application icon (remove if icon doesn't exist)
- `--add-data "assets;assets"` - Include assets folder
- `--add-data "settings.json;."` - Include settings file in root

### Windows Path Format for --add-data

**Important:** On Windows, use semicolon (`;`) to separate source and destination:

```bash
--add-data "source_path;destination_path_in_exe"
```

Examples:
- `--add-data "assets;assets"` - Copies `assets/` folder to `assets/` in exe
- `--add-data "settings.json;."` - Copies `settings.json` to root of exe
- `--add-data "data\pieces;pieces"` - Copies `data\pieces\` to `pieces\` in exe

**Linux/Mac:** Use colon (`:`) instead:
```bash
--add-data "assets:assets"
```

### Hidden Imports

If you encounter "ModuleNotFoundError" at runtime, add hidden imports:

```bash
--hidden-import=PyQt5
--hidden-import=chess
--collect-all=PyQt5  # Includes all PyQt5 submodules
```

## Build Output

After successful build:

- **Executable**: `dist/ChessApp.exe` (this is what you distribute)
- **Build files**: `build/` (temporary, can be deleted)
- **Spec file**: `ChessApp.spec` (can be reused for custom builds)

## Testing the Executable

### 1. Basic Test

```bash
# Run the executable
dist\ChessApp.exe
```

Verify:
- Application starts without errors
- Main window displays
- Chess board renders
- No console window appears

### 2. Feature Test

Test all features (see `PACKAGING_CHECKLIST.md` for detailed list):

- [ ] Make moves
- [ ] Promotion dialog
- [ ] AI mode
- [ ] Save/load game
- [ ] Settings persistence
- [ ] Piece images load

### 3. Clean System Test

Test on a system without Python installed:

1. Copy `dist\ChessApp.exe` to a clean Windows system
2. Run the executable
3. Verify it works without Python

## Including Non-Python Assets

### Method 1: Using --add-data (Recommended)

```bash
--add-data "assets;assets"
```

This copies the entire `assets/` folder into the executable.

**Access in code:**
```python
import sys
import os

if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(__file__)

assets_path = os.path.join(base_path, 'assets')
```

### Method 2: Manual Copy After Build

1. Build executable
2. Copy `assets/` folder next to `ChessApp.exe`
3. Create folder structure:
   ```
   dist/
   ├── ChessApp.exe
   └── assets/
       ├── pieces/
       └── icon.ico
   ```

### Method 3: Using .spec File (Advanced)

1. Generate spec file: `pyinstaller --name=ChessApp main.py`
2. Edit `ChessApp.spec` to customize data files
3. Build: `pyinstaller ChessApp.spec`

## Troubleshooting

### Problem: "ModuleNotFoundError"

**Solution:** Add hidden imports:
```bash
--hidden-import=<module_name>
```

Common missing imports:
- `PyQt5.QtCore`
- `chess.engine`
- `urllib.request`

### Problem: Assets Not Found

**Solution 1:** Check `--add-data` syntax:
- Windows: Use semicolon (`;`)
- Linux/Mac: Use colon (`:`)

**Solution 2:** Update code to use `sys._MEIPASS`:
```python
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)
```

### Problem: Large File Size

**Normal:** PyQt5 applications are typically 50-150 MB due to Qt libraries.

**To reduce size:**
- Use `--exclude-module` for unused modules
- Use UPX compression (advanced)

### Problem: Console Window Appears

**Solution:** Ensure `--windowed` or `--noconsole` flag is used.

### Problem: Icon Not Showing

**Solution:**
- Verify `assets/icon.ico` exists
- Check icon format (must be .ico on Windows)
- Try: `--icon=assets\icon.ico` (backslash for Windows)

## Advanced Options

### Custom Spec File

Create `ChessApp.spec` for advanced customization:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('settings.json', '.')],
    hiddenimports=['PyQt5', 'chess'],
    ...
)
```

Build with: `pyinstaller ChessApp.spec`

### Compression

Use UPX to compress executable (optional):

```bash
pyinstaller --upx-dir=path\to\upx --onefile main.py
```

### Debugging

Remove `--windowed` to see console output:

```bash
pyinstaller --onefile main.py  # Shows console
```

## Distribution

### Single File Distribution

The `--onefile` option creates a single `.exe` that:
- Extracts to temporary folder on first run
- Runs from temporary folder
- Cleans up on exit

**Pros:** Simple distribution (one file)
**Cons:** Slightly slower startup

### Directory Distribution

Remove `--onefile` for faster startup:

```bash
pyinstaller --windowed --icon=assets\icon.ico main.py
```

This creates `dist/ChessApp/` folder with:
- `ChessApp.exe`
- Supporting DLLs and files

**Pros:** Faster startup
**Cons:** Multiple files to distribute

## Verification Checklist

After building, verify:

- [ ] Executable exists: `dist/ChessApp.exe`
- [ ] File size is reasonable (50-150 MB)
- [ ] Application starts successfully
- [ ] All features work
- [ ] Assets are accessible
- [ ] Settings work correctly
- [ ] No console errors

See `PACKAGING_CHECKLIST.md` for detailed verification steps.

## Quick Reference

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
build_exe.bat

# Test executable
dist\ChessApp.exe

# Clean build (if needed)
rmdir /s /q build dist
del ChessApp.spec
```

## Support

For issues:
1. Check `PACKAGING_CHECKLIST.md` for common problems
2. Review PyInstaller documentation: https://pyinstaller.org/
3. Test with `--windowed` removed to see error messages

