"""Configuration settings for data handling."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directory settings
BASE_DIR = Path.home() / ".gammaforge"
CACHE_DIR = BASE_DIR / "cache"
DATA_DIR = BASE_DIR / "data"

# Create directories if they don't exist
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Cache settings
CACHE_EXPIRY = 3600  # Cache expiry in seconds (1 hour)

# CBOE URL patterns
CBOE_URL_PATTERNS = {
    "option_chain_primary": "https://cdn.cboe.com/api/global/delayed_quotes/options/{symbol}.json",
    "option_chain_underscore": "https://cdn.cboe.com/api/global/delayed_quotes/options/_{symbol}.json"
}

# Polygon.io API configuration
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") 