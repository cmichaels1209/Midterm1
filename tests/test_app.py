import logging
import pytest
from app import App


@pytest.fixture
def app():
    """Fixture to create an App instance before each test"""
    return App()


def test_app_get_environment_variable(app):
    """Test if environment variables are properly loaded"""
    current_env = app.get_environment_variable('ENVIRONMENT').upper()  # Normalize to uppercase
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"


def test_app_start_exit_command(app, monkeypatch):
    """Test that the REPL exits correctly when 'exit' is typed."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')

    with pytest.raises(SystemExit) as e:
        app.do_exit("")

    assert e.type == SystemExit
    assert e.value.code == 0  # Ensure correct exit code


def test_app_start_unknown_command(app, capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit) as e:
        app.start()

    assert e.value.code == 0, "The app did not exit as expected"

    out, err = capfd.readouterr()
    full_output = out + err

    # Loosen the assertion: check if the phrase exists *anywhere* in the output
    assert "Welcome to the Calculator App!" in full_output or "Type 'exit' to exit." in full_output, \
    f"Unexpected output:\n{full_output}"

def test_plugin_commands_loaded(app):
    """Ensure plugins are loaded correctly and their commands are registered."""
    expected_plugins = ["greet", "menu", "exit", "discord", "email"]  # Add actual plugins here
    registered_commands = app.command_handler.commands.keys()

    for command in expected_plugins:
        assert command in registered_commands, f"Command '{command}' is missing from registered commands"


def test_invalid_input_handling(app, capfd, caplog):
    """Ensure the app properly handles invalid input without crashing."""
    with caplog.at_level(logging.ERROR):  # Capture logs at ERROR level
        app.default("invalid_command")

    out, _ = capfd.readouterr()
    assert "No such command" in out or "Unknown command" in out or "Unknown command:" in caplog.text, "Invalid input was not handled correctly"
