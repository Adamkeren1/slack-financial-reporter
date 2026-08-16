"""Configuration management for Slack Financial Reporter."""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "financial_reporter.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for the application."""
    
    # Slack Configuration
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
    
    # Market Settings
    TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
    MESSAGE_TIME = os.getenv("MESSAGE_TIME", "09:30")
    
    # API Configuration
    EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
    CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
    
    # API Endpoints (using free APIs)
    EXCHANGERATE_API_URL = "https://api.exchangerate-api.com/v4/latest"
    COINGECKO_API_URL = "https://api.coingecko.com/v3/simple/price"
    
    # Market Hours (EST/EDT)
    MARKET_OPEN_HOUR = 9
    MARKET_OPEN_MINUTE = 30
    MARKET_CLOSE_HOUR = 16
    MARKET_CLOSE_MINUTE = 0
    
    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    REQUEST_TIMEOUT = 10  # seconds
    
    @staticmethod
    def validate():
        """Validate required configuration."""
        required_vars = ["SLACK_BOT_TOKEN", "SLACK_CHANNEL_ID"]
        missing = [var for var in required_vars if not getattr(Config, var)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        logger.info("Configuration validated successfully")

if __name__ == "__main__":
    try:
        Config.validate()
        print("✅ Configuration is valid!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
