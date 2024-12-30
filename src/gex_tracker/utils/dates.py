"""Date utilities for GEX Tracker."""

from datetime import datetime, timedelta
from typing import Optional, Union, List

import pandas as pd


def get_market_days_between(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    include_start: bool = True,
    include_end: bool = True
) -> List[datetime]:
    """
    Get list of market days between start and end dates.
    
    Args:
        start_date: Start date.
        end_date: End date.
        include_start: Whether to include start date.
        include_end: Whether to include end date.
        
    Returns:
        List of market days.
    """
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
        
    market_days = pd.date_range(
        start=start_date,
        end=end_date,
        freq='B'  # Business days
    )
    
    if not include_start:
        market_days = market_days[1:]
    if not include_end:
        market_days = market_days[:-1]
        
    return market_days.tolist()


def get_next_market_day(
    date: Optional[Union[str, datetime]] = None
) -> datetime:
    """
    Get next market day after given date.
    
    Args:
        date: Reference date, defaults to today.
        
    Returns:
        Next market day.
    """
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = pd.to_datetime(date)
        
    next_day = date + timedelta(days=1)
    while next_day.weekday() in (5, 6):  # Skip weekends
        next_day += timedelta(days=1)
        
    return next_day


def get_previous_market_day(
    date: Optional[Union[str, datetime]] = None
) -> datetime:
    """
    Get previous market day before given date.
    
    Args:
        date: Reference date, defaults to today.
        
    Returns:
        Previous market day.
    """
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = pd.to_datetime(date)
        
    prev_day = date - timedelta(days=1)
    while prev_day.weekday() in (5, 6):  # Skip weekends
        prev_day -= timedelta(days=1)
        
    return prev_day


def get_market_days_ahead(
    days: int,
    start_date: Optional[Union[str, datetime]] = None
) -> List[datetime]:
    """
    Get list of market days ahead of start date.
    
    Args:
        days: Number of market days ahead.
        start_date: Start date, defaults to today.
        
    Returns:
        List of market days.
    """
    if start_date is None:
        start_date = datetime.now()
    elif isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
        
    end_date = start_date + timedelta(days=days * 2)  # Approximate to account for weekends
    market_days = get_market_days_between(start_date, end_date)
    
    return market_days[:days]


def get_market_days_behind(
    days: int,
    end_date: Optional[Union[str, datetime]] = None
) -> List[datetime]:
    """
    Get list of market days behind end date.
    
    Args:
        days: Number of market days behind.
        end_date: End date, defaults to today.
        
    Returns:
        List of market days.
    """
    if end_date is None:
        end_date = datetime.now()
    elif isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
        
    start_date = end_date - timedelta(days=days * 2)  # Approximate to account for weekends
    market_days = get_market_days_between(start_date, end_date)
    
    return market_days[-days:] 