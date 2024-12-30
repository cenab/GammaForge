"""Data models for GEX analysis."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class OptionData:
    """Container for option data."""
    
    ticker: str
    spot_price: float
    expiration: datetime
    strike: float
    option_type: str  # 'C' for call, 'P' for put
    gamma: float
    open_interest: int
    volume: int
    iv: Optional[float] = None


@dataclass
class GEXResult:
    """Container for GEX calculation results."""
    
    total_gex: float
    call_gex: float
    put_gex: float
    by_strike: pd.Series
    by_expiry: pd.Series
    weighted_expiry: float
    flip_points: List[float]
    dominant_expiry: datetime


@dataclass
class HistoricalGEX:
    """Container for historical GEX data."""
    
    date: datetime
    total_gex: float
    call_gex: float
    put_gex: float
    spot_price: float
    weighted_expiry: float
    correlation: Optional[float] = None
    percentiles: Optional[Dict[float, float]] = None


@dataclass
class GEXSurface:
    """Container for GEX surface data."""
    
    strikes: List[float]
    expiries: List[datetime]
    values: pd.DataFrame  # DataFrame with strikes as index and expiries as columns
    spot_price: float 