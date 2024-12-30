"""Core utility functions for GEX calculations."""

from datetime import datetime, timedelta


def calculate_price_bounds(spot_price: float, percentage: float = 0.15) -> tuple[float, float]:
    """
    Calculate upper and lower price bounds based on spot price.
    
    Args:
        spot_price: Current spot price
        percentage: Percentage range (default 15%)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    lower_bound = spot_price * (1 - percentage)
    upper_bound = spot_price * (1 + percentage)
    return lower_bound, upper_bound


def get_one_year_date() -> datetime:
    """Get date one year from today."""
    return datetime.now() + timedelta(days=365) 