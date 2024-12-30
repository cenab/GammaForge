"""GEX scenario analysis functionality."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..utils.logging import get_logger
from .black_scholes import compute_option_greeks
from .utils import calculate_price_bounds

logger = get_logger(__name__)


def scenario_spot_shock(
    df: pd.DataFrame,
    spot_price: float,
    shift_pct: float = 0.05,
    contract_size: int = 100
) -> tuple[float, float]:
    """
    Calculate GEX after a spot price shock.
    
    Args:
        df: DataFrame with option data
        spot_price: Current spot price
        shift_pct: Percentage to shift spot price
        contract_size: Contract size
        
    Returns:
        Tuple of (new_spot_price, new_total_gex)
    """
    new_spot = spot_price * (1 + shift_pct)
    df_scenario = df.copy()
    
    # Recalculate GEX with new spot
    df_scenario['GEX'] = (
        new_spot *
        df_scenario['gamma'] *
        df_scenario['open_interest'] *
        contract_size *
        new_spot *
        0.01
    )
    
    # Invert puts
    df_scenario.loc[df_scenario['type'] == 'P', 'GEX'] *= -1
    
    return new_spot, df_scenario['GEX'].sum()


def scenario_vol_shock(
    df: pd.DataFrame,
    spot_price: float,
    vol_shift: float = 0.05,
    risk_free_rate: float = 0.01,
    contract_size: int = 100
) -> float:
    """
    Calculate GEX after an implied volatility shock.
    
    Args:
        df: DataFrame with option data
        spot_price: Current spot price
        vol_shift: Amount to shift implied volatility
        risk_free_rate: Risk-free rate
        contract_size: Contract size
        
    Returns:
        New total GEX
    """
    df_scenario = df.copy()
    
    # Shift implied volatility
    df_scenario['iv'] = df_scenario['iv'] + vol_shift
    
    # Recalculate Greeks with new volatility
    new_greeks = compute_option_greeks(
        df_scenario,
        spot_price,
        risk_free_rate=risk_free_rate
    )
    
    # Calculate new GEX
    df_scenario['GEX'] = (
        spot_price *
        new_greeks['gamma'] *
        df_scenario['open_interest'] *
        contract_size *
        spot_price *
        0.01
    )
    
    # Invert puts
    df_scenario.loc[df_scenario['type'] == 'P', 'GEX'] *= -1
    
    return df_scenario['GEX'].sum()


def scenario_time_decay(
    df: pd.DataFrame,
    spot_price: float,
    days_forward: int = 7,
    risk_free_rate: float = 0.01,
    contract_size: int = 100
) -> float:
    """
    Calculate GEX after time decay.
    
    Args:
        df: DataFrame with option data
        spot_price: Current spot price
        days_forward: Number of days to move forward
        risk_free_rate: Risk-free rate
        contract_size: Contract size
        
    Returns:
        New total GEX
    """
    df_scenario = df.copy()
    
    # Adjust time to expiry
    days_per_year = 365
    df_scenario['T'] = df_scenario['T'] - (days_forward / days_per_year)
    df_scenario['T'] = df_scenario['T'].clip(lower=0)
    
    # Remove expired options
    df_scenario = df_scenario[df_scenario['T'] > 0]
    
    if len(df_scenario) == 0:
        return 0.0
    
    # Recalculate Greeks with new time to expiry
    new_greeks = compute_option_greeks(
        df_scenario,
        spot_price,
        risk_free_rate=risk_free_rate
    )
    
    # Calculate new GEX
    df_scenario['GEX'] = (
        spot_price *
        new_greeks['gamma'] *
        df_scenario['open_interest'] *
        contract_size *
        spot_price *
        0.01
    )
    
    # Invert puts
    df_scenario.loc[df_scenario['type'] == 'P', 'GEX'] *= -1
    
    return df_scenario['GEX'].sum()


def scenario_all(
    df: pd.DataFrame,
    spot_price: float,
    spot_shifts: list[float] = [-0.05, 0.05],
    vol_shifts: list[float] = [-0.05, 0.05],
    time_days: list[int] = [7, 14],
    risk_free_rate: float = 0.01,
    contract_size: int = 100
) -> dict:
    """
    Run multiple scenarios and return results.
    
    Args:
        df: DataFrame with option data
        spot_price: Current spot price
        spot_shifts: List of spot price shifts
        vol_shifts: List of volatility shifts
        time_days: List of days forward
        risk_free_rate: Risk-free rate
        contract_size: Contract size
        
    Returns:
        Dictionary of scenario results
    """
    results = {
        'base_gex': df['GEX'].sum(),
        'spot_scenarios': {},
        'vol_scenarios': {},
        'time_scenarios': {}
    }
    
    # Spot price scenarios
    for shift in spot_shifts:
        new_spot, new_gex = scenario_spot_shock(
            df, spot_price, shift, contract_size
        )
        results['spot_scenarios'][f'{shift:+.1%}'] = {
            'spot': new_spot,
            'gex': new_gex
        }
    
    # Volatility scenarios
    for shift in vol_shifts:
        new_gex = scenario_vol_shock(
            df, spot_price, shift, risk_free_rate, contract_size
        )
        results['vol_scenarios'][f'{shift:+.1%}'] = new_gex
    
    # Time decay scenarios
    for days in time_days:
        new_gex = scenario_time_decay(
            df, spot_price, days, risk_free_rate, contract_size
        )
        results['time_scenarios'][f'{days}d'] = new_gex
    
    return results 