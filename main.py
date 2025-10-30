# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator  # Use @validator for Pydantic 1.x
from fastapi.exceptions import RequestValidationError
from app.operations import add, subtract, multiply, divide  # Ensure correct import path
import uvicorn
import logging
import sys
from datetime import datetime
import json
from app.logger_module import setup_logging, get_logger, StructuredLogger

# Configure comprehensive logging
logger = setup_logging(
    log_level="INFO",
    log_file="logs/app.log",
    enable_colors=True
)
structured_logger = StructuredLogger(logger)

logger.info("FastAPI Calculator Application starting up...")

app = FastAPI()

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all incoming requests."""
    start_time = datetime.utcnow()
    
    # Log the incoming request
    client_ip = request.client.host if request.client else 'unknown'
    user_agent = request.headers.get('user-agent', 'unknown')
    structured_logger.log_request(request.method, str(request.url.path), client_ip, user_agent)
    
    # Process the request
    response = await call_next(request)
    
    # Log the response
    process_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    logger.info(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}ms")
    
    return response

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Pydantic model for request data
class OperationRequest(BaseModel):
    """
    Request model for calculator operations.
    
    This Pydantic model validates and structures the input data for arithmetic operations.
    It ensures that both operands are valid numbers (integers or floats) before processing.
    
    Attributes:
    -----------
    a : float
        The first number (operand) for the operation.
        Can be an integer or floating-point number.
    b : float
        The second number (operand) for the operation.
        Can be an integer or floating-point number.
    
    Validators:
    -----------
    validate_numbers(cls, value)
        Validates that both a and b are numeric values.
        Raises ValueError if either value is not a number.
    
    Examples:
    ---------
    Valid request:
    >>> request = OperationRequest(a=10, b=5)
    
    Valid with floats:
    >>> request = OperationRequest(a=2.5, b=3.7)
    
    Raises ValueError:
    >>> OperationRequest(a="not a number", b=5)
    ValueError: Both a and b must be numbers.
    
    Notes:
    ------
    - Both fields are required (Field(...))
    - Accepts both integers and floats
    - Validation ensures type safety before operations
    """
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')  # Correct decorator for Pydantic 1.x
    def validate_numbers(cls, value):
        """
        Validate that input values are numeric.
        
        Parameters:
        -----------
        value : Any
            The value to validate, which should be an integer or float.
        
        Returns:
        --------
        int or float
            The validated numeric value.
        
        Raises:
        -------
        ValueError
            If the value is not an integer or float.
        """
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    """
    Response model for successful calculator operations.
    
    This Pydantic model structures the response data returned to clients after a
    successful arithmetic operation. It ensures type consistency and provides
    clear API documentation.
    
    Attributes:
    -----------
    result : float
        The computed result of the arithmetic operation.
        Always returned as a float value, even for integer operations.
    
    Examples:
    ---------
    Addition result:
    >>> response = OperationResponse(result=15.0)
    
    Division result:
    >>> response = OperationResponse(result=2.5)
    
    Notes:
    ------
    - Result is always a float for consistency
    - Format: {"result": <numeric_value>}
    - Returned by all successful calculator endpoints
    """
    result: float = Field(..., description="The result of the operation")

# Pydantic model for error response
class ErrorResponse(BaseModel):
    """
    Response model for API error responses.
    
    This Pydantic model structures error messages returned to clients when
    an operation fails due to invalid input, division by zero, or other errors.
    It provides a consistent error format across all endpoints.
    
    Attributes:
    -----------
    error : str
        A human-readable error message describing what went wrong.
        Should be clear and actionable for API consumers.
    
    Examples:
    ---------
    Division by zero error:
    >>> error = ErrorResponse(error="Cannot divide by zero!")
    
    Validation error:
    >>> error = ErrorResponse(error="a: value is not a valid number")
    
    Notes:
    ------
    - Always returned with HTTP status codes 400 or 500
    - Format: {"error": "<error_message>"}
    - Used by custom exception handlers
    """
    error: str = Field(..., description="Error message")

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions and return standardized error responses.
    
    This custom exception handler intercepts HTTPExceptions raised by the application
    and returns a JSON-formatted error response with the appropriate status code and
    error message.
    
    Parameters:
    -----------
    request : Request
        The FastAPI request object that caused the exception.
    exc : HTTPException
        The HTTP exception that was raised, containing status code and detail message.
    
    Returns:
    --------
    JSONResponse
        A JSON response containing:
        - error (str): The error message from the exception
    
    Notes:
    ------
    This handler logs all HTTPExceptions for monitoring and debugging purposes.
    """
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors and return user-friendly error messages.
    
    This custom exception handler intercepts Pydantic validation errors that occur
    when request data doesn't match the expected schema. It formats all validation
    errors into a readable message.
    
    Parameters:
    -----------
    request : Request
        The FastAPI request object that caused the validation error.
    exc : RequestValidationError
        The validation error containing details about which fields failed validation.
    
    Returns:
    --------
    JSONResponse
        A JSON response with status code 400 containing:
        - error (str): A concatenated string of all validation errors
    
    Notes:
    ------
    This handler ensures that users receive clear, actionable error messages when
    they submit invalid data to the API endpoints.
    """
    # Extracting error messages
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )

@app.get("/")
async def read_root(request: Request):
    """
    Serve the calculator homepage.
    
    This endpoint renders and returns the HTML template for the calculator interface.
    The template provides a user-friendly web interface for performing arithmetic operations.
    
    Parameters:
    -----------
    request : Request
        The FastAPI request object containing client request information.
    
    Returns:
    --------
    TemplateResponse
        A Jinja2 template response containing the rendered index.html page.
    
    Examples:
    ---------
    Visiting http://localhost:8000/ will display the calculator web interface.
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Failed to render homepage: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers together.
    
    This endpoint performs addition of two numbers. It accepts both integers and floats,
    and returns the sum. Handles large numbers and floating-point arithmetic.
    
    Parameters:
    -----------
    operation : OperationRequest
        A request object containing:
        - a (float): The first number to add
        - b (float): The second number to add
    
    Returns:
    --------
    OperationResponse
        A response object containing:
        - result (float): The sum of a and b
    
    Raises:
    -------
    HTTPException (400)
        If an error occurs during the addition operation.
    
    Examples:
    ---------
    Request: {"a": 10, "b": 5}
    Response: {"result": 15}
    
    Request: {"a": 2.5, "b": 3.7}
    Response: {"result": 6.2}
    """
    logger.info(f"Addition request: {operation.a} + {operation.b}")
    try:
        result = add(operation.a, operation.b)
        structured_logger.log_operation("add", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except Exception as e:
        structured_logger.log_error("add", str(e), {"operand_a": operation.a, "operand_b": operation.b})
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract the second number from the first number.
    
    This endpoint performs subtraction of two numbers. It accepts both integers and floats,
    and returns the difference (a - b). Handles large numbers and floating-point arithmetic.
    
    Parameters:
    -----------
    operation : OperationRequest
        A request object containing:
        - a (float): The number from which to subtract
        - b (float): The number to subtract
    
    Returns:
    --------
    OperationResponse
        A response object containing:
        - result (float): The difference of a minus b
    
    Raises:
    -------
    HTTPException (400)
        If an error occurs during the subtraction operation.
    
    Examples:
    ---------
    Request: {"a": 10, "b": 5}
    Response: {"result": 5}
    
    Request: {"a": 5.5, "b": 2.5}
    Response: {"result": 3.0}
    """
    logger.info(f"Subtraction request: {operation.a} - {operation.b}")
    try:
        result = subtract(operation.a, operation.b)
        structured_logger.log_operation("subtract", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except Exception as e:
        structured_logger.log_error("subtract", str(e), {"operand_a": operation.a, "operand_b": operation.b})
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers together.
    
    This endpoint performs multiplication of two numbers. It accepts both integers and floats,
    and returns the product. Handles large numbers and floating-point arithmetic.
    
    Parameters:
    -----------
    operation : OperationRequest
        A request object containing:
        - a (float): The first number to multiply
        - b (float): The second number to multiply
    
    Returns:
    --------
    OperationResponse
        A response object containing:
        - result (float): The product of a and b
    
    Raises:
    -------
    HTTPException (400)
        If an error occurs during the multiplication operation.
    
    Examples:
    ---------
    Request: {"a": 10, "b": 5}
    Response: {"result": 50}
    
    Request: {"a": 2.5, "b": 4}
    Response: {"result": 10.0}
    """
    logger.info(f"Multiplication request: {operation.a} * {operation.b}")
    try:
        result = multiply(operation.a, operation.b)
        structured_logger.log_operation("multiply", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except Exception as e:
        structured_logger.log_error("multiply", str(e), {"operand_a": operation.a, "operand_b": operation.b})
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide the first number by the second number.
    
    This endpoint performs division of two numbers. It accepts both integers and floats,
    and returns the quotient (a / b). Handles division by zero by returning an error.
    
    Parameters:
    -----------
    operation : OperationRequest
        A request object containing:
        - a (float): The dividend (number to be divided)
        - b (float): The divisor (number to divide by)
    
    Returns:
    --------
    OperationResponse
        A response object containing:
        - result (float): The quotient of a divided by b
    
    Raises:
    -------
    HTTPException (400)
        If the divisor is zero or an error occurs during division.
    HTTPException (500)
        If an unexpected internal server error occurs.
    
    Examples:
    ---------
    Request: {"a": 10, "b": 2}
    Response: {"result": 5.0}
    
    Request: {"a": 6.0, "b": 3.0}
    Response: {"result": 2.0}
    
    Request: {"a": 10, "b": 0}
    Response: 400 Error with "Cannot divide by zero!"
    """
    logger.info(f"Division request: {operation.a} / {operation.b}")
    try:
        result = divide(operation.a, operation.b)
        structured_logger.log_operation("divide", operation.a, operation.b, result)
        return OperationResponse(result=result)
    except ValueError as e:
        structured_logger.log_error("divide", str(e), {"operand_a": operation.a, "operand_b": operation.b})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        structured_logger.log_error("divide", str(e), {"operand_a": operation.a, "operand_b": operation.b})
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
