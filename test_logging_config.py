"""
Test logging configuration for the FastAPI Calculator Application.

This module provides logging configuration specifically for testing environments,
with minimal output to avoid cluttering test results while still capturing
important errors and warnings.
"""

import logging
import sys
from logging_config import setup_logging


def setup_test_logging():
    """
    Set up logging for testing environment.
    
    Configures minimal logging to avoid cluttering test output while
    still capturing errors and warnings for debugging purposes.
    
    Returns:
    --------
    logging.Logger
        The configured root logger for testing.
    """
    # Set up minimal logging for tests
    logger = setup_logging(
        log_level="WARNING",  # Only show warnings and errors
        log_file=None,        # No file logging during tests
        enable_colors=False   # No colors in test output
    )
    
    # Suppress specific noisy loggers during tests
    logging.getLogger('uvicorn').setLevel(logging.ERROR)
    logging.getLogger('uvicorn.access').setLevel(logging.ERROR)
    logging.getLogger('fastapi').setLevel(logging.ERROR)
    logging.getLogger('httpx').setLevel(logging.ERROR)
    
    return logger


def setup_integration_test_logging():
    """
    Set up logging for integration tests.
    
    Provides more verbose logging than unit tests to help debug
    API integration issues while still being manageable.
    
    Returns:
    --------
    logging.Logger
        The configured root logger for integration testing.
    """
    logger = setup_logging(
        log_level="INFO",
        log_file=None,
        enable_colors=False
    )
    
    # Keep API-related logging for integration tests
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('fastapi').setLevel(logging.INFO)
    
    return logger


def setup_e2e_test_logging():
    """
    Set up logging for end-to-end tests.
    
    Provides comprehensive logging for E2E tests to help debug
    browser automation and full application flow issues.
    
    Returns:
    --------
    logging.Logger
        The configured root logger for E2E testing.
    """
    logger = setup_logging(
        log_level="INFO",
        log_file="logs/e2e_test.log",  # Log E2E tests to file
        enable_colors=False
    )
    
    # Enable detailed logging for E2E debugging
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.INFO)
    logging.getLogger('fastapi').setLevel(logging.INFO)
    
    return logger
