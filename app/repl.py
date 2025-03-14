import cmd
import logging
import os
import importlib
import pandas as pd
from abc import ABC, abstractmethod

# Configure logging
def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, log_level),
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='calculator.log', filemode='a')
setup_logging()

# Singleton for history management
class HistoryManager:
    _instance = None
    _history_file = "history.csv"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistoryManager, cls).__new__(cls)
            cls._instance.history = pd.DataFrame(columns=["operation", "operand1", "operand2", "result"])
            cls._instance.load_history()
        return cls._instance

    def save_to_history(self, operation, operand1, operand2, result):
        new_entry = pd.DataFrame([[operation, operand1, operand2, result]],
                                 columns=["operation", "operand1", "operand2", "result"])
        self.history = pd.concat([self.history, new_entry], ignore_index=True)
        self.history.to_csv(self._history_file, index=False)

    def load_history(self):
        if os.path.exists(self._history_file):
            self.history = pd.read_csv(self._history_file)

    def clear_history(self):
        self.history = pd.DataFrame(columns=["operation", "operand1", "operand2", "result"])
        self.history.to_csv(self._history_file, index=False)

    def show_history(self):
        return self.history

# Command Pattern for calculator operations
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddCommand(Command):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self):
        result = self.x + self.y
        HistoryManager().save_to_history("Add", self.x, self.y, result)
        return result

class SubtractCommand(Command):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self):
        result = self.x - self.y
        HistoryManager().save_to_history("Subtract", self.x, self.y, result)
        return result

class MultiplyCommand(Command):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self):
        result = self.x * self.y
        HistoryManager().save_to_history("Multiply", self.x, self.y, result)
        return result

class DivideCommand(Command):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def execute(self):
        if self.y == 0:
            logging.error("Attempted division by zero")
            return "Error: Division by zero"
        result = self.x / self.y
        HistoryManager().save_to_history("Divide", self.x, self.y, result)
        return result

# REPL Interface
class CalculatorREPL(cmd.Cmd):
    prompt = "(calc) "

    def do_add(self, args):
        "Usage: add x y - Perform addition"
        try:
            x, y = map(float, args.split())
            print(AddCommand(x, y).execute())
        except Exception as e:
            print("Invalid input.", e)

    def do_subtract(self, args):
        "Usage: subtract x y - Perform subtraction"
        try:
            x, y = map(float, args.split())
            print(SubtractCommand(x, y).execute())
        except Exception as e:
            print("Invalid input.", e)

    def do_multiply(self, args):
        "Usage: multiply x y - Perform multiplication"
        try:
            x, y = map(float, args.split())
            print(MultiplyCommand(x, y).execute())
        except Exception as e:
            print("Invalid input.", e)

    def do_divide(self, args):
        "Usage: divide x y - Perform division"
        try:
            x, y = map(float, args.split())
            print(DivideCommand(x, y).execute())
        except Exception as e:
            print("Invalid input.", e)

    def do_history(self, args):
        "Usage: history - Display calculation history"
        print(HistoryManager().show_history())

    def do_clear_history(self, args):
        "Usage: clear_history - Clear all history records"
        HistoryManager().clear_history()
        print("History cleared.")

    def do_menu(self, args):
        "Usage: menu - List all available commands"
        commands = ["add", "subtract", "multiply", "divide", "history", "clear_history", "menu", "load_plugin", "exit"]
        print("Available commands:", ", ".join(commands))

    def do_load_plugin(self, args):
        "Usage: load_plugin plugin_name - Dynamically load a plugin"
        try:
            module = importlib.import_module(f"plugins.{args}")
            plugin = module.Plugin()
            setattr(self, f"do_{args}", plugin.execute)
            print(f"Plugin '{args}' loaded successfully.")
        except Exception as e:
            print("Failed to load plugin.", e)

    def do_exit(self, args):
        "Usage: exit - Exit the calculator"
        print("Exiting calculator...")
        return True

if __name__ == "__main__":
    CalculatorREPL().cmdloop()