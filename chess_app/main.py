"""
Main entry point for the Chess Desktop Application.
Initializes the MVC components and starts the application.

DEVELOPER INSTRUCTIONS:
======================

1. INSTALLATION:
   Before running this application, install the required dependencies:
   
   pip install PyQt5 python-chess pyinstaller
   
   Note: This requires Python 3.10 or higher.

2. RUNNING THE APPLICATION:
   From the chess_app directory, run:
   
   python main.py
   
   Or from the parent directory:
   
   python chess_app/main.py

3. BUILDING EXECUTABLE:
   To create a standalone executable, use the provided build script:
   
   Windows: build_exe.bat
   Linux/Mac: Use PyInstaller command directly (see build_exe.bat for reference)

4. PROJECT STRUCTURE:
   - model/chess_model.py: Game logic and state management
   - model/ai_engine.py: AI opponent using minimax algorithm
   - view/chess_view.py: GUI interface with PyQt5
   - controller/chess_controller.py: Coordinates model, view, and AI
   - assets/pieces/: Directory for chess piece images (optional)
   - settings.json: Application settings (auto-created)

5. TROUBLESHOOTING:
   - If PyQt5 import fails: pip install PyQt5
   - If chess import fails: pip install python-chess
   - If window doesn't show: Check console for error messages
   - For piece images: Place PNG files in assets/pieces/ folder with names:
     white_king.png, white_queen.png, white_rook.png, white_bishop.png,
     white_knight.png, white_pawn.png, black_king.png, black_queen.png,
     black_rook.png, black_bishop.png, black_knight.png, black_pawn.png
"""

import sys
import chess
from PyQt5.QtWidgets import QApplication, QMessageBox
from controller.chess_controller import ChessController
from model.chess_model import ChessModel
from model.ai_engine import AIEngine
from view.chess_view import ChessView


def main():
    """
    Initialize and run the chess application.
    
    Creates the QApplication, instantiates MVC components,
    sets default game mode to Human vs Computer (Medium difficulty),
    and starts the application event loop.
    """
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Chess Desktop Application")
    app.setOrganizationName("Chess App")
    
    # Show developer credit popup
    msg = QMessageBox()
    msg.setWindowTitle("Chess Application")
    msg.setText("Developed by Muhammad Abdullah")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
    
    # Initialize MVC components
    print("Initializing Chess Model...")
    model = ChessModel()
    
    print("Initializing Chess View...")
    view = ChessView()
    
    print("Initializing Chess Controller...")
    controller = ChessController(model, view)
    
    # Set default mode to Human vs Computer (AI mode)
    print("Setting default mode: Human vs Computer")
    controller.game_mode = "ai"
    controller.ai_plays_as = chess.BLACK  # AI plays as black
    
    # Initialize AI engine with medium difficulty (depth 2)
    controller.ai_engine = AIEngine(depth=controller.ai_depth)
    
    # Update view to reflect AI mode
    if hasattr(view, 'mode_btn'):
        view.mode_btn.setText("Mode: Human vs AI")
        view.game_mode = "ai"  # Sync view state
    
    # Set difficulty to Medium (index 1 in combo box, depth 2)
    if hasattr(view, 'difficulty_combo'):
        view.difficulty_combo.setCurrentIndex(1)  # Medium = depth 2
        controller.ai_depth = 2  # Ensure controller has correct depth
        controller.ai_engine.depth = 2  # Update AI engine depth
    
    # Show the main window
    print("Showing main window...")
    view.show()
    
    # Start the application event loop
    print("Starting application...")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
