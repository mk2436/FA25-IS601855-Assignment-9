import io
import os
import logging
import pytest
from datetime import datetime

from app.logger_module import (
    setup_logging,
    setup_development_logging,
    setup_production_logging,
    setup_test_logging,
    get_logger,
    ColoredFormatter,
    StructuredLogger,
)


@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file path."""
    return str(tmp_path / "app.tests_logs.log")


@pytest.mark.parametrize(
    "log_level,log_file,enable_colors,expect_file",
    [
        ("DEBUG", None, False, False),  # console only
        ("DEBUG", "logs/test_app.log", False, True),  # with file
    ],
)
def test_setup_logging_variants(monkeypatch, tmp_path, log_level, log_file, enable_colors, expect_file):
    """Parameterized test for both console and file-based setups."""
    stream = io.StringIO()
    monkeypatch.setattr("sys.stdout", stream)

    # Ensure temp directory for file logging
    if log_file:
        log_file = str(tmp_path / "app_test.log")

    logger = setup_logging(
        log_level=log_level,
        log_file=log_file,
        enable_colors=enable_colors,
    )

    logger.info("Test message")
    output = stream.getvalue()

    assert "Test message" in output
    assert "INFO" in output

    if expect_file:
        assert os.path.exists(log_file)
        error_log = log_file.replace(".log", "_error.log")
        assert os.path.exists(error_log)
    else:
        # no log files for console-only mode
        assert not list(tmp_path.glob("*.log"))


@pytest.mark.parametrize(
    "func,expected_level",
    [
        (setup_development_logging, logging.DEBUG),
        (setup_production_logging, logging.INFO),
        (setup_test_logging, logging.WARNING),
    ],
)
def test_environment_specific_loggers(func, expected_level):
    """Check that environment helper functions set correct log levels."""
    logger = func()
    assert logger.level == expected_level


@pytest.mark.parametrize(
    "levelname,color_code",
    [
        ("DEBUG", "\033[36m"),
        ("INFO", "\033[32m"),
        ("WARNING", "\033[33m"),
        ("ERROR", "\033[31m"),
        ("CRITICAL", "\033[35m"),
    ],
)
def test_colored_formatter_colors(levelname, color_code):
    """Verify that each log level gets its correct color."""
    record = logging.LogRecord(
        name="test",
        level=getattr(logging, levelname),
        pathname="",
        lineno=1,
        msg=f"{levelname} message",
        args=(),
        exc_info=None,
    )
    formatter = ColoredFormatter("%(levelname)s: %(message)s")
    formatted = formatter.format(record)

    assert color_code in formatted
    assert f"{levelname} message" in formatted


def test_get_logger_singleton_behavior():
    """Ensure get_logger returns consistent logger instances."""
    logger1 = get_logger("my.test.logger")
    logger2 = get_logger("my.test.logger")
    assert logger1 is logger2
    assert isinstance(logger1, logging.Logger)


@pytest.mark.parametrize(
    "method,args,expected_level,expected_text",
    [
        ("log_operation", ("add", 1, 2, 3, 12.5), logging.INFO, "Operation completed: add"),
        ("log_error", ("divide", "Division by zero", {"operand_a": 1, "operand_b": 0}), logging.ERROR, "Division by zero"),
        ("log_request", ("GET", "/calc", "127.0.0.1", "pytest"), logging.INFO, "Request received: GET /calc"),
    ],
)
def test_structured_logger_methods(caplog, method, args, expected_level, expected_text):
    """Parameterized test for StructuredLogger methods."""
    base_logger = logging.getLogger(f"structured.{method}")
    structured = StructuredLogger(base_logger)

    with caplog.at_level(expected_level):
        getattr(structured, method)(*args)

    assert any(expected_text in m for m in caplog.messages)

    record = caplog.records[0]
    assert "timestamp" in record.__dict__

    # basic field checks by method type
    if method == "log_operation":
        assert record.operation == "add"
        assert record.result == 3
    elif method == "log_error":
        assert record.error == "Division by zero"
        assert record.operand_a == 1
    elif method == "log_request":
        assert record.method == "GET"
        assert record.path == "/calc"
        assert record.client_ip == "127.0.0.1"
        datetime.fromisoformat(record.timestamp)
