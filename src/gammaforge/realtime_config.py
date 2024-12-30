import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Polygon.io API configuration
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
if not POLYGON_API_KEY:
    raise ValueError("POLYGON_API_KEY environment variable is not set")

# WebSocket configuration
WS_RECONNECT_TIMEOUT = 30  # seconds
WS_HEARTBEAT_INTERVAL = 30  # seconds

# Real-time processing settings
UPDATE_INTERVAL = 1.0  # seconds between GEX recalculations
BATCH_SIZE = 100  # number of updates to process in batch
MAX_QUEUE_SIZE = 10000  # maximum number of updates to queue

# Market hours (US Eastern Time)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0

# Logging configuration
WEBSOCKET_LOG_LEVEL = "INFO"
DATA_LOG_LEVEL = "INFO" 