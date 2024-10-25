import pandas as pd
import os

class CalculationHistory:
    def __init__(self, filename='calculation_history.csv'):
        self.filename = filename
        self.history = pd.DataFrame(columns=['operation', 'operands', 'result'])

        # Load existing history if the file exists
        if os.path.exists(self.filename):
            self.history = pd.read_csv(self.filename)

    def add_entry(self, operation, operands, result):
        new_entry = pd.DataFrame({'operation': [operation], 'operands': [operands], 'result': [result]})
        self.history = pd.concat([self.history, new_entry], ignore_index=True)

    def save_history(self):
        self.history.to_csv(self.filename, index=False)

    def clear_history(self):
        self.history = pd.DataFrame(columns=['operation', 'operands', 'result'])
        self.save_history()  # Save the cleared history to the file

    def delete_entry(self, index):
        if 0 <= index < len(self.history):
            self.history = self.history.drop(index).reset_index(drop=True)
            self.save_history()  # Save after deletion
        else:
            raise IndexError("Invalid index. Cannot delete entry.")

    def show_history(self):
        return self.history


