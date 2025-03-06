from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name, command_executor):
        self.commands[command_name.lower()] = command_executor

    def execute_command(self, command_input):
        # split the input into command and arguments
        parts = command_input.split()
        if not parts:
            return False

        command_name = parts[0].lower()
        args = parts[1:]

        if command_name in self.commands:
            executor = self.commands[command_name]
            # Handle both callable functions and command objects
            if callable(executor) and not hasattr(executor, 'execute'):
                executor(*args) # pass None as the app instance for simple functions
            else:
                executor.execute(*args) #for command objects
            return True
        return False


