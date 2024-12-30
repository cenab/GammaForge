"""Data provider implementations."""

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
        errors = []
        
        # Try both URL patterns
        patterns = [
            CBOE_URL_PATTERNS["option_chain_underscore"],  # Try underscore version first
            CBOE_URL_PATTERNS["option_chain_primary"]      # Then try primary version
        ]
        
        for pattern in patterns:
            try:
                url = pattern.format(symbol=ticker)
                logger.info(f"Trying URL: {url}")
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                if "data" not in data:
                    raise ValueError("Invalid response format: 'data' field missing")
                    
                # Extract spot price
                spot_price = float(data["data"].get("current_price", 0))
                if spot_price == 0:
                    raise ValueError("Invalid spot price")
                    
                # Extract option data
                options = data["data"].get("options", [])
                if not options:
                    raise ValueError("No options data found")
                    
                # Convert to DataFrame
                option_data = pd.DataFrame(options)
                
                # Ensure required columns exist
                required_columns = ["gamma", "open_interest", "volume", "iv"]
                for col in required_columns:
                    if col not in option_data.columns:
                        option_data[col] = None
                        
                # Extract option type and strike from option symbol
                option_data["type"] = option_data["option"].str[-9].map({"C": "C", "P": "P"})
                option_data["strike"] = option_data["option"].str[-8:-3].astype(float)
                option_data["expiration"] = pd.to_datetime(
                    option_data["option"].str[-15:-9],
                    format="%y%m%d"
                )
                
                # Filter out invalid data
                option_data = option_data[
                    (option_data["strike"] > 0) & 
                    (option_data["type"].isin(["C", "P"]))
                ]
                
                if option_data.empty:
                    raise ValueError("No valid options data after filtering")
                    
                return spot_price, option_data
                
            except Exception as e:
                errors.append(f"{pattern}: {str(e)}")
                continue
        
        # If we get here, both URLs failed
        error_msg = "\n".join(errors)
        logger.error(f"Failed to fetch from CBOE: {error_msg}")
        raise ValueError(f"Could not fetch data from CBOE endpoint: {error_msg}")
        
    def get_historical_data(self, ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical options data from CBOE."""
        logger.warning("CBOE historical data API is not available. Consider using a paid data provider or storing daily snapshots.")
        return pd.DataFrame()  # Return empty DataFrame

def get_data_provider(use_polygon: bool = True) -> DataProvider:
    """Factory function to get the appropriate data provider."""
    if use_polygon and POLYGON_API_KEY:
        try:
            return PolygonDataProvider()
        except Exception as e:
            logger.warning(f"Failed to initialize Polygon provider: {e}. Falling back to CBOE.")
    return CBOEDataProvider() 