import argparse
import asyncio
import logging
import signal
from typing import Optional

from ..data.realtime import RealtimeGEXHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RealtimeGEXTracker:
    """CLI interface for real-time GEX tracking."""
    
    def __init__(self):
        self.handler: Optional[RealtimeGEXHandler] = None
        self.running = False
        
    def parse_args(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description="Real-time GEX Tracker")
        
        parser.add_argument(
            "--ticker",
            type=str,
            required=True,
            help="Ticker symbol to track (e.g., SPX, SPY)"
        )
        
        parser.add_argument(
            "--log-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO",
            help="Set the logging level"
        )
        
        parser.add_argument(
            "--update-interval",
            type=float,
            default=1.0,
            help="Update interval in seconds"
        )
        
        return parser.parse_args()
        
    async def start(self):
        """Start the real-time tracker."""
        args = self.parse_args()
        
        # Setup logging
        logging.getLogger().setLevel(args.log_level)
        
        try:
            self.running = True
            self.handler = RealtimeGEXHandler(
                args.ticker,
                update_interval=args.update_interval
            )
            
            # Setup signal handlers
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, self._signal_handler)
                
            logger.info(f"Starting real-time GEX tracking for {args.ticker}")
            await self.handler.start()
            
        except Exception as e:
            logger.error(f"Error starting tracker: {e}")
            await self.stop()
            
    async def stop(self):
        """Stop the real-time tracker."""
        self.running = False
        if self.handler:
            await self.handler.stop()
            
    def _signal_handler(self, signum, frame):
        """Handle system signals."""
        logger.info("Received shutdown signal")
        asyncio.create_task(self.stop())

def main():
    """Entry point for real-time GEX tracking."""
    tracker = RealtimeGEXTracker()
    asyncio.run(tracker.start())

if __name__ == "__main__":
    main() 