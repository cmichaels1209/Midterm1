import logging
import pytest
from app import App  # Import your main App class

@pytest.fixture
def app():
    """Fixture to create an App instance before each test"""
    return App()

def test_add(app, capsys):
    """Test addition command"""
    app.do_add("4 5")
    captured = capsys.readouterr()
    assert "Result: 9.0" in captured.out

def test_subtract(app, capsys):
    """Test subtraction command"""
    app.do_subtract("10 3")
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out

def test_multiply(app, capsys):
    """Test multiplication command"""
    app.do_multiply("2 6")
    captured = capsys.readouterr()
    assert "Result: 12.0" in captured.out

def test_divide(app, capsys):
    """Test division command"""
    app.do_divide("9 3")
    captured = capsys.readouterr()
    assert "Result: 3.0" in captured.out

def test_divide_by_zero(app, capsys):
    """Test division by zero error handling"""
    app.do_divide("10 0")
    captured = capsys.readouterr()
    assert "Error: Division by zero" in captured.out

def test_invalid_input(app, capsys):
    """Test handling of non-numeric input"""
    app.do_add("3 a")
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out

def test_missing_argument(app, capsys):
    """Test handling of missing arguments"""
    app.do_multiply("5")
    captured = capsys.readouterr()
    assert "Invalid input" in captured.out
