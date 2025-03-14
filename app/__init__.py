import os
import pkgutil
import importlib
import sys
import cmd
import logging
import logging.config
import pandas as pd
from dotenv import load_dotenv
from app.commands import CommandHandler, Command
from app.history_manager import HistoryManager  # Import history manager

class App(cmd.Cmd):
    prompt = ">>> "  # REPL prompt

    def __init__(self):
        super().__init__()
        self.logs_dir = 'logs'
        os.makedirs(self.logs_dir, exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.history_manager = HistoryManager()  # Singleton for history
        self.load_plugins()  # Load available plugins

    def configure_logging(self):
        log_file_path = os.path.join(self.logs_dir, "app.log")  # Log file inside logs directory
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(log_file_path, mode="a")])
        logging.getLogger(__name__).info(f"Logging initialized successfully! Logs saved in {log_file_path}")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"✅ Command '{plugin_name}' from plugin '{plugin_name}' registered successfully.")

    def do_add(self, args):
        """Usage: add x y - Perform addition"""
        try:
            x, y = map(float, args.split())
            result = x + y
            self.history_manager.save_to_history("Add", x, y, result)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Invalid input: {e}")

    def do_subtract(self, args):
        """Usage: subtract x y - Perform subtraction"""
        try:
            x, y = map(float, args.split())
            result = x - y
            self.history_manager.save_to_history("Subtract", x, y, result)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Invalid input: {e}")

    def do_multiply(self, args):
        """Usage: multiply x y - Perform multiplication"""
        try:
            x, y = map(float, args.split())
            result = x * y
            self.history_manager.save_to_history("Multiply", x, y, result)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Invalid input: {e}")

    def do_divide(self, args):
        """Usage: divide x y - Perform division"""
        try:
            x, y = map(float, args.split())
            if y == 0:
                print("Error: Division by zero")
                return
            result = x / y
            self.history_manager.save_to_history("Divide", x, y, result)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Invalid input: {e}")

    def do_history(self, args):
        """Usage: history - Show calculation history"""
        print(self.history_manager.show_history())

    def do_clear_history(self, args):
        """Usage: clear_history - Clear calculation history"""
        self.history_manager.clear_history()
        print("Calculation history cleared.")

    def do_menu(self, arg):
        """Display the available calculator commands."""
        commands = {
            "add": "Addition operation",
            "subtract": "Subtraction operation",
            "multiply": "Multiplication operation",
            "divide": "Division operation",
            "history": "View calculation history",
            "clear_history": "Clear calculation history",
            "logs": "View application logs",
            "clear_logs": "Clear logs",
            "exit": "Exit the calculator"
        }

        print("\nAvailable Commands:")
        for command, description in commands.items():
            print(f" - {command}: {description}")



    def do_exit(self, args):
        """Usage: exit - Exit the application"""
        print("Exiting calculator...")
        logging.info("Application exited.")

        if 'PYTEST_CURRENT_TEST' in os.environ:
            raise SystemExit(0)  # Ensure pytest can catch the exception
        else:
            sys.exit(0)  # Normal exit for regular execution

    def do_greet(self, _):
        """Handles the 'greet' command."""
        print("Hello, World!")


    def start(self):
        """Start the REPL loop"""
        logging.info("Application started. Type 'exit' to exit.")
        print("Welcome to the Calculator App! Type 'menu' to see commands.")  # <-- Add this if missing
        self.cmdloop()  # Starts REPL

    def default(self, line):
        """Handle unknown commands by converting them to lowercase, avoiding infinite recursion."""
        line = line.lower()

        if line in self.get_names():  # Check if the command exists in the registered commands
            self.onecmd(line)
        else:
            print(f"Unknown command: {line}")  # Gracefully handle unknown commands


    def do_logs(self, args):
        """Usage: logs - Show application log history."""
        log_file_path = os.path.join(self.logs_dir, "app.log")
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                logs = log_file.readlines()
                if logs:
                    print("==== Application Log History ====")
                    for line in logs[-20:]:  # Show only the last 20 logs to avoid flooding the screen
                        print(line.strip())
                else:
                    print("Log file is empty.")
        else:
            print("No log file found.")

    def do_clear_logs(self, args):
        """Usage: clear_logs - Clear application log history."""
        log_file_path = os.path.join(self.logs_dir, "app.log")
        if os.path.exists(log_file_path):
            with open(log_file_path, "w") as log_file:
                log_file.truncate(0)  # Clear log file contents
            print("Application log history cleared.")
        else:
            print("No log file found to clear.")

    def do_add(self, args):
        """Usage: add x y - Perform Addition"""
        try:
            x, y = map(float, args.split())
            result = x + y
            self.history_manager.save_to_history("Add", x, y, result)
            logging.info(f"Performed Addition: {x} + {y} = {result}")  # ✅ Log operation
            print(f"Result: {result}")
        except Exception as e:
            logging.error(f"Addition failed: {args} - Error: {e}")
            print(f"Invalid input: {e}")

    def do_subtract(self, args):
        """Usage: subtract x y - Perform subtraction"""
        try:
            x, y = map(float, args.split())
            result = x - y
            self.history_manager.save_to_history("Subtract", x, y, result)
            logging.info(f"Performed Subtraction: {x} - {y} = {result}")  # ✅ Log operation
            print(f"Result: {result}")
        except Exception as e:
            logging.error(f"Subtraction failed: {args} - Error: {e}")
            print(f"Invalid input: {e}")

    def do_multiply(self, args):
        """Usage: multiply x y - Perform multiplication"""
        try:
            x, y = map(float, args.split())
            result = x * y
            self.history_manager.save_to_history("Multiply", x, y, result)
            logging.info(f"Performed Multiplication: {x} * {y} = {result}")  # ✅ Log operation
            print(f"Result: {result}")
        except Exception as e:
            logging.error(f"Multiplication failed: {args} - Error: {e}")
            print(f"Invalid input: {e}")

    def do_divide(self, args):
        """Usage: divide x y - Perform division"""
        try:
            x, y = map(float, args.split())
            if y == 0:
                logging.warning(f"Division by zero attempt: {x} / {y}")  # ✅ Log warning
                print("Error: Division by zero")
                return
            result = x / y
            self.history_manager.save_to_history("Divide", x, y, result)
            logging.info(f"Performed Division: {x} / {y} = {result}")  # ✅ Log operation
            print(f"Result: {result}")
        except Exception as e:
            logging.error(f"Division failed: {args} - Error: {e}")
            print(f"Invalid input: {e}")

if __name__ == "__main__":
    app = App()
    app.start()
