import os
import logging
from abc import ABC, abstractmethod

# Create the logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),  # Log to file
        logging.StreamHandler()               # Also log to console
    ]
)

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
        return f"The result of {self.a} add {self.b} is equal to {self.a + self.b}"

class SubtractCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return f"The result of {self.a} subtract {self.b} is equal to {self.a - self.b}"

class MultiplyCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        return f"The result of {self.a} multiply {self.b} is equal to {self.a * self.b}"

class DivideCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        if self.b == 0:
            return "An error occurred: Cannot divide by zero"
        return f"The result of {self.a} divide {self.b} is equal to {self.a // self.b}"

# MenuCommand to display the available operations
class MenuCommand(Command):
    def execute(self):
        return "Available operations: add, subtract, multiply, divide, menu"

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
            return "Unknown operation."

# Main function to handle user input
def main():
    handler = CommandHandler()

    while True:
        operation = input("Enter operation (add, subtract, multiply, divide, menu) or 'quit' to exit: ")

        if operation == 'quit':
            logging.info("Exiting the app. Goodbye!")
            break

        if operation == 'menu':
            handler.register_command('menu', MenuCommand())
            print(handler.execute_command('menu'))
            logging.info("Displayed menu options.")
            continue  # Skip to the next iteration for menu

        a = input("Enter first number: ")
        b = input("Enter second number: ")

        # Try converting inputs to integers
        try:
            a = int(a)
            b = int(b)

            # Register the commands based on the input operation
            if operation == 'add':
                handler.register_command('add', AddCommand(a, b))
            elif operation == 'subtract':
                handler.register_command('subtract', SubtractCommand(a, b))
            elif operation == 'multiply':
                handler.register_command('multiply', MultiplyCommand(a, b))
            elif operation == 'divide':
                handler.register_command('divide', DivideCommand(a, b))
            else:
                logging.error("Unknown operation.")
                print("Unknown operation.")
                continue

            # Execute the command
            result = handler.execute_command(operation)
            print(result)
            logging.info(f"Executed {operation} command with result: {result}")

        except ValueError:
            logging.error("Invalid input. Please enter valid numbers.")
            print("Invalid input. Please enter valid numbers.")

# Ensure the program starts correctly
if __name__ == "__main__":
    main()
