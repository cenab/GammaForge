"""Utility functions for visualization."""

import matplotlib.pyplot as plt
from ..utils.formatting import format_billions as fmt_billions
from .config import PLOT_STYLES, DARK_THEME, LIGHT_THEME

def setup_plot_style(dark_mode: bool = True) -> None:
    """
    Set up the plot style for matplotlib.
    
    Args:
        dark_mode: Whether to use dark mode theme.
    """
    # Apply base styles
    plt.style.use('seaborn-darkgrid')
    plt.rcParams.update(PLOT_STYLES)
    
    # Apply theme
    theme = DARK_THEME if dark_mode else LIGHT_THEME
    plt.rcParams.update(theme)

def format_billions(value: float) -> str:
    """
    Format a number in billions with B suffix.
    Wrapper around the main formatting utility.
    
    Args:
        value: Number to format.
        
    Returns:
        Formatted string.
    """
    return fmt_billions(value)

def create_figure(figsize: tuple = None) -> tuple:
    """
    Create a new figure and axis with the current style.
    
    Args:
        figsize: Optional figure size tuple (width, height).
        
    Returns:
        Tuple of (figure, axis).
    """
    if figsize is None:
        figsize = PLOT_STYLES['figure.figsize']
    
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax

def save_figure(fig, filename: str, dpi: int = None) -> None:
    """
    Save a figure to file with proper settings.
    
    Args:
        fig: matplotlib Figure object.
        filename: Output filename.
        dpi: Optional DPI setting.
    """
    if dpi is None:
        dpi = PLOT_STYLES['figure.dpi']
    
    fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor=fig.get_facecolor()) 