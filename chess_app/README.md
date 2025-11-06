# Chess Desktop Application

A PyQt5-based desktop chess application built with the Model-View-Controller (MVC) architecture pattern.

## Requirements

### Python Version
- **Python 3.10 or higher** is required

### Required Packages
Install the following packages using pip:

```bash
pip install PyQt5 python-chess pyinstaller
```

#### Package Details:
- **PyQt5** (>=5.15.0): GUI framework for the desktop application interface
- **python-chess** (>=1.999): Chess engine library for game logic, move validation, and board state management
- **pyinstaller** (>=5.0): Used for packaging the application into a standalone executable

## Project Structure

```
chess_app/
├── main.py                 # Application entry point
├── model/
│   └── chess_model.py      # Game logic and state management
├── view/
│   └── chess_view.py       # GUI and user interface
├── controller/
│   └── chess_controller.py # Coordinates Model and View
├── assets/
│   ├── pieces/             # Chess piece images (placeholders)
│   └── icon.ico           # Application icon (placeholder)
├── settings.json           # Application configuration
├── build_exe.bat          # Script to build executable
└── README.md              # This file
```

## File Responsibilities

### `main.py`
- **Purpose**: Application entry point
- **Responsibilities**:
  - Initializes the QApplication
  - Creates instances of Model, View, and Controller
  - Connects the MVC components
  - Starts the application event loop

### `model/chess_model.py`
- **Purpose**: Game logic and state management
- **Responsibilities**:
  - Manages the chess board state using `python-chess`
  - Handles move validation and execution
  - Tracks game history
  - Determines game over conditions (checkmate, stalemate, etc.)
  - Provides legal move generation
  - Manages game reset functionality

### `view/chess_view.py`
- **Purpose**: User interface and presentation
- **Responsibilities**:
  - Creates and manages the PyQt5 GUI window
  - Displays the chess board
  - Shows game status and turn information
  - Provides UI controls (undo, reset buttons)
  - Emits signals for user interactions (moves, undo, reset)
  - Displays game over messages

### `controller/chess_controller.py`
- **Purpose**: Coordinates between Model and View
- **Responsibilities**:
  - Receives user input from the View
  - Validates and processes moves through the Model
  - Updates the View with current board state
  - Handles undo and reset operations
  - Manages game state synchronization between Model and View

### `assets/`
- **Purpose**: Application resources
- **Contents**:
  - `pieces/`: Directory for chess piece image files (PNG/SVG)
  - `icon.ico`: Application icon for the window and executable

#### Chess Piece Images

The application supports custom chess piece images. On first run, if pieces are missing, the application will offer to download default open-license pieces from Wikimedia Commons.

**Required Filenames:**
- `white_king.png`, `white_queen.png`, `white_rook.png`, `white_bishop.png`, `white_knight.png`, `white_pawn.png`
- `black_king.png`, `black_queen.png`, `black_rook.png`, `black_bishop.png`, `black_knight.png`, `black_pawn.png`

**Image Recommendations:**
- **Format**: PNG (preferred) or SVG
- **Size**: 45x45 pixels to 128x128 pixels recommended
- **Background**: Transparent (PNG with alpha channel)
- **Aspect Ratio**: Square (1:1)
- **Color**: Clear distinction between white and black pieces

**Loading Custom Pieces:**
1. Place your piece images in the `assets/pieces/` folder with the exact filenames listed above
2. Or use the "Load Piece Folder" button in the toolbar to select a custom folder
3. The application will automatically detect and use PNG images, falling back to Unicode symbols if images are missing

**Automatic Download:**
- On first launch, if pieces are missing, you'll be prompted to download default pieces
- Default pieces are sourced from Wikimedia Commons (public domain/CC0 license)
- Downloaded pieces are saved as SVG format and work with PyQt5

### `settings.json`
- **Purpose**: Application configuration
- **Stores**:
  - Window dimensions
  - Board theme preferences
  - Sound settings
  - Auto-save preferences
  - Game difficulty settings

### `build_exe.bat`
- **Purpose**: Build script for creating a standalone executable
- **Functionality**:
  - Uses PyInstaller to package the application
  - Creates a single executable file (`ChessApp.exe`)
  - Includes assets and configuration files
  - Sets up the application icon

## Quick Start

### Running the Application

#### Development Mode
```bash
# Install dependencies first
pip install PyQt5 python-chess

# Run the application
python main.py
```

**Expected Result:**
- Application window opens
- Chess board displays with starting position
- Toolbar and move history panel visible
- Status bar shows "White to move"

#### Troubleshooting Launch Issues

**Problem: Import errors**
```bash
# Solution: Install missing dependencies
pip install PyQt5 python-chess
```

**Problem: Window doesn't open**
- Check Python version: `python --version` (requires 3.10+)
- Verify PyQt5: `pip list | findstr PyQt5`
- Check console for error messages

**Problem: Pieces don't display**
- Application will use Unicode fallback if images missing
- On first run, you'll be prompted to download pieces

### Building Executable

#### Prerequisites
```bash
pip install pyinstaller
```

#### Quick Build
```bash
build_exe.bat
```

The executable will be created in the `dist/` folder as `ChessApp.exe`.

#### Manual Build
```bash
pyinstaller --name=ChessApp --onefile --windowed --icon=assets\icon.ico --add-data "assets;assets" --add-data "settings.json;." main.py
```

**Important:** On Windows, use semicolon (`;`) in `--add-data`. On Linux/Mac, use colon (`:`).

#### Testing the Executable
1. Run: `dist\ChessApp.exe`
2. Verify all features work (see `PACKAGING_CHECKLIST.md`)
3. Test on a clean system (without Python installed)

For detailed build instructions, see `BUILD_INSTRUCTIONS.md`.
For packaging verification, see `PACKAGING_CHECKLIST.md`.

## Architecture

This application follows the **Model-View-Controller (MVC)** pattern:

- **Model** (`chess_model.py`): Manages data and business logic
- **View** (`chess_view.py`): Handles presentation and user input
- **Controller** (`chess_controller.py`): Mediates between Model and View

The Model is independent of the View, making the codebase modular and maintainable.

## Future Enhancements

Potential improvements for this scaffold:
- Visual chess board with piece images
- Move input via click-and-drag
- Game history and move notation
- Save/load game functionality
- AI opponent integration
- Online multiplayer support
- Sound effects and animations

