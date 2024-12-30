"""
GEX Tracker - A tool for analyzing Gamma Exposure in options markets.
"""

from .core import (
    # Models
    OptionData,
    GEXResult,
    HistoricalGEX,
    GEXSurface,
    # Calculator
    GEXCalculator,
    calculate_gex,
    calculate_gex_by_strike,
    calculate_gex_by_expiry,
    calculate_gex_surface
)
from .data import (
    # Data Fetching
    fetch_option_chain,
    fetch_historical_data,
    fetch_realtime_data,
    # Cache Management
    cache_data,
    load_cached_data,
    clear_cache,
    is_cache_valid,
    # Data Processing
    process_option_data,
    process_historical_data,
    process_realtime_update
)
from .visualization import (
    # Static Plots
    plot_gex_by_strike,
    plot_gex_by_expiry,
    plot_gex_surface,
    plot_historical_gex,
    plot_gex_heatmap,
    # Interactive Plots
    create_interactive_surface,
    create_interactive_heatmap,
    create_interactive_dashboard,
    # Reporting
    generate_gex_report,
    generate_historical_report,
    generate_realtime_report
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
__author__ = 'Batu Cam'
__email__ = 'batuhan.camlica@gmail.com'

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
    'calculate_gex',
    'calculate_gex_by_strike',
    'calculate_gex_by_expiry',
    'calculate_gex_surface',
    # Data - Fetching
    'fetch_option_chain',
    'fetch_historical_data',
    'fetch_realtime_data',
    # Data - Cache
    'cache_data',
    'load_cached_data',
    'clear_cache',
    'is_cache_valid',
    # Data - Processing
    'process_option_data',
    'process_historical_data',
    'process_realtime_update',
    # Visualization - Static
    'plot_gex_by_strike',
    'plot_gex_by_expiry',
    'plot_gex_surface',
    'plot_historical_gex',
    'plot_gex_heatmap',
    # Visualization - Interactive
    'create_interactive_surface',
    'create_interactive_heatmap',
    'create_interactive_dashboard',
    # Visualization - Reporting
    'generate_gex_report',
    'generate_historical_report',
    'generate_realtime_report',
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