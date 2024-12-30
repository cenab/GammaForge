import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from .config import CACHE_DIR, CACHE_EXPIRY
from .providers import get_data_provider
from ..utils.logger import get_logger

logger = get_logger(__name__)

class OptionDataFetcher:
    """Class to handle option data fetching and caching."""
    
    def __init__(self, ticker: str, use_polygon: bool = True):
        self.ticker = ticker.upper()
        self.cache_file = CACHE_DIR / f"{self.ticker}.json"
        self.provider = get_data_provider(use_polygon)
        
    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid."""
        if not self.cache_file.exists():
            return False
            
        cache_time = datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        age = (datetime.now() - cache_time).total_seconds()
        return age < CACHE_EXPIRY
        
    def _save_to_cache(self, spot_price: float, option_data: pd.DataFrame):
        """Save data to cache file."""
        cache_data = {
            'spot_price': spot_price,
            'option_data': option_data.to_dict(orient='records'),
            'timestamp': datetime.now().timestamp()
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)
            
    def _load_from_cache(self) -> tuple[float, pd.DataFrame]:
        """Load data from cache file."""
        with open(self.cache_file) as f:
            cache_data = json.load(f)
            return (
                cache_data['spot_price'],
                pd.DataFrame.from_records(cache_data['option_data'])
            )
            
    def get_option_data(self) -> tuple[float, pd.DataFrame]:
        """
        Get option data either from cache or data provider.
        
        Returns:
            tuple: (spot_price, option_data_df)
        """
        try:
            if self._is_cache_valid():
                logger.info(f"Loading cached data for {self.ticker}")
                return self._load_from_cache()
            else:
                logger.info(f"Fetching fresh data for {self.ticker}")
                spot_price, option_data = self.provider.get_option_chain(self.ticker)
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