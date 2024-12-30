"""Configuration settings for visualization."""

# Plot colors
PLOT_COLORS = {
    'positive': '#2ecc71',  # Green
    'negative': '#e74c3c',  # Red
    'neutral': '#3498db',   # Blue
    'background': '#2c3e50',  # Dark blue
    'text': '#ecf0f1',      # Light gray
    'grid': '#7f8c8d',      # Gray
    'bars': '#3498db',      # Blue for bars
    'line': '#e67e22',      # Orange for lines
    'scatter': '#9b59b6',   # Purple for scatter plots
    'area': '#1abc9c',      # Turquoise for area plots
    'heatmap': {
        'positive': '#2ecc71',
        'negative': '#e74c3c',
        'neutral': '#3498db'
    }
}

# Plot styles
PLOT_STYLES = {
    'figure.figsize': (12, 8),
    'figure.dpi': 100,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'lines.linewidth': 2
}

# Theme settings
DARK_THEME = {
    'axes.facecolor': PLOT_COLORS['background'],
    'figure.facecolor': PLOT_COLORS['background'],
    'text.color': PLOT_COLORS['text'],
    'axes.labelcolor': PLOT_COLORS['text'],
    'xtick.color': PLOT_COLORS['text'],
    'ytick.color': PLOT_COLORS['text'],
    'grid.color': PLOT_COLORS['grid']
}

LIGHT_THEME = {
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'text.color': 'black',
    'axes.labelcolor': 'black',
    'xtick.color': 'black',
    'ytick.color': 'black',
    'grid.color': '#cccccc'
} 