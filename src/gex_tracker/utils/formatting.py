"""Formatting utilities for GEX Tracker."""

from typing import Union


def format_billions(value: float, precision: int = 2) -> str:
    """
    Format a number in billions with specified precision.
    
    Args:
        value: Number to format.
        precision: Number of decimal places.
        
    Returns:
        Formatted string with B suffix.
    """
    return f"${value / 1e9:.{precision}f}B"


def format_millions(value: float, precision: int = 2) -> str:
    """
    Format a number in millions with specified precision.
    
    Args:
        value: Number to format.
        precision: Number of decimal places.
        
    Returns:
        Formatted string with M suffix.
    """
    return f"${value / 1e6:.{precision}f}M"


def format_percentage(value: float, precision: int = 2) -> str:
    """
    Format a number as a percentage with specified precision.
    
    Args:
        value: Number to format (0.1 = 10%).
        precision: Number of decimal places.
        
    Returns:
        Formatted percentage string.
    """
    return f"{value * 100:.{precision}f}%"


def format_currency(
    value: float,
    precision: int = 2,
    auto_scale: bool = True
) -> str:
    """
    Format a number as currency with automatic scaling.
    
    Args:
        value: Number to format.
        precision: Number of decimal places.
        auto_scale: Whether to automatically choose B/M suffix.
        
    Returns:
        Formatted currency string.
    """
    abs_value = abs(value)
    if auto_scale:
        if abs_value >= 1e9:
            return format_billions(value, precision)
        elif abs_value >= 1e6:
            return format_millions(value, precision)
            
    return f"${value:,.{precision}f}"


def format_number(
    value: Union[int, float],
    precision: int = 2,
    use_commas: bool = True
) -> str:
    """
    Format a number with optional comma separators.
    
    Args:
        value: Number to format.
        precision: Number of decimal places for floats.
        use_commas: Whether to use comma separators.
        
    Returns:
        Formatted number string.
    """
    if isinstance(value, int):
        return f"{value:,d}" if use_commas else str(value)
    else:
        format_str = f"{{:,.{precision}f}}" if use_commas else f"{{:.{precision}f}}"
        return format_str.format(value) 