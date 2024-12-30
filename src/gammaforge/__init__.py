"""
GammaForge - A professional tool for analyzing Gamma Exposure in options markets.
"""

from .core import (
    # Models
    OptionData,
    GEXResult,
    HistoricalGEX,
    GEXSurface,
    # Calculator
    GEXCalculator,
    # Advanced GEX
    compute_call_put_gex,
    compute_gex_by_moneyness,
    compute_cumulative_gex,
    find_zero_gamma,
    compute_weighted_metrics,
    # Black-Scholes
    black_scholes_greeks,
    compute_option_greeks,
    # Scenarios
    scenario_spot_shock,
    scenario_vol_shock,
    scenario_time_decay,
    scenario_all,
    # Flow Analysis
    compare_oi_changes,
    analyze_volume_vs_oi,
    track_large_trades,
    aggregate_flow_metrics,
    # Utilities
    calculate_price_bounds,
    get_one_year_date
)

from .utils import (
    # Dates
    get_market_days_between,
    get_next_market_day,
    get_previous_market_day,
    get_market_days_ahead,
    get_market_days_behind,
    # Formatting
    format_billions,
    format_millions,
    format_percentage,
    format_currency,
    format_number,
    # Logging
    setup_logging,
    get_logger,
    log_error,
    log_warning,
    log_info,
    log_debug,
    # Plotting
    set_style,
    get_figure_size,
    get_color_palette,
    get_plot_defaults,
    apply_plot_defaults
)

__version__ = '0.1.0'
__author__ = 'Cenab Batu Bora'
__email__ = 'hello@batubora.com'

__all__ = [
    # Package info
    '__version__',
    '__author__',
    '__email__',
    # Core - Models
    'OptionData',
    'GEXResult',
    'HistoricalGEX',
    'GEXSurface',
    # Core - Calculator
    'GEXCalculator',
    # Core - Advanced GEX
    'compute_call_put_gex',
    'compute_gex_by_moneyness',
    'compute_cumulative_gex',
    'find_zero_gamma',
    'compute_weighted_metrics',
    # Core - Black-Scholes
    'black_scholes_greeks',
    'compute_option_greeks',
    # Core - Scenarios
    'scenario_spot_shock',
    'scenario_vol_shock',
    'scenario_time_decay',
    'scenario_all',
    # Core - Flow Analysis
    'compare_oi_changes',
    'analyze_volume_vs_oi',
    'track_large_trades',
    'aggregate_flow_metrics',
    # Core - Utilities
    'calculate_price_bounds',
    'get_one_year_date',
    # Utils - Dates
    'get_market_days_between',
    'get_next_market_day',
    'get_previous_market_day',
    'get_market_days_ahead',
    'get_market_days_behind',
    # Utils - Formatting
    'format_billions',
    'format_millions',
    'format_percentage',
    'format_currency',
    'format_number',
    # Utils - Logging
    'setup_logging',
    'get_logger',
    'log_error',
    'log_warning',
    'log_info',
    'log_debug',
    # Utils - Plotting
    'set_style',
    'get_figure_size',
    'get_color_palette',
    'get_plot_defaults',
    'apply_plot_defaults'
] 