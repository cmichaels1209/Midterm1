import os
import pkgutil
import importlib
import sys
from app.commands import CommandHandler, Command
from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        """Dynamically load all plugins in the app.plugins directory."""
        plugins_package = "app.plugins"
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")

        if not os.path.exists(plugins_dir):
            print(f"WARNING: Plugins directory '{plugins_dir}' not found.")
            return

        for _, plugin_name, _ in pkgutil.iter_modules([plugins_dir]):
            plugin_module = importlib.import_module(f"{plugins_package}.{plugin_name}")
            for item_name in dir(plugin_module):
                item = getattr(plugin_module, item_name)
                if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                    self.command_handler.register_command(plugin_name, item())

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                # Command names are now explicitly set to the plugin's folder name
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        self.load_plugins()
        print("Hello World. Type 'exit' to exit.")  # Print welcome message to console
        logging.info("Application started. Type 'exit' to exit.")

        try:
            while True:
                cmd_input = input(">>> ").strip()
                if cmd_input.lower() == 'exit':
                    print("Exiting...")  # Print exit message
                    logging.info("Application exit.")
                    sys.exit(0)  # Use sys.exit(0) for a clean exit, indicating success.

                try:
                    cmd_found = self.command_handler.execute_command(cmd_input)
                    if not cmd_found:
                        print(f"No such command: {cmd_input}")
                        logging.error(f"Unknown command: {cmd_input}")
                except Exception as e:
                    print(f"Error executing command: {e}")
                    logging.error(f"Error executing command {cmd_input}: {e}")



        except KeyboardInterrupt:
            print("Exiting...")
            logging.info("Application interrupted and exiting gracefully.")
            sys.exit(0)
        finally:
            logging.info("Application shutdown.")

if __name__ == "__main__":
    app = App()
    app.start()
