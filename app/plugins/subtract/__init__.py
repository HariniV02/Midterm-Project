from app.commands import Command

class SubtractCommand(Command):
    """Class to represent a subtraction command."""
    def __init__(self, a, b):
        """Initialize the command with two operands.
        """
        self.a = a
        self.b = b

    def execute(self):
        """Execute the subtraction command.
        """
        result = self.a - self.b
        print(f"SubtractCommand: {self.a} - {self.b} = {result}")
        return result  # Return the result here
