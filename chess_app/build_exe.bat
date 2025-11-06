@echo off
REM ============================================================================
REM Build executable for Chess Desktop Application using PyInstaller
REM ============================================================================
REM
REM This script packages the chess application into a standalone .exe file
REM that can run on Windows without requiring Python installation.
REM
REM Prerequisites:
REM   1. Install PyInstaller: pip install pyinstaller
REM   2. Install all dependencies: pip install PyQt5 python-chess pyinstaller
REM   3. Ensure assets/icon.ico exists (or remove --icon flag)
REM
REM ============================================================================

echo.
echo ============================================================================
echo Building Chess Desktop Application...
echo ============================================================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed!
    echo Please run: pip install pyinstaller
    pause
    exit /b 1
)

REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ChessApp.spec del /q ChessApp.spec

echo Step 1: Cleaning previous build artifacts...
echo.

echo Step 2: Building executable with PyInstaller...
echo.

REM Build command for Windows
REM Note: --add-data uses semicolon (;) on Windows, colon (:) on Linux/Mac
REM Format: "source_path;destination_path_in_exe"
REM Multiple --add-data flags can be used for different directories/files

REM Check if icon exists and is valid, otherwise skip icon flag
if exist assets\icon.ico (
    pyinstaller --name=ChessApp ^
        --onefile ^
        --windowed ^
        --noconsole ^
        --icon=assets\icon.ico ^
        --add-data "assets;assets" ^
        --add-data "settings.json;." ^
        --hidden-import=PyQt5 ^
        --hidden-import=PyQt5.QtCore ^
        --hidden-import=PyQt5.QtWidgets ^
        --hidden-import=PyQt5.QtGui ^
        --hidden-import=chess ^
        --hidden-import=chess.engine ^
        --hidden-import=urllib.request ^
        --hidden-import=urllib.error ^
        --collect-all=PyQt5 ^
        main.py
) else (
    echo WARNING: Icon file not found or invalid. Building without icon...
    pyinstaller --name=ChessApp ^
        --onefile ^
        --windowed ^
        --noconsole ^
        --add-data "assets;assets" ^
        --add-data "settings.json;." ^
        --hidden-import=PyQt5 ^
        --hidden-import=PyQt5.QtCore ^
        --hidden-import=PyQt5.QtWidgets ^
        --hidden-import=PyQt5.QtGui ^
        --hidden-import=chess ^
        --hidden-import=chess.engine ^
        --hidden-import=urllib.request ^
        --hidden-import=urllib.error ^
        --collect-all=PyQt5 ^
        main.py
)

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo Build completed successfully!
echo ============================================================================
echo.
echo Executable location: dist\ChessApp.exe
echo.
echo Next steps:
echo   1. Test the executable: dist\ChessApp.exe
echo   2. Verify assets are included (pieces folder, settings.json)
echo   3. Check the PACKAGING_CHECKLIST.txt for verification steps
echo.
pause
