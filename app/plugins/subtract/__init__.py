from app.commands import Command

class SubtractCommand(Command):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def execute(self):
        result = self.a - self.b
        print(f"SubtractCommand: {self.a} - {self.b} = {result}")
        return result  # Return the result here