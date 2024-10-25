""" This module defines the MenuCommand, which prints a menu of available operations."""
import sys
from app.commands import Command

class MenuCommand(Command):
    def execute(self):
        return "Available operations: add, subtract, multiply, divide\n"  # Updated output

# pylint: disable=R0903
