# tests/e2e/test_e2e.py

import pytest  # Import the pytest framework for writing and running tests

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This test verifies that when a user navigates to the homepage of the application,
    the main header (`<h1>`) correctly displays the text "Hello World". This ensures
    that the server is running and serving the correct template.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Use an assertion to check that the text within the first <h1> tag is exactly "Hello World".
    # If the text does not match, the test will fail.
    assert page.inner_text('h1') == 'Hello World'



# ---------------------------------------------
# Parametrized E2E Tests for Calculator Operations
# ---------------------------------------------

@pytest.mark.e2e
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("2", "3", "5"),
        ("-2", "-3", "-5"),
        ("2.5", "3.5", "6.0"),
        ("-2.5", "3.5", "1.0"),
        ("0", "0", "0"),
        ("1000000000", "2000000000", "3000000000"),
        ("-1000000000", "-2000000000", "-3000000000"),
        ("0.1", "0.2", "0.3"),
        ("0.7", "0.1", "0.8"),
    ],
    ids=[
        "add_pos_integers",
        "add_neg_integers",
        "add_pos_floats",
        "add_neg_pos_float",
        "add_zeros",
        "add_large_integers",
        "add_large_neg_integers",
        "add_decimal_0.1_0.2",
        "add_decimal_0.7_0.1",
    ]
)
def test_calculator_add_parametrized(page, fastapi_server, a, b, expected):
    """
    Test the addition functionality of the calculator.

    This test simulates a user performing an addition operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Add" button, and verifies
    that the result displayed is correct.
    """
     # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    # Fill in the first number input field (with id 'a') with the value 'a'.
    page.fill('#a', a)
    # Fill in the second number input field (with id 'b') with the value 'b'.
    page.fill('#b', b)
    # Click the button that has the exact text "Add". This triggers the addition operation.
    page.click('button:text("Add")')
    
    # Wait for result to be displayed
    page.wait_for_function("document.querySelector('#result').innerText.trim() !== ''")

    # Get the text within the result div (with id 'result').
    result_text = page.inner_text('#result')
    # Extract just the number part (remove "Calculation Result: ")
    result_value = result_text.replace('Calculation Result: ', '')
    # Convert to float for comparison to handle precision
    actual = float(result_value)
    # Convert to float for comparison to handle precision
    expected_float = float(expected)
    # Use tolerance for floating point comparisons
    assert abs(actual - expected_float) < 1e-10 or actual == expected_float, \
        f"Expected {expected_float}, but got {actual}"


@pytest.mark.e2e
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("5", "3", "2"),
        ("-5", "-3", "-2"),
        ("5.5", "2.5", "3.0"),
        ("-5.5", "-2.5", "-3.0"),
        ("0", "0", "0"),
        ("1000000000000", "500000000000", "500000000000"),
        ("-1000000000000", "-500000000000", "-500000000000"),
        ("0.123456789", "0.023456789", "0.1"),
    ],
    ids=[
        "subtract_pos_integers",
        "subtract_neg_integers",
        "subtract_pos_floats",
        "subtract_neg_floats",
        "subtract_zeros",
        "subtract_large_integers",
        "subtract_large_neg_integers",
        "subtract_decimal_precision",
    ]
)
def test_calculator_subtract_parametrized(page, fastapi_server, a, b, expected):
    """
    Test the subtraction functionality of the calculator.

    This test simulates a user performing a subtraction operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Subtract" button, and verifies
    that the result displayed is correct.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    # Fill in the first number input field (with id 'a') with the value 'a'.
    page.fill('#a', a)
    # Fill in the second number input field (with id 'b') with the value 'b'.
    page.fill('#b', b)
    # Click the button that has the exact text "Subtract". This triggers the subtraction operation.
    page.click('button:text("Subtract")')
    
    # Wait for result to be displayed
    page.wait_for_function("document.querySelector('#result').innerText.trim() !== ''")
    
    # Get the text within the result div (with id 'result').
    result_text = page.inner_text('#result')
    # Extract just the number part (remove "Calculation Result: ")
    result_value = result_text.replace('Calculation Result: ', '')
    # Convert to float for comparison to handle precision
    actual = float(result_value)
    # Convert to float for comparison to handle precision
    expected_float = float(expected)
    # Use tolerance for floating point comparisons
    assert abs(actual - expected_float) < 1e-10 or actual == expected_float, \
        f"Expected {expected_float}, but got {actual}"


@pytest.mark.e2e
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("2", "3", "6"),
        ("-2", "3", "-6"),
        ("2.5", "4.0", "10.0"),
        ("-2.5", "4.0", "-10.0"),
        ("0", "5", "0"),
        ("999999999999", "2", "1999999999998"),
        ("-999999999999", "2", "-1999999999998"),
        ("0.123456789", "0.987654321", "0.1219326311115269"),
    ],
    ids=[
        "multiply_pos_integers",
        "multiply_neg_pos_integer",
        "multiply_pos_floats",
        "multiply_neg_float",
        "multiply_zero",
        "multiply_large_integers",
        "multiply_large_neg_integers",
        "multiply_decimal_precision",
    ]
)
def test_calculator_multiply_parametrized(page, fastapi_server, a, b, expected):
    """
    Test the multiplication functionality of the calculator.

    This test simulates a user performing a multiplication operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Multiply" button, and verifies
    that the result displayed is correct.   
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    # Fill in the first number input field (with id 'a') with the value 'a'.
    page.fill('#a', a)
    # Fill in the second number input field (with id 'b') with the value 'b'.
    page.fill('#b', b)
    # Click the button that has the exact text "Multiply". This triggers the multiplication operation.
    page.click('button:text("Multiply")')

    # Wait for result to be displayed
    page.wait_for_function("document.querySelector('#result').innerText.trim() !== ''")

    
    # Get the text within the result div (with id 'result').
    result_text = page.inner_text('#result')
    # Extract just the number part (remove "Calculation Result: ")
    result_value = result_text.replace('Calculation Result: ', '')
    # Convert to float for comparison to handle precision
    actual = float(result_value)
    # Convert to float for comparison to handle precision
    expected_float = float(expected)
    # Use tolerance for floating point comparisons
    
    assert abs(actual - expected_float) < abs(expected_float) * 1e-10 or actual == expected_float, \
        f"Expected {expected_float}, but got {actual}"


@pytest.mark.e2e
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("6", "3", "2.0"),
        ("-6", "3", "-2.0"),
        ("6.0", "3.0", "2.0"),
        ("-6.0", "3.0", "-2.0"),
        ("0", "5", "0.0"),
        ("1000000000", "1000000", "1000.0"),
        ("1.0", "10.0", "0.1"),
    ],
    ids=[
        "divide_pos_integers",
        "divide_neg_pos_integer",
        "divide_pos_floats",
        "divide_neg_float",
        "divide_zero_by_pos",
        "divide_large_integers",
        "divide_precise_decimal",
    ]
)
def test_calculator_divide_parametrized(page, fastapi_server, a, b, expected):
    """
    Test the division functionality of the calculator.

    This test simulates a user performing a division operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Divide" button, and verifies
    that the result displayed is correct.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    # Fill in the first number input field (with id 'a') with the value 'a'.
    page.fill('#a', a)
    # Fill in the second number input field (with id 'b') with the value 'b'.
    page.fill('#b', b)
    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')

    # Wait for result to be displayed
    page.wait_for_function("document.querySelector('#result').innerText.trim() !== ''")

    
    # Get the text within the result div (with id 'result').
    result_text = page.inner_text('#result')
    # Extract just the number part (remove "Calculation Result: ")
    result_value = result_text.replace('Calculation Result: ', '')
    # Convert to float for comparison to handle precision
    actual = float(result_value)
    # Convert to float for comparison to handle precision
    expected_float = float(expected)
    
    # Use tolerance for floating point comparisons    
    assert abs(actual - expected_float) < abs(expected_float) * 1e-10 or actual == expected_float, \
        f"Expected {expected_float}, but got {actual}"


@pytest.mark.e2e
@pytest.mark.parametrize(
    "value",
    ["0", "0.0", "-0.0"],
    ids=["int_zero", "float_zero", "neg_float_zero"]
)
def test_calculator_divide_by_zero_variations(page, fastapi_server, value):
    """
    Test the divide by zero functionality of the calculator.

    This test simulates a user attempting to divide a number by zero using the calculator.
    It fills in the numbers, clicks the "Divide" button, and verifies that the appropriate
    error message is displayed. This ensures that the application correctly handles invalid
    operations and provides meaningful feedback to the user.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    # Fill in the first number input field (with id 'a') with the value '100'.
    page.fill('#a', '100')
    # Fill in the second number input field (with id 'b') with the value 'value'.
    page.fill('#b', value)
    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')

    # Wait for result to be displayed
    page.wait_for_function("document.querySelector('#result').innerText.trim() !== ''")

    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly "Error: Cannot divide by zero!".
    # This verifies that the application correctly handles division by zero and displays the appropriate error message to the user.
    assert page.inner_text('#result') == 'Error: Cannot divide by zero!'
