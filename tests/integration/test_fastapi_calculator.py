# tests/integration/test_fastapi_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from fastapi.testclient import TestClient  # Import TestClient for simulating API requests
from main import app  # Import the FastAPI app instance from your main application file

# ---------------------------------------------
# Pytest Fixture: client
# ---------------------------------------------

@pytest.fixture
def client():
    """
    Pytest Fixture to create a TestClient for the FastAPI application.

    This fixture initializes a TestClient instance that can be used to simulate
    requests to the FastAPI application without running a live server. The client
    is yielded to the test functions and properly closed after the tests complete.

    Benefits:
    - Speeds up testing by avoiding the overhead of running a server.
    - Allows for testing API endpoints in isolation.
    """
    with TestClient(app) as client:
        yield client  # Provide the TestClient instance to the test functions

# ---------------------------------------------
# Parametrized Test Function: test_add_api
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (-2, -3, -5),
        (2.5, 3.5, 6.0),
        (-2.5, 3.5, 1.0),
        (0, 0, 0),
        (1000000000, 2000000000, 3000000000),
        (-1000000000, -2000000000, -3000000000),
        (0.1, 0.2, 0.3),
        (0.7, 0.1, 0.8),
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
def test_add_api(client, a, b, expected):
    """
    Test the Addition API Endpoint with various edge cases.

    This test verifies that the `/add` endpoint correctly adds two numbers provided
    in the JSON payload and returns the expected result for various scenarios including
    large numbers and decimal precision.

    Steps:
    1. Send a POST request to the `/add` endpoint with JSON data.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result.
    """
    # Send a POST request to the '/add' endpoint with JSON payload
    response = client.post('/add', json={'a': a, 'b': b})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value with tolerance for floating point
    actual = response.json()['result']
    assert actual == expected or abs(actual - expected) < 1e-10, \
        f"Expected result {expected}, got {actual}"

# ---------------------------------------------
# Parametrized Test Function: test_subtract_api
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),
        (-5, -3, -2),
        (5.5, 2.5, 3.0),
        (-5.5, -2.5, -3.0),
        (0, 0, 0),
        (1000000000000, 500000000000, 500000000000),
        (-1000000000000, -500000000000, -500000000000),
        (0.123456789, 0.023456789, 0.1),
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
def test_subtract_api(client, a, b, expected):
    """
    Test the Subtraction API Endpoint with various edge cases.

    This test verifies that the `/subtract` endpoint correctly subtracts the second number
    from the first number provided in the JSON payload and returns the expected result for
    various scenarios including large numbers and precision.

    Steps:
    1. Send a POST request to the `/subtract` endpoint with JSON data.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result.
    """
    # Send a POST request to the '/subtract' endpoint with JSON payload
    response = client.post('/subtract', json={'a': a, 'b': b})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value with tolerance for floating point
    actual = response.json()['result']
    assert actual == expected or abs(actual - expected) < 1e-10, \
        f"Expected result {expected}, got {actual}"

# ---------------------------------------------
# Parametrized Test Function: test_multiply_api
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (-2, 3, -6),
        (2.5, 4.0, 10.0),
        (-2.5, 4.0, -10.0),
        (0, 5, 0),
        (999999999999, 2, 1999999999998),
        (-999999999999, 2, -1999999999998),
        (0.123456789, 0.987654321, 0.1219326311115269),
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
def test_multiply_api(client, a, b, expected):
    """
    Test the Multiplication API Endpoint with various edge cases.

    This test verifies that the `/multiply` endpoint correctly multiplies two numbers
    provided in the JSON payload and returns the expected result for various scenarios
    including large numbers and precision.

    Steps:
    1. Send a POST request to the `/multiply` endpoint with JSON data.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result.
    """
    # Send a POST request to the '/multiply' endpoint with JSON payload
    response = client.post('/multiply', json={'a': a, 'b': b})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value with tolerance for floating point
    actual = response.json()['result']
    assert actual == expected or abs(actual - expected) < abs(expected) * 1e-10, \
        f"Expected result {expected}, got {actual}"

# ---------------------------------------------
# Parametrized Test Function: test_divide_api
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),
        (-6, 3, -2.0),
        (6.0, 3.0, 2.0),
        (-6.0, 3.0, -2.0),
        (0, 5, 0.0),
        (1000000000, 1000000, 1000.0),
        (1.0, 10.0, 0.1),
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
def test_divide_api(client, a, b, expected):
    """
    Test the Division API Endpoint with various edge cases.

    This test verifies that the `/divide` endpoint correctly divides the first number
    by the second number provided in the JSON payload and returns the expected result
    for various scenarios including large numbers.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result.
    """
    # Send a POST request to the '/divide' endpoint with JSON payload
    response = client.post('/divide', json={'a': a, 'b': b})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value with tolerance for floating point
    actual = response.json()['result']
    assert actual == expected or abs(actual - expected) < abs(expected) * 1e-10, \
        f"Expected result {expected}, got {actual}"

# ---------------------------------------------
# Parametrized Test Function: test_divide_by_zero_api
# ---------------------------------------------

@pytest.mark.parametrize(
    "a, b",
    [
        (10, 0),
        (100, 0.0),
        (-50, -0.0),
    ],
    ids=[
        "divide_int_by_zero",
        "divide_by_float_zero",
        "divide_by_neg_float_zero",
    ]
)
def test_divide_by_zero_api(client, a, b):
    """
    Test the Division by Zero API Endpoint with various zero representations.

    This test verifies that the `/divide` endpoint correctly handles division by zero
    by returning an appropriate error message and status code for different zero representations.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data attempting division by zero.
    2. Assert that the response status code is `400 Bad Request`.
    3. Assert that the JSON response contains an 'error' field with the message "Cannot divide by zero!".
    """
    # Send a POST request to the '/divide' endpoint with JSON payload attempting division by zero
    response = client.post('/divide', json={'a': a, 'b': b})
    
    # Assert that the response status code is 400 (Bad Request), indicating an error occurred
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    
    # Assert that the JSON response contains an 'error' field
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"
    
    # Assert that the 'error' field contains the correct error message
    assert "Cannot divide by zero!" in response.json()['error'], \
        f"Expected error message 'Cannot divide by zero!', got '{response.json()['error']}'"
