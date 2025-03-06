import pytest
from app import App

def test_app_get_environment_variable():
    app = App()
#   Retrieve the current environment setting
    current_env = app.get_environment_variable('ENVIRONMENT')
    # Assert that the current environment is what you expect
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')

    app = App()  # ✅ Create an instance of App
    with pytest.raises(SystemExit) as e:  # ✅ Capture SystemExit
        app.start()

    assert e.value.code == 0, "The app did not exit as expected"

    out, _ = capfd.readouterr()
    assert "Hello World. Type 'exit' to exit." in out
    assert "Exiting..." in out

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    assert e.value.code == 0, "The app did not exit as expected"

    out, _ = capfd.readouterr()
    assert "Hello World. Type 'exit' to exit." in out
    assert "No such command: unknown_command" in out  # ✅ Fix assertion
    assert "Exiting..." in out
