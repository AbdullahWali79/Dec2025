"""
Pytest configuration and fixtures for chess application tests.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication for GUI tests."""
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def chess_model():
    """Create a fresh ChessModel instance for each test."""
    from model.chess_model import ChessModel
    return ChessModel()


@pytest.fixture
def ai_engine():
    """Create an AIEngine instance for each test."""
    from model.ai_engine import AIEngine
    return AIEngine(depth=2)


@pytest.fixture
def chess_view(qapp):
    """Create a ChessView instance for each test."""
    from view.chess_view import ChessView
    view = ChessView()
    yield view
    view.close()

