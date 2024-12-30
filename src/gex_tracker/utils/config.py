import os
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Constants
CONTRACT_SIZE = 100  # Standard option contract size
CACHE_EXPIRY = 3600  # Cache expiry in seconds (1 hour)

# CBOE API URLs
CBOE_URL_PATTERNS = [
    "https://cdn.cboe.com/api/global/delayed_quotes/options/_{}.json",
    "https://cdn.cboe.com/api/global/delayed_quotes/options/{}.json"
]

# Plotting settings
PLOT_STYLE = "seaborn-dark"
PLOT_COLORS = {
    "background": "#212946",
    "text": "#0.9",
    "grid": "#2A3459",
    "bars": "#FE53BB"
} 