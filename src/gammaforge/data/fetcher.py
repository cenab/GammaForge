"""Data fetching functionality."""

import json
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pandas as pd

from ..utils.logger import get_logger
from .config import CACHE_DIR, CACHE_EXPIRY
from .providers import get_data_provider

logger = get_logger(__name__)

class OptionDataFetcher:
    """Class to handle fetching option data."""
    
    def __init__(self, ticker: str, use_polygon: bool = False):
        """
        Initialize the fetcher.
        
        Args:
            ticker: Stock symbol to fetch data for.
            use_polygon: Whether to use Polygon.io as data provider.
        """
        self.ticker = ticker.upper()
        self.provider = get_data_provider(use_polygon)
        self.cache_file = CACHE_DIR / f"{self.ticker}_options.json"
        
    def _save_to_cache(self, spot_price: float, option_data: pd.DataFrame) -> None:
        """Save data to cache."""
        try:
            # Convert timestamps to strings before saving
            option_data_dict = option_data.copy()
            if 'expiration' in option_data_dict.columns:
                option_data_dict['expiration'] = option_data_dict['expiration'].dt.strftime('%Y-%m-%d')
                
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'spot_price': spot_price,
                'option_data': option_data_dict.to_dict(orient='records')
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
                
            logger.debug(f"Saved data to cache: {self.cache_file}")
                
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
            
    def _load_from_cache(self) -> Tuple[float, pd.DataFrame]:
        """Load data from cache if valid."""
        try:
            if not self.cache_file.exists():
                logger.debug("No cache file found")
                return None
                
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
                
            # Check cache expiry
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if (datetime.now() - cache_time).total_seconds() > CACHE_EXPIRY:
                logger.debug("Cache expired")
                return None
                
            # Convert option data back to DataFrame
            option_data = pd.DataFrame(cache_data['option_data'])
            if 'expiration' in option_data.columns:
                option_data['expiration'] = pd.to_datetime(option_data['expiration'])
                
            logger.debug(f"Loaded data from cache: {self.cache_file}")
            return cache_data['spot_price'], option_data
            
        except Exception as e:
            logger.error(f"Error loading from cache: {e}")
            return None
        
    def get_option_data(self) -> Tuple[float, pd.DataFrame]:
        """
        Get option chain data for the ticker.
        
        Returns:
            Tuple of (spot_price, option_data_df).
        """
        # Try to load from cache first
        cached_data = self._load_from_cache()
        if cached_data is not None:
            logger.info(f"Using cached data for {self.ticker}")
            return cached_data
            
        # Fetch fresh data
        logger.info(f"Fetching fresh data for {self.ticker}")
        try:
            spot_price, option_data = self.provider.get_option_chain(self.ticker)
            
            # Validate data
            if option_data.empty:
                raise ValueError("Empty option data received")
                
            required_columns = ['type', 'strike', 'expiration', 'gamma', 'open_interest']
            missing_columns = [col for col in required_columns if col not in option_data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
                
            # Save to cache
            self._save_to_cache(spot_price, option_data)
            
            return spot_price, option_data
            
        except Exception as e:
            logger.error(f"Error getting option data: {e}")
            raise
            
    def get_historical_data(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical options data."""
        try:
            return self.provider.get_historical_data(self.ticker, start_date, end_date)
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            raise 