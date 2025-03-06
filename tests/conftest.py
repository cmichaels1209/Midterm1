import pytest
from app import App

@pytest.fixture
def app_runner(monkeypatch):
    """Fixture to create an App instance and simulate REPL input."""
    def run_app_with_input(user_inputs):
        inputs = iter(user_inputs)
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        app = App()
        with pytest.raises(SystemExit) as e:
            app.start()

        return e, app  # Return both the exception and app instance

    return run_app_with_input
