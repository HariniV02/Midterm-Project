""""
Provides fixtures and utilities for generating test data dynamically
using the Faker library and parametrize test functions in pytest.
"""

from decimal import Decimal
from faker import Faker
from calculator.operations import add, subtract, multiply, divide

# Initialize Faker
fake = Faker()

# Define the operation mappings
operation_mappings = {
    'add': add,
    'multiply': multiply,
    'divide': divide
}

def generate_test_data(num_records):
    """
    Generates test data for arithmetic operations using Faker.
    Yields tuples (a, b, operation_name, operation_func, expected).
    """
    for _ in range(num_records):
        # Generate random numbers for 'a' and 'b'
        a = Decimal(fake.random_number(digits=2))
        b = (Decimal(fake.random_number(digits=2))
            if _ % 4 !=3
            else Decimal(fake.random_number(digits=1)))

        # Randomly choose an operation
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        # Avoid division by zero for divide operation
        if operation_func == divide:  # pylint: disable=W0143
            b = Decimal('1') if b == Decimal('0') else b

        # Try to perform the operation and calculate the expected result
        try:
            expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    """
    Adds the custom command-line option to specify the number of records.
    """
    parser.addoption(
        "--num_records",
        action="store",
        default=5,
        type=int,
        help="Number of test records to generate"
    )

def pytest_generate_tests(metafunc):
    """
    Dynamically generates test data and parametrize the test functions
    that expect 'a', 'b', 'operation', and 'expected'.
    """
    # Skip dynamic parameterization for test_calculation_operations (handled explicitly)
    if metafunc.function.__name__ != 'test_calculation_operations':
        if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
            num_records = metafunc.config.getoption("num_records")
            test_data = list(generate_test_data(num_records))

            # Modify the test parameters to fit the test function's needs
            modified_parameters = [
                (a, b, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected)
                for a, b, op_name, op_func, expected in test_data
            ]

            # Split the line to avoid exceeding the character limit
            metafunc.parametrize(
                "a,b,operation,expected", modified_parameters
            )
