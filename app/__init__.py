import os
import sys
import logging
import importlib
import pkgutil
from dotenv import load_dotenv
from app.commands import CommandHandler, Command

# Load environment variables ONCE at the start
load_dotenv()

# Configure logging ONCE at the start
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("Logging configured.")

# Retrieve environment setting
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # Default to 'production' if not set
logger.info(f"Running in {ENVIRONMENT} mode")


class App:
    def __init__(self):
        """Initialize the application."""
        os.makedirs('logs', exist_ok=True)  # ✅ Ensure 'logs' directory exists
        self.settings = self.load_environment_variables()  # ✅ Load environment variables
        self.command_handler = CommandHandler()  # ✅ Initialize command handler

    def load_environment_variables(self):
        """Load and return all environment variables, ensuring uppercase normalization."""
        settings = {key.upper(): value.upper() for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        """Retrieve an environment variable."""
        return self.settings.get(env_var, None)

    def load_plugins(self):
        """Dynamically load all plugins in the 'app.plugins' directory."""
        plugins_package = "app.plugins"
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")

        if not os.path.exists(plugins_dir):
            logger.warning(f"Plugins directory '{plugins_dir}' not found.")
            return

        for _, plugin_name, _ in pkgutil.iter_modules([plugins_dir]):
            plugin_module = importlib.import_module(f"{plugins_package}.{plugin_name}")
            self.register_plugin_commands(plugin_module, plugin_name)

    def register_plugin_commands(self, plugin_module, plugin_name):
        """Register plugin commands dynamically."""
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                self.command_handler.register_command(plugin_name, item())
                logger.info(f"Registered command '{plugin_name}' from plugin '{plugin_name}'.")

    def start(self):
        """Start the application REPL loop."""
        self.load_plugins()
        print("Hello World. Type 'exit' to exit.")  # ✅ Print welcome message
        logger.info("Application started. Type 'exit' to exit.")

        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    print("Exiting...")
                    logger.info("Application exit.")
                    sys.exit(0)  # ✅ Exit cleanly

                try:
                    cmd_found = self.command_handler.execute_command(cmd_input)
                    if not cmd_found:
                        print(f"No such command: {cmd_input}")
                        logger.error(f"Unknown command: {cmd_input}")
                except Exception as e:
                    print(f"Error executing command: {e}")
                    logger.error(f"Error executing command {cmd_input}: {e}")

        except KeyboardInterrupt:
            print("Exiting...")
            logger.info("Application interrupted. Exiting gracefully.")
            sys.exit(0)
        finally:
            logger.info("Application shutdown.")

if __name__ == "__main__":
    app = App()
    app.start()
