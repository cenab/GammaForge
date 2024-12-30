"""Advanced GEX calculations and analytics."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import norm
from scipy.optimize import bisect

from ..utils.logging import get_logger
from ..utils.formatting import format_billions
from .utils import calculate_price_bounds, get_one_year_date

logger = get_logger(__name__)


def compute_call_put_gex(df: pd.DataFrame, spot_price: float, contract_size: int = 100) -> tuple[float, float, float]:
    """
    Compute separate GEX for calls and puts.
    
    Args:
        df: DataFrame with columns ['type', 'gamma', 'open_interest']
        spot_price: Current spot price
        contract_size: Contract size (usually 100)
        
    Returns:
        Tuple of (call_gex, put_gex, total_gex)
    """
    df = df.copy()
    df['GEX'] = spot_price * df['gamma'] * df['open_interest'] * contract_size * spot_price * 0.01
    
    # Invert puts
    df.loc[df['type'] == 'P', 'GEX'] *= -1
    
    call_gex = df[df['type'] == 'C']['GEX'].sum()
    put_gex = df[df['type'] == 'P']['GEX'].sum()
    total_gex = call_gex + put_gex
    
    return call_gex, put_gex, total_gex


def compute_gex_by_moneyness(df: pd.DataFrame, spot_price: float, bins: list[float] = None) -> pd.Series:
    """
    Group GEX by strike/spot moneyness.
    
    Args:
        df: DataFrame with columns ['strike', 'GEX']
        spot_price: Current spot price
        bins: Optional list of moneyness levels
        
    Returns:
        Series of GEX grouped by moneyness bins
    """
    if bins is None:
        bins = [0.8, 0.9, 1.0, 1.1, 1.2]
    
    df = df.copy()
    df['moneyness'] = df['strike'] / spot_price
    df['moneyness_bin'] = pd.cut(df['moneyness'], bins=bins)
    
    return df.groupby('moneyness_bin')['GEX'].sum()


def compute_cumulative_gex(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative GEX distribution by strike.
    
    Args:
        df: DataFrame with columns ['strike', 'GEX']
        
    Returns:
        DataFrame with columns ['strike', 'GEX', 'cum_gex']
    """
    df = df[['strike', 'GEX']].copy()
    df = df.groupby('strike')['GEX'].sum().reset_index()
    df.sort_values('strike', inplace=True)
    df['cum_gex'] = df['GEX'].cumsum()
    
    return df


def find_zero_gamma(df: pd.DataFrame, spot_price: float, bounds_pct: tuple[float, float] = (0.8, 1.2)) -> float:
    """
    Find the spot price where net gamma is zero.
    
    Args:
        df: DataFrame with option data
        spot_price: Current spot price
        bounds_pct: Tuple of (lower_bound_pct, upper_bound_pct)
        
    Returns:
        Spot price where net gamma is zero, or None if not found
    """
    lower_bound = spot_price * bounds_pct[0]
    upper_bound = spot_price * bounds_pct[1]
    
    def net_gamma_at_spot(spot: float) -> float:
        df_copy = df.copy()
        df_copy['GEX'] = spot * df_copy['gamma'] * df_copy['open_interest'] * 100 * spot * 0.01
        df_copy.loc[df_copy['type'] == 'P', 'GEX'] *= -1
        return df_copy['GEX'].sum()
    
    try:
        f_low = net_gamma_at_spot(lower_bound)
        f_high = net_gamma_at_spot(upper_bound)
        
        if f_low * f_high > 0:
            logger.warning("No zero gamma point found in the specified range")
            return None
        
        return bisect(net_gamma_at_spot, lower_bound, upper_bound)
    except Exception as e:
        logger.error(f"Error finding zero gamma point: {str(e)}")
        return None


def compute_weighted_metrics(df: pd.DataFrame) -> dict:
    """
    Compute various weighted metrics based on GEX.
    
    Args:
        df: DataFrame with columns ['GEX', 'expiration', 'strike']
        
    Returns:
        Dictionary of weighted metrics
    """
    df = df.copy()
    df['abs_gex'] = df['GEX'].abs()
    total_abs_gex = df['abs_gex'].sum()
    
    if total_abs_gex == 0:
        return {
            'weighted_strike': 0,
            'weighted_expiry_days': 0
        }
    
    # Weighted average strike
    weighted_strike = (df['strike'] * df['abs_gex']).sum() / total_abs_gex
    
    # Weighted average expiry
    today = datetime.now()
    df['days_to_exp'] = (df['expiration'] - today).dt.days.clip(lower=0)
    weighted_expiry = (df['days_to_exp'] * df['abs_gex']).sum() / total_abs_gex
    
    return {
        'weighted_strike': weighted_strike,
        'weighted_expiry_days': weighted_expiry
    } 