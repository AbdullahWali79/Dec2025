# Chess Application - Test Suite

This directory contains unit tests for the Chess Desktop Application.

## Test Files

- `test_chess_model.py` - Tests for ChessModel class
- `test_ai_engine.py` - Tests for AIEngine class  
- `test_chess_view.py` - Tests for ChessView class
- `conftest.py` - Pytest fixtures and configuration
- `TEST_CHECKLIST.md` - Comprehensive test checklist

## Installation

### Install Test Dependencies

```bash
# From the chess_app directory
pip install -r requirements-test.txt

# Or install individually
pip install pytest pytest-qt pytest-cov
```

### Required Packages
- `pytest` - Testing framework
- `pytest-qt` - PyQt5 testing support
- `pytest-cov` - Code coverage reporting

## Running Tests

### Run All Tests

```bash
# From the chess_app directory
pytest tests/

# Or with verbose output
pytest tests/ -v
```

### Run Specific Test File

```bash
# Model tests
pytest tests/test_chess_model.py

# AI engine tests
pytest tests/test_ai_engine.py

# View tests
pytest tests/test_chess_view.py
```

### Run Specific Test Class

```bash
pytest tests/test_chess_model.py::TestChessModel
```

### Run Specific Test Method

```bash
pytest tests/test_chess_model.py::TestChessModel::test_legal_moves_starting_position
```

### Run Tests with Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage
pytest tests/ --cov=model --cov=view --cov=controller --cov-report=html

# View HTML report
# Open htmlcov/index.html in browser
```

### Run Tests with Output

```bash
# Show print statements
pytest tests/ -s

# Show local variables on failure
pytest tests/ -l

# Stop on first failure
pytest tests/ -x
```

## Test Coverage

### Model Tests (test_chess_model.py)

Tests cover:
- ✅ Legal move generation
- ✅ Castling (kingside and queenside)
- ✅ En passant capture
- ✅ Pawn promotion
- ✅ Checkmate detection
- ✅ Stalemate detection
- ✅ FEN loading and saving
- ✅ Move execution and undo

### AI Engine Tests (test_ai_engine.py)

Tests cover:
- ✅ AI returns legal moves
- ✅ AI handles different positions
- ✅ AI handles game over states
- ✅ AI works with different depths
- ✅ AI handles promotion positions
- ✅ Node evaluation counting

### View Tests (test_chess_view.py)

Tests cover:
- ✅ Board rendering from FEN
- ✅ Piece display (images and Unicode)
- ✅ Square highlighting
- ✅ Promotion dialog
- ✅ End-of-game dialog
- ✅ Move history panel
- ✅ UI component functionality

## Expected Test Results

When all tests pass, you should see:

```
tests/test_chess_model.py::TestChessModel::test_new_game PASSED
tests/test_chess_model.py::TestChessModel::test_legal_moves_starting_position PASSED
tests/test_chess_model.py::TestChessModel::test_push_move_valid PASSED
...
tests/test_ai_engine.py::TestAIEngine::test_ai_select_move_starting_position PASSED
...
tests/test_chess_view.py::TestChessView::test_view_initialization PASSED
...

========================== X passed in Y.YYs ==========================
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running tests from the `chess_app` directory:

```bash
cd chess_app
pytest tests/
```

### PyQt5 Errors

If PyQt5 tests fail, ensure PyQt5 is installed:

```bash
pip install PyQt5
```

### QApplication Errors

If you see "QApplication already exists" errors, the `conftest.py` fixture should handle this. If issues persist, try:

```bash
pytest tests/ --no-qt
```

## Continuous Integration

For CI/CD pipelines, run:

```bash
# Install dependencies
pip install -r requirements-test.txt

# Run tests with coverage
pytest tests/ --cov=model --cov=view --cov=controller --cov-report=xml --cov-report=term

# Check coverage threshold (optional)
pytest tests/ --cov=model --cov=view --cov=controller --cov-fail-under=80
```

## Adding New Tests

When adding new features:

1. Add corresponding tests to the appropriate test file
2. Follow the existing test naming convention: `test_<feature_name>`
3. Use descriptive test names
4. Update `TEST_CHECKLIST.md` with new test items
5. Ensure tests pass before committing

## Test Checklist

See `TEST_CHECKLIST.md` for a comprehensive checklist of all test scenarios.

