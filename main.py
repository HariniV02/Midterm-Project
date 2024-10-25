import os
import logging
import pandas as pd
from abc import ABC, abstractmethod

# Create the logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),  # Log to file
        logging.StreamHandler()                # Also log to console
    ]
)

# Define the CalculationHistory class
class CalculationHistory:
    def __init__(self, filename='calculation_history.csv'):
        self.filename = filename
        self.history = pd.DataFrame(columns=['operation', 'operands', 'result'])

        # Load existing history if the file exists
        if os.path.exists(self.filename):
            self.history = pd.read_csv(self.filename)

    def add_entry(self, operation, operands, result):
        new_entry = pd.DataFrame({'operation': [operation], 'operands': [operands], 'result': [result]})
        # Use pd.concat instead of append
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

# Define the Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Define individual command classes for each operation
class AddCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return self.a + self.b

class SubtractCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return self.a - self.b

class MultiplyCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return self.a * self.b

class DivideCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        if self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self.a / self.b

# MenuCommand to display the available operations
class MenuCommand(Command):
    def execute(self):
        return "Available operations: add, subtract, multiply, divide, menu, history, clear, delete"

# CommandHandler to manage the operations
class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, operation, command):
        self.commands[operation] = command

    def execute_command(self, operation):
        if operation in self.commands:
            return self.commands[operation].execute()
        else:
            raise ValueError("Unknown operation.")

# Main function to handle user input
def main():
    handler = CommandHandler()
    history = CalculationHistory()  # Create an instance of CalculationHistory

    while True:
        operation = input("Enter operation (add, subtract, multiply, divide, menu, history, clear, delete) or 'quit' to exit: ")

        if operation == 'quit':
            logging.info("Exiting the app. Goodbye!")
            break

        if operation == 'menu':
            handler.register_command('menu', MenuCommand())
            print(handler.execute_command('menu'))
            logging.info("Displayed menu options.")
            continue  # Skip to the next iteration for menu

        if operation == 'history':
            print(history.show_history())
            logging.info("Displayed calculation history.")
            continue

        if operation == 'clear':
            history.clear_history()
            print("History cleared.")
            logging.info("Cleared calculation history.")
            continue

        if operation == 'delete':
            index = input("Enter the index of the entry to delete: ")
            try:
                index = int(index)
                history.delete_entry(index)
                print(f"Entry at index {index} deleted.")
                logging.info(f"Deleted entry at index {index}.")
            except (ValueError, IndexError) as e:
                print(f"Error deleting entry: {e}")
                logging.error(f"Error deleting entry: {e}")
            continue

        a = input("Enter first number: ")
        b = input("Enter second number: ")

        # Try converting inputs to integers
        try:
            a = int(a)
            b = int(b)

            # Register the commands based on the input operation
            if operation == 'add':
                command = AddCommand(a, b)
            elif operation == 'subtract':
                command = SubtractCommand(a, b)
            elif operation == 'multiply':
                command = MultiplyCommand(a, b)
            elif operation == 'divide':
                command = DivideCommand(a, b)
            else:
                logging.error("Unknown operation.")
                print("Unknown operation.")
                continue

            # Execute the command
            result = command.execute()
            print(f"The result is: {result}")
            logging.info(f"Executed {operation} command with result: {result}")

            # Add to history
            history.add_entry(operation, (a, b), result)
            history.save_history()

        except ValueError as e:
            logging.error(f"Invalid input: {e}")
            print(f"Invalid input: {e}")

# Ensure the program starts correctly
if __name__ == "__main__":
    main()
