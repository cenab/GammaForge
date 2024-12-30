"""Logging configuration for GEX Tracker."""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import DATA_DIR

# Create logs directory
LOGS_DIR = DATA_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Default format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with the specified configuration.
    
    Args:
        name: Name of the logger.
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_file: Optional file path for logging output.
        format_string: Optional custom format string.
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Use custom or default format
    formatter = logging.Formatter(format_string or DEFAULT_FORMAT)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_path = LOGS_DIR / log_file
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one with default settings.
    
    Args:
        name: Name of the logger.
        
    Returns:
        Logger instance.
    """
    logger = logging.getLogger(name)
    
    # If logger doesn't have handlers, set up with defaults
    if not logger.handlers:
        return setup_logger(name)
        
    return logger 