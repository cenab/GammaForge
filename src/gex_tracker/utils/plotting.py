"""Plotting utilities for GEX Tracker."""

from typing import Optional, Tuple, Dict, Any

import matplotlib.pyplot as plt
import seaborn as sns


def set_style(style: str = 'dark') -> None:
    """
    Set the plotting style.
    
    Args:
        style: Style name ('dark' or 'light').
    """
    if style == 'dark':
        plt.style.use('dark_background')
        sns.set_style('darkgrid')
    else:
        plt.style.use('default')
        sns.set_style('whitegrid')


def get_figure_size(
    width: float = 12,
    height: float = 6,
    aspect_ratio: Optional[float] = None
) -> Tuple[float, float]:
    """
    Get figure size with optional aspect ratio.
    
    Args:
        width: Figure width.
        height: Figure height.
        aspect_ratio: Optional aspect ratio to override height.
        
    Returns:
        Tuple of (width, height).
    """
    if aspect_ratio is not None:
        height = width / aspect_ratio
    return width, height


def get_color_palette(
    style: str = 'dark',
    n_colors: Optional[int] = None
) -> Dict[str, str]:
    """
    Get color palette for plotting.
    
    Args:
        style: Style name ('dark' or 'light').
        n_colors: Optional number of colors needed.
        
    Returns:
        Dictionary of color names and hex codes.
    """
    if style == 'dark':
        colors = {
            'primary': '#FE53BB',  # Pink
            'secondary': '#09FBD3',  # Cyan
            'positive': '#00FF00',  # Green
            'negative': '#FF0000',  # Red
            'neutral': '#808080',  # Gray
            'highlight': '#FFD700',  # Gold
            'background': '#000000',  # Black
            'text': '#FFFFFF'  # White
        }
    else:
        colors = {
            'primary': '#FF1493',  # Deep Pink
            'secondary': '#00CED1',  # Dark Turquoise
            'positive': '#008000',  # Green
            'negative': '#FF0000',  # Red
            'neutral': '#808080',  # Gray
            'highlight': '#FFD700',  # Gold
            'background': '#FFFFFF',  # White
            'text': '#000000'  # Black
        }
        
    if n_colors is not None:
        palette = sns.color_palette('husl', n_colors=n_colors)
        colors.update({f'color_{i}': f'#{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x}'
                      for i, c in enumerate(palette)})
        
    return colors


def get_plot_defaults(style: str = 'dark') -> Dict[str, Any]:
    """
    Get default plotting parameters.
    
    Args:
        style: Style name ('dark' or 'light').
        
    Returns:
        Dictionary of default parameters.
    """
    colors = get_color_palette(style)
    
    return {
        'figure.figsize': get_figure_size(),
        'figure.facecolor': colors['background'],
        'axes.facecolor': colors['background'],
        'axes.edgecolor': colors['text'],
        'axes.labelcolor': colors['text'],
        'axes.grid': True,
        'grid.color': colors['neutral'],
        'grid.alpha': 0.1,
        'xtick.color': colors['text'],
        'ytick.color': colors['text'],
        'text.color': colors['text'],
        'lines.linewidth': 2,
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12
    }


def apply_plot_defaults(style: str = 'dark') -> None:
    """
    Apply default plotting parameters.
    
    Args:
        style: Style name ('dark' or 'light').
    """
    plt.rcParams.update(get_plot_defaults(style)) 