# app/operations.py

"""
Module: operations.py

This module contains basic arithmetic functions that perform addition, subtraction,
multiplication, and division of two numbers. These functions are foundational for
building more complex applications, such as calculators or financial tools.

Functions:
- add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the sum of a and b.
- subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the difference when b is subtracted from a.
- multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the product of a and b.
- divide(a: Union[int, float], b: Union[int, float]) -> float: Returns the quotient when a is divided by b. Raises ValueError if b is zero.

Usage:
These functions can be imported and used in other modules or integrated into APIs
to perform arithmetic operations based on user input.
"""

from typing import Union  # Import Union for type hinting multiple possible types
import logging

# Setup logger for operations module
logger = logging.getLogger(__name__)

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """
    Add two numbers and return the result.

    Parameters:
    - a (int or float): The first number to add.
    - b (int or float): The second number to add.

    Returns:
    - int or float: The sum of a and b.

    Example:
    >>> add(2, 3)
    5
    >>> add(2.5, 3)
    5.5
    """
    logger.debug(f"Adding {a} + {b}")
    try:
        # Perform addition of a and b
        result = a + b
        logger.info(f"Addition successful: {a} + {b} = {result}")
        return result
    except Exception as e:  # pragma: no cover
        logger.error(f"Addition failed for {a} + {b}: {str(e)}")    # pragma: no cover
        raise   # pragma: no cover

def subtract(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first and return the result.

    Parameters:
    - a (int or float): The number from which to subtract.
    - b (int or float): The number to subtract.

    Returns:
    - int or float: The difference between a and b.

    Example:
    >>> subtract(5, 3)
    2
    >>> subtract(5.5, 2)
    3.5
    """
    logger.debug(f"Subtracting {a} - {b}")
    try:
        # Perform subtraction of b from a
        result = a - b
        logger.info(f"Subtraction successful: {a} - {b} = {result}")
        return result
    except Exception as e:  # pragma: no cover
        logger.error(f"Subtraction failed for {a} - {b}: {str(e)}")  # pragma: no cover
        raise  # pragma: no cover

def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers and return the product.

    Parameters:
    - a (int or float): The first number to multiply.
    - b (int or float): The second number to multiply.

    Returns:
    - int or float: The product of a and b.

    Example:
    >>> multiply(2, 3)
    6
    >>> multiply(2.5, 4)
    10.0
    """
    logger.debug(f"Multiplying {a} * {b}")
    try:
        # Perform multiplication of a and b
        result = a * b
        logger.info(f"Multiplication successful: {a} * {b} = {result}")
        return result
    except Exception as e:  # pragma: no cover
        logger.error(f"Multiplication failed for {a} * {b}: {str(e)}")  # pragma: no cover
        raise  # pragma: no cover

def divide(a: Number, b: Number) -> float:
    """
    Divide the first number by the second and return the quotient.

    Parameters:
    - a (int or float): The dividend.
    - b (int or float): The divisor.

    Returns:
    - float: The quotient of a divided by b.

    Raises:
    - ValueError: If b is zero, as division by zero is undefined.

    Example:
    >>> divide(6, 3)
    2.0
    >>> divide(5.5, 2)
    2.75
    >>> divide(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero!
    """
    logger.debug(f"Dividing {a} / {b}")
    try:
        # Check if the divisor is zero to prevent division by zero
        if b == 0:
            logger.error(f"Division by zero attempted: {a} / {b}")
            # Raise a ValueError with a descriptive message
            raise ValueError("Cannot divide by zero!")
        
        # Perform division of a by b and return the result as a float
        result = a / b
        logger.info(f"Division successful: {a} / {b} = {result}")
        return result
    except ValueError as ve:
        logger.error(f"Division by zero error: {str(ve)}")
        raise  # pragma: no cover
    except Exception as e:  # pragma: no cover
        logger.error(f"Division failed for {a} / {b}: {str(e)}")
        raise  # pragma: no cover
