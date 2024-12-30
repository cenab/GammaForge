import asyncio
import json
import logging
from datetime import datetime, time
from typing import Dict, List, Optional
import pytz
from collections import deque
from polygon import WebSocketClient
from polygon.websocket.models import OptionsTrade, Market

from .realtime_config import (
    POLYGON_API_KEY, WS_RECONNECT_TIMEOUT, UPDATE_INTERVAL,
    BATCH_SIZE, MAX_QUEUE_SIZE, MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE,
    MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE
)
from .gex_calculator import GEXCalculator
from .utils import logger

class RealtimeGEXHandler:
    """Handles real-time GEX calculations using Polygon.io WebSocket feed."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.client: Optional[WebSocketClient] = None
        self.update_queue = deque(maxlen=MAX_QUEUE_SIZE)
        self.last_calculation = datetime.now()
        self.gex_calculator: Optional[GEXCalculator] = None
        self.running = False
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    async def start(self):
        """Start the real-time GEX tracking."""
        self.running = True
        self.client = WebSocketClient(
            api_key=POLYGON_API_KEY,
            market=Market.Options,
            reconnect=True,
            reconnect_timeout=WS_RECONNECT_TIMEOUT
        )
        
        # Setup handlers
        self.client.subscribe(f"O.{self.ticker}*", self._handle_option_trade)
        
        # Start processing tasks
        await asyncio.gather(
            self._run_websocket(),
            self._process_updates()
        )
        
    async def stop(self):
        """Stop the real-time GEX tracking."""
        self.running = False
        if self.client:
            await self.client.close()
            
    async def _run_websocket(self):
        """Run the WebSocket connection."""
        try:
            await self.client.connect()
            while self.running:
                await asyncio.sleep(0.1)  # Prevent CPU hogging
        except Exception as e:
            self.logger.error(f"WebSocket error: {e}")
            await self.stop()
            
    def _handle_option_trade(self, trade: OptionsTrade):
        """Handle incoming option trade data."""
        if not self._is_market_hours():
            return
            
        try:
            trade_data = {
                "option": trade.symbol,
                "price": trade.price,
                "size": trade.size,
                "timestamp": trade.timestamp
            }
            self.update_queue.append(trade_data)
        except Exception as e:
            self.logger.error(f"Error handling trade: {e}")
            
    async def _process_updates(self):
        """Process queued updates and recalculate GEX."""
        while self.running:
            now = datetime.now()
            if (now - self.last_calculation).total_seconds() >= UPDATE_INTERVAL:
                await self._recalculate_gex()
                self.last_calculation = now
            await asyncio.sleep(0.1)
            
    async def _recalculate_gex(self):
        """Recalculate GEX based on recent updates."""
        if not self.update_queue:
            return
            
        # Process updates in batches
        updates = []
        while len(updates) < BATCH_SIZE and self.update_queue:
            updates.append(self.update_queue.popleft())
            
        try:
            # Update option data
            self._update_option_data(updates)
            
            # Recalculate GEX
            if self.gex_calculator:
                total_gex = self.gex_calculator.get_total_gex()
                self.logger.info(f"Updated GEX for {self.ticker}: {total_gex:,.2f}")
                
        except Exception as e:
            self.logger.error(f"Error recalculating GEX: {e}")
            
    def _update_option_data(self, updates: List[Dict]):
        """Update option data with new trades."""
        # This would update the underlying data used by GEXCalculator
        # Implementation depends on how you want to handle real-time updates
        pass
        
    def _is_market_hours(self) -> bool:
        """Check if current time is within market hours."""
        now = datetime.now(pytz.timezone('America/New_York'))
        market_open = time(MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE)
        market_close = time(MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE)
        
        return market_open <= now.time() <= market_close 