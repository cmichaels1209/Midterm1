import sys

class App:
    def __init__(self):
        """Initialize the application."""
        self.running = True

    def start(self):
        """Start the REPL loop."""
        print("Hello World. Type 'exit' to exit.")
        while self.running:
            user_input = input(">>> ").strip().lower()
            if user_input == "exit":
                print("Exiting...")
                sys.exit(0)  # <- Ensure SystemExit is raised
            elif user_input == "menu":
                print("Menu displayed...")
            else:
                print("Unknown command. Type 'exit' to exit.")
        
