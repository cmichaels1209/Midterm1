import os
import pandas as pd

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
        new_entry = pd.DataFrame([[operation, operand1, operand2, result]], columns=["operation", "operand1", "operand2", "result"])
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