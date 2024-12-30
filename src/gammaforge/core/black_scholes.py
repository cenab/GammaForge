"""Black-Scholes option pricing and Greeks calculations."""

import math
import numpy as np
from scipy.stats import norm
from typing import Dict, Union


def black_scholes_greeks(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = 'C'
) -> Dict[str, float]:
    """
    Calculate Black-Scholes option Greeks.
    
    Args:
        S: Spot price
        K: Strike price
        T: Time to expiry in years
        r: Risk-free rate (as decimal)
        sigma: Volatility (as decimal)
        option_type: 'C' for call, 'P' for put
        
    Returns:
        Dictionary of Greeks
    """
    if T <= 0:
        return {
            'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0,
            'charm': 0, 'vanna': 0, 'speed': 0, 'color': 0
        }
    
    sqrt_T = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    
    nd1 = norm.pdf(d1)
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    
    # Base Greeks
    if option_type == 'C':
        delta = Nd1
        rho = K * T * math.exp(-r*T) * Nd2
        theta = -(S * nd1 * sigma) / (2 * sqrt_T) - r * K * math.exp(-r*T) * Nd2
    else:
        delta = Nd1 - 1
        rho = -K * T * math.exp(-r*T) * norm.cdf(-d2)
        theta = -(S * nd1 * sigma) / (2 * sqrt_T) + r * K * math.exp(-r*T) * norm.cdf(-d2)
    
    gamma = nd1 / (S * sigma * sqrt_T)
    vega = S * nd1 * sqrt_T
    
    # Advanced Greeks
    charm = -nd1 * (d2 / (2 * sigma * sqrt_T))
    if option_type == 'C':
        charm -= r * K * math.exp(-r*T) * Nd2 / (S * sigma * sqrt_T)
    else:
        charm += r * K * math.exp(-r*T) * norm.cdf(-d2) / (S * sigma * sqrt_T)
    
    vanna = -nd1 * d2 / sigma  # Alternative: vega * (1 - d1/(sigma * sqrt_T))
    speed = -gamma * (d1 / (sigma * sqrt_T) + 1) / S
    color = -gamma * (r + (d1 * sigma)/(2 * sqrt_T) + (2*r + sigma**2)/(2*sigma)) / (2*T)
    
    return {
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega,
        'rho': rho,
        'charm': charm,
        'vanna': vanna,
        'speed': speed,
        'color': color
    }


def compute_option_greeks(
    df,
    spot_price: float,
    risk_free_rate: float = 0.01
) -> Dict[str, np.ndarray]:
    """
    Compute Greeks for a DataFrame of options.
    
    Args:
        df: DataFrame with columns ['type', 'strike', 'T', 'iv']
        spot_price: Current spot price
        risk_free_rate: Risk-free rate (default 0.01)
        
    Returns:
        Dictionary of Greek arrays
    """
    results = {
        'delta': np.zeros(len(df)),
        'gamma': np.zeros(len(df)),
        'theta': np.zeros(len(df)),
        'vega': np.zeros(len(df)),
        'charm': np.zeros(len(df)),
        'vanna': np.zeros(len(df)),
        'speed': np.zeros(len(df)),
        'color': np.zeros(len(df))
    }
    
    for i, row in df.iterrows():
        greeks = black_scholes_greeks(
            S=spot_price,
            K=row['strike'],
            T=row['T'],
            r=risk_free_rate,
            sigma=row['iv'],
            option_type=row['type']
        )
        
        for greek, value in greeks.items():
            results[greek][i] = value
    
    return results 