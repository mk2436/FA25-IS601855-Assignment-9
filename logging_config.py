"""
Logging configuration for the FastAPI Calculator Application.

This module provides centralized logging configuration that can be imported
and used across the application. It sets up different log levels for different
environments and provides structured logging capabilities.
"""

import logging
import logging.handlers
import sys
import os
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels for better readability."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to the level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    enable_colors: bool = True
) -> logging.Logger:
    """
    Set up comprehensive logging configuration for the application.
    
    Parameters:
    -----------
    log_level : str, optional
        The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default is INFO.
    log_file : str, optional
        Path to the log file. If None, only console logging is enabled.
    max_file_size : int, optional
        Maximum size of each log file before rotation. Default is 10MB.
    backup_count : int, optional
        Number of backup files to keep. Default is 5.
    enable_colors : bool, optional
        Whether to enable colored console output. Default is True.
    
    Returns:
    --------
    logging.Logger
        The configured root logger.
    """
    # Create logs directory if it doesn't exist
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    if enable_colors:
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        # Main application log file
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Error log file
        error_log_file = log_file.replace('.log', '_error.log')
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)
    
    # Set specific logger levels
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.INFO)
    logging.getLogger('fastapi').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Parameters:
    -----------
    name : str
        The name of the logger (typically __name__).
    
    Returns:
    --------
    logging.Logger
        A logger instance configured with the application's logging settings.
    """
    return logging.getLogger(name)


# Environment-specific logging configurations
def setup_development_logging():
    """Set up logging for development environment."""
    return setup_logging(
        log_level="DEBUG",
        log_file="logs/app.log",
        enable_colors=True
    )


def setup_production_logging():
    """Set up logging for production environment."""
    return setup_logging(
        log_level="INFO",
        log_file="logs/app.log",
        enable_colors=False
    )


def setup_test_logging():
    """Set up logging for testing environment."""
    return setup_logging(
        log_level="WARNING",
        log_file=None,
        enable_colors=False
    )


# Structured logging helpers
class StructuredLogger:
    """Helper class for structured logging with context."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_operation(self, operation: str, a: float, b: float, result: float, 
                     duration_ms: Optional[float] = None):
        """Log an arithmetic operation with structured data."""
        context = {
            "operation": operation,
            "operand_a": a,
            "operand_b": b,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if duration_ms is not None:
            context["duration_ms"] = duration_ms
        
        self.logger.info(f"Operation completed: {operation}", extra=context)
    
    def log_error(self, operation: str, error: str, context: Optional[dict] = None):
        """Log an error with structured context."""
        error_context = {
            "operation": operation,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if context:
            error_context.update(context)
        
        self.logger.error(f"Operation failed: {operation} - {error}", extra=error_context)
    
    def log_request(self, method: str, path: str, client_ip: str, 
                   user_agent: Optional[str] = None):
        """Log an incoming request."""
        request_context = {
            "method": method,
            "path": path,
            "client_ip": client_ip,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if user_agent:
            request_context["user_agent"] = user_agent
        
        self.logger.info(f"Request received: {method} {path}", extra=request_context)
