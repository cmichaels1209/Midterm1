import os
import pytest
from app import App  # Import App

@pytest.fixture
def app():
    """Fixture to create an App instance before each test"""
    return App()

def test_logs(app, capsys):
    """Test that logs command works"""
    app.do_logs("")
    captured = capsys.readouterr()
    assert "Application Log History" in captured.out or "Log file is empty" in captured.out

def test_clear_logs(app, capsys):
    """Test that clearing logs works"""
    log_file = os.path.join(app.logs_dir, "app.log")

    # Ensure log file has content
    with open(log_file, "a", encoding="utf-8") as f:  # ✅ Explicit encoding
        f.write("Test log entry\n")

    with open(log_file, "r", encoding="utf-8") as f:  # ✅ Explicit encoding
        assert f.read().strip() != ""  # ✅ Ensure log file is not empty before clearing

    app.do_clear_logs("")
    captured = capsys.readouterr()
    assert "Application log history cleared." in captured.out

    # Check that the log file is empty after clearing
    with open(log_file, "r", encoding="utf-8") as f:  # ✅ Explicit encoding
        assert f.read().strip() == ""  # ✅ Ensuring log is empty after clearing
