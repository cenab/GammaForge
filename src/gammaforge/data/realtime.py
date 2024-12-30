"""Real-time data handling functionality."""

import asyncio
from datetime import datetime
from typing import Optional, Dict, List

import pandas as pd
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from ..utils.logger import get_logger
from ..core.calculator import GEXCalculator
from .config import POLYGON_API_KEY

logger = get_logger(__name__)

class RealtimeGEXHandler:
    """Handler for real-time GEX calculations using Polygon.io WebSocket feed."""
    
    def __init__(self, symbol: str, update_interval: int = 60):
        """
        Initialize the real-time GEX handler.
        
        Args:
            symbol: Stock symbol to track.
            update_interval: How often to recalculate GEX (in seconds).
        """
        self.symbol = symbol.upper()
        self.update_interval = update_interval
        self.client = WebSocketClient(
            api_key=POLYGON_API_KEY,
            subscriptions=[f"O.{self.symbol}"],
            market="options"
        )
        self.trades: List[Dict] = []
        self.last_update: Optional[datetime] = None
        self.calculator: Optional[GEXCalculator] = None
        
    async def handle_msg(self, msg: WebSocketMessage) -> None:
        """
        Handle incoming WebSocket messages.
        
        Args:
            msg: Message from Polygon WebSocket.
        """
        if msg.event_type == "trade":
            self.trades.append({
                'timestamp': msg.timestamp,
                'price': msg.price,
                'size': msg.size,
                'conditions': msg.conditions,
                'exchange': msg.exchange,
                'sequence': msg.sequence_number
            })
            
            # Check if it's time to update GEX
            now = datetime.now()
            if (self.last_update is None or 
                (now - self.last_update).total_seconds() >= self.update_interval):
                await self.update_gex()
                self.last_update = now
                
    async def update_gex(self) -> None:
        """Update GEX calculations with latest trade data."""
        if not self.trades:
            return
            
        # Convert trades to DataFrame
        df = pd.DataFrame(self.trades)
        
        # Calculate VWAP
        df['value'] = df['price'] * df['size']
        vwap = df['value'].sum() / df['size'].sum()
        
        # Get option chain data
        try:
            fetcher = OptionDataFetcher(self.symbol, use_polygon=True)
            spot_price, option_data = fetcher.get_option_data()
            
            # Update GEX calculations
            self.calculator = GEXCalculator(spot_price, option_data)
            total_gex = self.calculator.get_total_gex()
            
            # Log update
            logger.info(f"Updated GEX for {self.symbol}")
            logger.info(f"VWAP: ${vwap:.2f}")
            logger.info(f"Total GEX: {format_billions(total_gex)}")
            
            # Clear processed trades
            self.trades = []
            
        except Exception as e:
            logger.error(f"Error updating GEX: {e}")
            
    async def start(self) -> None:
        """Start the real-time GEX tracking."""
        try:
            await self.client.connect()
            
            # Add message handler
            self.client.subscribe_callback(self.handle_msg)
            
            # Keep connection alive
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            
        finally:
            await self.stop()
            
    async def stop(self) -> None:
        """Stop the real-time GEX tracking."""
        if self.client:
            await self.client.close()
            logger.info("WebSocket connection closed") 