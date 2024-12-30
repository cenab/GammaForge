from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd
from polygon import RESTClient
import requests

from ..utils.logger import get_logger
from .config import CBOE_URL_PATTERNS, POLYGON_API_KEY

logger = get_logger(__name__)

class DataProvider(ABC):
    """Abstract base class for data providers."""
    
    @abstractmethod
    def get_option_chain(self, ticker: str) -> Tuple[float, pd.DataFrame]:
        """Get option chain data for a ticker."""
        pass
        
    @abstractmethod
    def get_historical_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical options data."""
        pass

class PolygonDataProvider(DataProvider):
    """Polygon.io data provider implementation."""
    
    def __init__(self):
        self.client = RESTClient(POLYGON_API_KEY)
        
    def get_option_chain(self, ticker: str) -> Tuple[float, pd.DataFrame]:
        """Get option chain data from Polygon.io."""
        try:
            # Get current stock price
            stock_price = self.client.get_last_trade(ticker)
            spot_price = stock_price.price
            
            # Get option chain
            options = self.client.list_options_contracts(
                underlying_ticker=ticker,
                expiration_date_gte=datetime.now(),
                expiration_date_lte=datetime.now().replace(year=datetime.now().year + 1)
            )
            
            # Process options data
            option_data = []
            for opt in options:
                last_quote = self.client.get_last_option_quote(opt.ticker)
                if last_quote:
                    option_data.append({
                        'option': opt.ticker,
                        'type': 'C' if opt.contract_type == 'call' else 'P',
                        'strike': opt.strike_price,
                        'expiration': opt.expiration_date,
                        'gamma': last_quote.gamma if hasattr(last_quote, 'gamma') else None,
                        'open_interest': opt.open_interest,
                        'volume': last_quote.volume if hasattr(last_quote, 'volume') else 0,
                        'iv': last_quote.implied_volatility if hasattr(last_quote, 'implied_volatility') else None
                    })
            
            return spot_price, pd.DataFrame(option_data)
            
        except Exception as e:
            logger.error(f"Error fetching data from Polygon.io: {e}")
            raise
            
    def get_historical_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical options data from Polygon.io."""
        try:
            historical_data = []
            
            # Get historical options data
            options = self.client.list_options_contracts(
                underlying_ticker=ticker,
                expiration_date_gte=start_date,
                expiration_date_lte=end_date
            )
            
            for opt in options:
                aggs = self.client.get_aggs(
                    ticker=opt.ticker,
                    multiplier=1,
                    timespan="day",
                    from_=start_date,
                    to=end_date
                )
                
                for agg in aggs:
                    historical_data.append({
                        'date': agg.timestamp,
                        'option': opt.ticker,
                        'type': 'C' if opt.contract_type == 'call' else 'P',
                        'strike': opt.strike_price,
                        'expiration': opt.expiration_date,
                        'volume': agg.volume,
                        'vwap': agg.vwap,
                        'open': agg.open,
                        'high': agg.high,
                        'low': agg.low,
                        'close': agg.close
                    })
            
            return pd.DataFrame(historical_data)
            
        except Exception as e:
            logger.error(f"Error fetching historical data from Polygon.io: {e}")
            raise

class CBOEDataProvider(DataProvider):
    """CBOE data provider implementation."""
    
    def get_option_chain(self, ticker: str) -> Tuple[float, pd.DataFrame]:
        """Get option chain data from CBOE."""
        for url_pattern in CBOE_URL_PATTERNS:
            try:
                url = url_pattern.format(ticker)
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                # Convert to pandas DataFrame
                df = pd.DataFrame.from_dict(data)
                spot_price = df.loc["current_price", "data"]
                option_data = pd.DataFrame(df.loc["options", "data"])
                
                # Process option data
                option_data["type"] = option_data.option.str.extract(r"\d([A-Z])\d")
                option_data["strike"] = option_data.option.str.extract(r"\d[A-Z](\d+)\d\d\d").astype(float)
                option_data["expiration"] = pd.to_datetime(
                    option_data.option.str.extract(r"[A-Z](\d+)").astype(str),
                    format="%y%m%d"
                )
                
                return spot_price, option_data
                
            except requests.RequestException as e:
                logger.warning(f"Failed to fetch from {url}: {e}")
                continue
                
        raise ValueError(f"Could not fetch data from any CBOE endpoint")
        
    def get_historical_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical options data from CBOE."""
        raise NotImplementedError("Historical data not available from CBOE provider")

def get_data_provider(use_polygon: bool = True) -> DataProvider:
    """Factory function to get the appropriate data provider."""
    if use_polygon and POLYGON_API_KEY:
        try:
            return PolygonDataProvider()
        except Exception as e:
            logger.warning(f"Failed to initialize Polygon provider: {e}. Falling back to CBOE.")
    return CBOEDataProvider() 