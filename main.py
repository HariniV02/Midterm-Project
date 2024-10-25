import os
import logging
import pandas as pd
from abc import ABC, abstractmethod

# Create the logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level here directly
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),  # Log to file
        logging.StreamHandler()                # Also log to console
    ]
)

class CalculationHistory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CalculationHistory, cls).__new__(cls)
        return cls._instance

    def __init__(self, filename='calculation_history.csv'):
        if not hasattr(self, 'initialized'):
            self.filename = filename
            self.history = pd.DataFrame(columns=['operation', 'operands', 'result'])
            if os.path.exists(self.filename):
                self.history = pd.read_csv(self.filename)
            self.initialized = True

    def add_entry(self, operation, operands, result):
        new_entry = pd.DataFrame({'operation': [operation], 'operands': [operands], 'result': [result]})
        self.history = pd.concat([self.history, new_entry], ignore_index=True)
        self.save_history()

    def save_history(self):
        self.history.to_csv(self.filename, index=False)

    def clear_history(self):
        self.history = pd.DataFrame(columns=['operation', 'operands', 'result'])
        self.save_history()

    def delete_entry(self, index):
        if 0 <= index < len(self.history):
            self.history = self.history.drop(index).reset_index(drop=True)
            self.save_history()
        else:
            raise IndexError("Invalid index. Cannot delete entry.")

    def show_history(self):
        return self.history

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

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

class MenuCommand(Command):
    def execute(self):
        return "Available operations: add, subtract, multiply, divide, menu, history, clear, delete"

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

# Implementation of the Facade Pattern
class CalculationFacade:
    def __init__(self):
        self.history = CalculationHistory()
        self.handler = CommandHandler()

    def perform_operation(self, operation, a, b):
        command = self.create_command(operation, a, b)
        result = command.execute()
        self.history.add_entry(operation, (a, b), result)
        return result

    def create_command(self, operation, a, b):
        if operation == 'add':
            return AddCommand(a, b)
        elif operation == 'subtract':
            return SubtractCommand(a, b)
        elif operation == 'multiply':
            return MultiplyCommand(a, b)
        elif operation == 'divide':
            return DivideCommand(a, b)
        else:
            raise ValueError("Unknown operation.")

    def show_history(self):
        return self.history.show_history()

    def clear_history(self):
        self.history.clear_history()

    def delete_entry(self, index):
        self.history.delete_entry(index)

def main():
    facade = CalculationFacade()  # Use the Facade
    while True:
        operation = input("Enter operation (add, subtract, multiply, divide, menu, history, clear, delete) or 'quit' to exit: ")

        if operation == 'quit':
            logging.info("Exiting the app. Goodbye!")
            break

        if operation == 'menu':
            print("Available operations: add, subtract, multiply, divide, menu, history, clear, delete")
            logging.info("Displayed menu options.")
            continue

        if operation == 'history':
            print(facade.show_history())
            logging.info("Displayed calculation history.")
            continue

        if operation == 'clear':
            facade.clear_history()
            print("History cleared.")
            logging.info("Cleared calculation history.")
            continue

        if operation == 'delete':
            index = input("Enter the index of the entry to delete: ")
            try:
                index = int(index)
                facade.delete_entry(index)
                print(f"Entry at index {index} deleted.")
                logging.info(f"Deleted entry at index {index}.")
            except (ValueError, IndexError) as e:
                print(f"Error deleting entry: {e}")
                logging.error(f"Error deleting entry: {e}")
            continue

        a = input("Enter first number: ")
        b = input("Enter second number: ")

        try:
            a = int(a)
            b = int(b)

            # Perform the operation via the facade
            result = facade.perform_operation(operation, a, b)
            print(f"The result is: {result}")
            logging.info(f"Executed {operation} command with result: {result}")

        except ValueError as e:
            logging.error(f"Invalid input: {e}")
            print(f"Invalid input: {e}")

# Ensure the program starts correctly
if __name__ == "__main__":
    main()
