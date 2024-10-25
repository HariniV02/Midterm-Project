# Project Documentation for the Calculator


## Design Patterns Implementation
In this project, I utilized the **Factory Design Pattern** to manage the creation of different operation classes (add, subtract, multiply, divide). This allows for easy scalability if more operations need to be added in the future.

**Link to Implementation**: [Factory Design Pattern Implementation](https://refactoring.guru/design-patterns/factory-method)


## Environment Variables Usage
I used environment variables to manage sensitive configurations such as API keys and database URLs. This helps in keeping the code clean and secure. The `dotenv` library was employed to load these variables during the application startup.

**Link to Code**: [Environment Variables Implementation](https://pypi.org/project/python-dotenv/)


## Logging
Logging is implemented using Python's built-in `logging` module. It captures important events and errors that occur during execution, which aids in debugging and monitoring the application’s performance.

**Link to Logging Implementation**: [Logging Implementation](https://docs.python.org/3/library/logging.html)


## Exception Handling
I implemented exception handling using both the "Look Before You Leap" (LBYL) and "Easier to Ask for Forgiveness than Permission" (EAFP) paradigms:

- **LBYL**: Before performing operations that might fail (e.g., division), the code checks if the denominator is zero.
- **EAFP**: In other parts of the code, exceptions are caught and handled gracefully, allowing the program to continue running.

**Link to Exception Handling Implementation**: [Exception Handling Code](https://realpython.com/python-lbyl-vs-eafp/)


## Video Demonstration
A video demonstration of the calculator has been created to showcase its key features and functionalities. 

**Video Link**: [Calculator Demonstration Video](insert_link_to_video_here)

