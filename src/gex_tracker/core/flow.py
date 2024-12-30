"""Option flow and open interest tracking functionality."""

import pandas as pd
import numpy as np
from datetime import datetime

from ..utils.logging import get_logger

logger = get_logger(__name__)


def compare_oi_changes(
    df_today: pd.DataFrame,
    df_yesterday: pd.DataFrame,
    option_key: list[str] = ['type', 'strike', 'expiration']
) -> pd.DataFrame:
    """
    Compare open interest changes between two days.
    
    Args:
        df_today: Today's option data
        df_yesterday: Yesterday's option data
        option_key: Columns to identify unique options
        
    Returns:
        DataFrame with OI changes
    """
    # Create unique option identifier
    def create_key(df):
        return df[option_key].astype(str).agg('_'.join, axis=1)
    
    df_today = df_today.copy()
    df_yesterday = df_yesterday.copy()
    
    df_today['option_key'] = create_key(df_today)
    df_yesterday['option_key'] = create_key(df_yesterday)
    
    # Merge and calculate changes
    merged = pd.merge(
        df_today[['option_key', 'open_interest', 'GEX']],
        df_yesterday[['option_key', 'open_interest']],
        on='option_key',
        how='outer',
        suffixes=('_today', '_yday')
    )
    
    # Fill NaN with 0 for new or expired options
    merged = merged.fillna({
        'open_interest_today': 0,
        'open_interest_yday': 0,
        'GEX': 0
    })
    
    # Calculate changes
    merged['oi_change'] = merged['open_interest_today'] - merged['open_interest_yday']
    merged['oi_change_pct'] = (
        merged['oi_change'] / merged['open_interest_yday'].replace(0, 1)
    ) * 100
    
    return merged


def analyze_volume_vs_oi(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """
    Analyze volume relative to open interest.
    
    Args:
        df: DataFrame with option data
        threshold: Threshold for unusual volume
        
    Returns:
        DataFrame with volume analysis
    """
    df = df.copy()
    
    # Calculate volume to OI ratio
    df['volume_to_oi'] = df['volume'] / df['open_interest'].replace(0, 1)
    
    # Mark unusual volume
    df['is_unusual_volume'] = df['volume_to_oi'] > threshold
    
    # Group by strike and type
    grouped = df.groupby(['strike', 'type']).agg({
        'volume': 'sum',
        'open_interest': 'sum',
        'volume_to_oi': 'mean',
        'is_unusual_volume': 'any',
        'GEX': 'sum'
    }).reset_index()
    
    return grouped


def track_large_trades(
    df: pd.DataFrame,
    min_volume: int = 100,
    min_notional: float = 1e6
) -> pd.DataFrame:
    """
    Track large individual trades.
    
    Args:
        df: DataFrame with option data
        min_volume: Minimum volume to consider
        min_notional: Minimum notional value
        
    Returns:
        DataFrame with large trades
    """
    df = df.copy()
    
    # Calculate notional value (rough approximation)
    df['notional'] = df['volume'] * df['strike'] * 100  # 100 shares per contract
    
    # Filter for large trades
    large_trades = df[
        (df['volume'] >= min_volume) &
        (df['notional'] >= min_notional)
    ].copy()
    
    # Sort by notional value
    large_trades = large_trades.sort_values('notional', ascending=False)
    
    return large_trades


def aggregate_flow_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate aggregate flow metrics.
    
    Args:
        df: DataFrame with option data
        
    Returns:
        Dictionary of flow metrics
    """
    metrics = {
        'total_volume': df['volume'].sum(),
        'total_oi': df['open_interest'].sum(),
        'volume_to_oi_ratio': df['volume'].sum() / df['open_interest'].sum(),
        'call_volume': df[df['type'] == 'C']['volume'].sum(),
        'put_volume': df[df['type'] == 'P']['volume'].sum(),
        'call_oi': df[df['type'] == 'C']['open_interest'].sum(),
        'put_oi': df[df['type'] == 'P']['open_interest'].sum(),
        'pct_calls': 0.0,
        'pct_puts': 0.0
    }
    
    total_volume = metrics['call_volume'] + metrics['put_volume']
    if total_volume > 0:
        metrics['pct_calls'] = (metrics['call_volume'] / total_volume) * 100
        metrics['pct_puts'] = (metrics['put_volume'] / total_volume) * 100
    
    return metrics 