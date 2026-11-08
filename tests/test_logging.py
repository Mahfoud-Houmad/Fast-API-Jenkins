import logging

from app.logging import LEVELS, get_logger


def test_get_logger_default_name():
    """Test that get_logger returns a logger with default name."""
    logger = get_logger()
    assert logger.name == "app"
    assert isinstance(logger, logging.Logger)


def test_get_logger_custom_name():
    """Test that get_logger returns a logger with custom name."""
    custom_name = "test_logger"
    logger = get_logger(custom_name)
    assert logger.name == custom_name
    assert isinstance(logger, logging.Logger)


def test_logger_has_handler():
    """Test that the logger has a StreamHandler configured."""
    logger = get_logger("test_handler")
    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_logger_level_info():
    """Test that the logger is set to INFO level by default."""
    logger = get_logger("test_level")
    assert logger.level == logging.INFO


def test_logger_formatter():
    """Test that the logger handler has the correct formatter."""
    logger = get_logger("test_formatter")
    handler = logger.handlers[0]
    formatter = handler.formatter
    assert formatter is not None
    # Test the format string contains expected components
    format_string = formatter._fmt
    assert "%(asctime)s" in format_string
    assert "%(levelname)s" in format_string
    assert "%(name)s" in format_string
    assert "%(message)s" in format_string


def test_levels_dict():
    """Test that LEVELS dictionary contains expected log levels."""
    expected_levels = {"fatal": 50, "error": 40, "warn": 30, "info": 20, "debug": 10, "trace": 5}
    assert LEVELS == expected_levels


def test_trace_level_added():
    """Test that TRACE level is properly added to logging."""
    assert logging.getLevelName(5) == "TRACE"
    assert hasattr(logging, "TRACE") or logging.getLevelName("TRACE") != "Level TRACE"


def test_logger_singleton_behavior():
    """Test that calling get_logger with same name returns same logger."""
    logger1 = get_logger("singleton_test")
    logger2 = get_logger("singleton_test")
    assert logger1 is logger2


def test_logger_no_duplicate_handlers():
    """Test that calling get_logger multiple times doesn't add duplicate handlers."""
    logger_name = "no_duplicate_handlers"
    logger1 = get_logger(logger_name)
    initial_handler_count = len(logger1.handlers)

    logger2 = get_logger(logger_name)
    final_handler_count = len(logger2.handlers)

    assert initial_handler_count == final_handler_count
    assert logger1 is logger2
