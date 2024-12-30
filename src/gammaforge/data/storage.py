"""Module for tracking and analyzing historical GEX data."""

from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from .config import DATA_DIR
from .providers import get_data_provider
from ..core.calculator import GEXCalculator
from ..utils.logger import get_logger

logger = get_logger(__name__)

class HistoricalGEXTracker:
    """Class for tracking and analyzing historical GEX data."""
    
    def __init__(self, ticker: str, use_polygon: bool = True):
        self.ticker = ticker.upper()
        self.db_path = DATA_DIR / f"{self.ticker}_history.db"
        self.provider = get_data_provider(use_polygon)
        
        # Initialize database
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database for historical data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_gex (
                    date TEXT PRIMARY KEY,
                    total_gex REAL,
                    call_gex REAL,
                    put_gex REAL,
                    spot_price REAL,
                    weighted_expiry REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS strike_gex (
                    date TEXT,
                    strike REAL,
                    gex REAL,
                    type TEXT,
                    expiry TEXT,
                    PRIMARY KEY (date, strike, type, expiry)
                )
            """)
            
    def store_daily_snapshot(self, calculator: GEXCalculator, spot_price: float):
        """Store daily GEX snapshot in database."""
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Calculate GEX metrics
        total_gex = calculator.get_total_gex()
        call_gex, put_gex = calculator.get_put_call_gex()
        weighted_expiry = calculator.get_weighted_expiration()
        
        # Store daily summary
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO daily_gex
                (date, total_gex, call_gex, put_gex, spot_price, weighted_expiry)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (date, total_gex, call_gex, put_gex, spot_price, weighted_expiry))
            
            # Store strike-level data
            gex_by_strike = calculator.get_gex_by_strike()
            for strike, gex in gex_by_strike.items():
                conn.execute("""
                    INSERT OR REPLACE INTO strike_gex
                    (date, strike, gex, type, expiry)
                    VALUES (?, ?, ?, ?, ?)
                """, (date, strike, gex, 'C' if gex > 0 else 'P', date))
                
    def get_historical_gex(self, days: int = 30) -> pd.DataFrame:
        """
        Get historical GEX data for the last n days.
        
        Args:
            days: Number of days of historical data to retrieve.
            
        Returns:
            DataFrame with historical GEX data.
        """
        query = """
            SELECT date, total_gex, call_gex, put_gex, spot_price, weighted_expiry
            FROM daily_gex
            WHERE date >= date('now', ?)
            ORDER BY date
        """
        
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(
                query,
                conn,
                params=(f"-{days} days",)
            )
            
    def get_historical_strikes(self, date: str) -> pd.DataFrame:
        """
        Get strike-level GEX data for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format.
            
        Returns:
            DataFrame with strike-level GEX data.
        """
        query = """
            SELECT strike, gex, type, expiry
            FROM strike_gex
            WHERE date = ?
            ORDER BY strike
        """
        
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn, params=(date,))
            
    def analyze_gex_vs_price(self, days: int = 30) -> Dict:
        """
        Analyze correlation between GEX and price movements.
        
        Args:
            days: Number of days to analyze.
            
        Returns:
            Dictionary with analysis results.
        """
        historical_data = self.get_historical_gex(days)
        
        if len(historical_data) < 2:
            return {
                'correlation': None,
                'gex_percentiles': None,
                'price_changes': None
            }
            
        # Calculate daily changes
        historical_data['price_change'] = historical_data['spot_price'].pct_change()
        historical_data['gex_change'] = historical_data['total_gex'].pct_change()
        
        # Calculate correlation
        correlation = historical_data['gex_change'].corr(historical_data['price_change'])
        
        # Calculate GEX percentiles
        gex_percentiles = {
            p: np.percentile(historical_data['total_gex'], p)
            for p in [25, 50, 75, 90, 95]
        }
        
        # Calculate price changes following high/low GEX
        high_gex_days = historical_data['total_gex'] > gex_percentiles[75]
        low_gex_days = historical_data['total_gex'] < gex_percentiles[25]
        
        price_changes = {
            'high_gex': historical_data.loc[high_gex_days, 'price_change'].mean(),
            'low_gex': historical_data.loc[low_gex_days, 'price_change'].mean()
        }
        
        return {
            'correlation': correlation,
            'gex_percentiles': gex_percentiles,
            'price_changes': price_changes
        }
        
    def get_dominant_expiry(self) -> Optional[datetime]:
        """Get the expiration date with the largest absolute GEX."""
        query = """
            SELECT expiry, SUM(ABS(gex)) as total_gex
            FROM strike_gex
            WHERE date = date('now')
            GROUP BY expiry
            ORDER BY total_gex DESC
            LIMIT 1
        """
        
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute(query).fetchone()
            return datetime.strptime(result[0], "%Y-%m-%d") if result else None
            
    def backfill_historical_data(self, days: int = 30):
        """
        Backfill historical data using the data provider.
        
        Args:
            days: Number of days to backfill.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            # Get historical data from provider
            historical_data = self.provider.get_historical_data(
                self.ticker,
                start_date,
                end_date
            )
            
            if historical_data.empty:
                logger.warning("No historical data available for backfilling")
                return
                
            # Process and store historical data
            for date, group in historical_data.groupby('date'):
                calculator = GEXCalculator(group['close'].iloc[0], group)
                self.store_daily_snapshot(calculator, group['close'].iloc[0])
                
            logger.info(f"Successfully backfilled {days} days of historical data")
            
        except Exception as e:
            logger.error(f"Error backfilling historical data: {e}")
            raise 