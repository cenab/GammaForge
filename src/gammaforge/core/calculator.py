"""GEX calculation functionality."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..utils.dates import get_market_days_ahead
from ..utils.logging import get_logger
from ..utils.formatting import format_billions
from .utils import calculate_price_bounds, get_one_year_date

# Constants
CONTRACT_SIZE = 100  # Standard option contract size

logger = get_logger(__name__)

class GEXCalculator:
    """Class to handle GEX calculations."""
    
    def __init__(self, spot_price: float, option_data: pd.DataFrame):
        self.spot_price = spot_price
        self.option_data = option_data
        self._calculate_notional_gamma()
        
    def _calculate_notional_gamma(self):
        """
        Calculate notional gamma exposure.
        Formula: gamma * contract_size * open_interest * spot_price
        For puts: multiply by -1 (dealers are typically short puts)
        """
        self.option_data["notional_gamma"] = (
            self.option_data["gamma"] *
            CONTRACT_SIZE *
            self.option_data["open_interest"] *
            self.spot_price
        )
        
        # Invert gamma for puts (dealers are typically short puts)
        self.option_data.loc[self.option_data["type"] == "P", "notional_gamma"] *= -1
        
    def get_total_gex(self) -> float:
        """Get total gamma exposure across all options."""
        return self.option_data["notional_gamma"].sum()
        
    def get_gex_by_strike(self) -> pd.Series:
        """Get gamma exposure grouped by strike price."""
        lower_bound, upper_bound = calculate_price_bounds(self.spot_price)
        mask = (self.option_data["strike"] >= lower_bound) & (self.option_data["strike"] <= upper_bound)
        
        return self.option_data[mask].groupby("strike")["notional_gamma"].sum()
        
    def get_gex_by_expiry(self) -> pd.Series:
        """Get gamma exposure grouped by expiration date."""
        one_year = get_one_year_date()
        mask = self.option_data["expiration"] <= one_year
        
        return self.option_data[mask].groupby("expiration")["notional_gamma"].sum()
        
    def get_gex_surface(self) -> pd.DataFrame:
        """Get gamma exposure surface (strike x expiry)."""
        lower_bound, upper_bound = calculate_price_bounds(self.spot_price)
        one_year = get_one_year_date()
        
        mask = (
            (self.option_data["strike"] >= lower_bound) &
            (self.option_data["strike"] <= upper_bound) &
            (self.option_data["expiration"] <= one_year)
        )
        
        return self.option_data[mask].pivot_table(
            values="notional_gamma",
            index="expiration",
            columns="strike",
            aggfunc="sum"
        )
        
    def get_top_strikes(self, n: int = 5) -> dict:
        """Get top n strikes by absolute gamma exposure."""
        gex_by_strike = self.get_gex_by_strike()
        
        return {
            "positive": gex_by_strike[gex_by_strike > 0].nlargest(n),
            "negative": gex_by_strike[gex_by_strike < 0].nsmallest(n)
        }
        
    def get_put_call_gex(self) -> dict:
        """
        Compare call vs put GEX.
        Returns dictionary with separate GEX values for calls and puts.
        """
        lower_bound, upper_bound = calculate_price_bounds(self.spot_price)
        mask = (self.option_data["strike"] >= lower_bound) & (self.option_data["strike"] <= upper_bound)
        subset = self.option_data[mask]
        
        call_gex = subset[subset["type"] == "C"]["notional_gamma"].sum()
        put_gex = subset[subset["type"] == "P"]["notional_gamma"].sum()
        
        return {
            "calls": call_gex,
            "puts": put_gex,
            "net": call_gex + put_gex
        }
        
    def get_cumulative_gex(self) -> pd.DataFrame:
        """
        Calculate cumulative GEX distribution across strikes.
        Returns DataFrame with strike and cumulative GEX.
        """
        lower_bound, upper_bound = calculate_price_bounds(self.spot_price, percentage=0.20)
        mask = (self.option_data["strike"] >= lower_bound) & (self.option_data["strike"] <= upper_bound)
        subset = self.option_data[mask].copy()
        
        # Sort and calculate cumulative sum
        gex_by_strike = subset.groupby("strike")["notional_gamma"].sum().sort_index()
        cumulative_gex = gex_by_strike.cumsum()
        
        return pd.DataFrame({
            "strike": cumulative_gex.index,
            "cumulative_gex": cumulative_gex.values
        })
        
    def get_weighted_expiration(self) -> float:
        """
        Calculate weighted average time to expiration (in days) based on absolute GEX.
        Returns the weighted average days to expiration.
        """
        today = datetime.now()
        
        # Calculate days to expiration
        self.option_data["days_to_exp"] = (self.option_data["expiration"] - today).dt.days
        
        # Calculate weights based on absolute GEX
        abs_gex = self.option_data["notional_gamma"].abs()
        total_abs_gex = abs_gex.sum()
        weights = abs_gex / total_abs_gex
        
        # Calculate weighted average
        weighted_days = (self.option_data["days_to_exp"] * weights).sum()
        
        return weighted_days
        
    def get_iv_profile(self) -> pd.DataFrame:
        """
        Get implied volatility profile for near-term options.
        Returns DataFrame with IV data for calls and puts separately.
        """
        if "iv" not in self.option_data.columns:
            return None
            
        # Filter for near-term options (next 30 days)
        today = datetime.now()
        near_term = today + timedelta(days=30)
        lower_bound, upper_bound = calculate_price_bounds(self.spot_price, percentage=0.20)
        
        mask = (
            (self.option_data["expiration"] <= near_term) &
            (self.option_data["strike"] >= lower_bound) &
            (self.option_data["strike"] <= upper_bound)
        )
        
        subset = self.option_data[mask].copy()
        
        return subset[["strike", "type", "iv"]] 