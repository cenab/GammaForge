"""Logging utilities for GEX Tracker."""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level.
        log_file: Optional file to write logs to.
        log_format: Optional custom log format.
    """
    if log_format is None:
        log_format = '[%(asctime)s] %(levelname)s - %(message)s'
        
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
        
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get logger with specified name.
    
    Args:
        name: Logger name.
        
    Returns:
        Logger instance.
    """
    return logging.getLogger(name)


def log_error(logger: logging.Logger, error: Exception, message: str) -> None:
    """
    Log error with exception details.
    
    Args:
        logger: Logger instance.
        error: Exception to log.
        message: Error message.
    """
    logger.error(f"{message}: {str(error)}")
    logger.debug("Exception details:", exc_info=True)


def log_warning(logger: logging.Logger, message: str) -> None:
    """
    Log warning message.
    
    Args:
        logger: Logger instance.
        message: Warning message.
    """
    logger.warning(message)


def log_info(logger: logging.Logger, message: str) -> None:
    """
    Log info message.
    
    Args:
        logger: Logger instance.
        message: Info message.
    """
    logger.info(message)


def log_debug(logger: logging.Logger, message: str) -> None:
    """
    Log debug message.
    
    Args:
        logger: Logger instance.
        message: Debug message.
    """
    logger.debug(message) 