import logging
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from .config import PLOT_STYLE, PLOT_COLORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_plot_style():
    """Configure the matplotlib plot style."""
    plt.style.use(PLOT_STYLE)
    for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
        plt.rcParams[param] = PLOT_COLORS["background"]
    for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
        plt.rcParams[param] = PLOT_COLORS["text"]

def format_billions(value: float) -> str:
    """Format a number in billions with 2 decimal places."""
    return f"${value / 1e9:.2f}B"

def get_one_year_date() -> datetime:
    """Get date one year from today."""
    return datetime.today() + timedelta(days=365)

def calculate_price_bounds(spot_price: float, percentage: float = 0.15) -> tuple:
    """Calculate price bounds for filtering."""
    return (spot_price * (1 - percentage), spot_price * (1 + percentage)) 