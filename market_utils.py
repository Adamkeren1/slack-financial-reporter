"""Market hours and timezone utilities."""

import datetime
import logging
import pytz
from config import Config

logger = logging.getLogger(__name__)

class MarketUtils:
    """Utilities for market hours checking and timezone handling."""
    
    # US holidays when market is closed (year-agnostic day/month)
    US_HOLIDAYS = [
        (1, 1),      # New Year's Day
        (1, 20),     # MLK Jr. Day (third Monday of January)
        (2, 17),     # Presidents Day (third Monday of February)
        (3, 17),     # St. Patrick's Day adjacent
        (5, 26),     # Memorial Day (last Monday of May)
        (7, 4),      # Independence Day
        (9, 1),      # Labor Day (first Monday of September)
        (11, 27),    # Thanksgiving (fourth Thursday of November)
        (12, 25),    # Christmas
    ]
    
    @staticmethod
    def get_market_timezone():
        """Get market timezone object."""
        return pytz.timezone(Config.TIMEZONE)
    
    @staticmethod
    def get_current_market_time():
        """Get current time in market timezone."""
        tz = MarketUtils.get_market_timezone()
        return datetime.datetime.now(tz)
    
    @staticmethod
    def is_weekday():
        """Check if today is a weekday (Monday=0, Sunday=6)."""
        current_time = MarketUtils.get_current_market_time()
        return current_time.weekday() < 5  # Monday to Friday
    
    @staticmethod
    def is_holiday():
        """Check if today is a US market holiday."""
        current_time = MarketUtils.get_current_market_time()
        month_day = (current_time.month, current_time.day)
        
        # Simple check for fixed holidays
        return month_day in MarketUtils.US_HOLIDAYS
    
    @staticmethod
    def is_market_open():
        """
        Check if the market is currently open.
        
        Returns:
            bool: True if market is open, False otherwise
        """
        current_time = MarketUtils.get_current_market_time()
        
        # Check if it's a weekend
        if not MarketUtils.is_weekday():
            logger.info("Market closed: Weekend")
            return False
        
        # Check if it's a holiday
        if MarketUtils.is_holiday():
            logger.info("Market closed: Holiday")
            return False
        
        # Check market hours (9:30 AM - 4:00 PM ET)
        market_open_time = current_time.replace(
            hour=Config.MARKET_OPEN_HOUR,
            minute=Config.MARKET_OPEN_MINUTE,
            second=0,
            microsecond=0
        )
        market_close_time = current_time.replace(
            hour=Config.MARKET_CLOSE_HOUR,
            minute=Config.MARKET_CLOSE_MINUTE,
            second=0,
            microsecond=0
        )
        
        is_open = market_open_time <= current_time <= market_close_time
        
        if is_open:
            logger.info(f"Market is open. Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        else:
            logger.info(f"Market closed: Outside trading hours. Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        return is_open
    
    @staticmethod
    def should_send_message():
        """
        Check if we should send the daily message.
        
        Returns:
            bool: True if it's a market open day and message time
        """
        current_time = MarketUtils.get_current_market_time()
        
        # Check if market is open
        if not MarketUtils.is_weekday() or MarketUtils.is_holiday():
            return False
        
        # Check if current time matches message time (within a minute)
        target_hour = int(Config.MESSAGE_TIME.split(":")[0])
        target_minute = int(Config.MESSAGE_TIME.split(":")[1])
        
        is_message_time = (
            current_time.hour == target_hour and
            current_time.minute == target_minute
        )
        
        return is_message_time

if __name__ == "__main__":
    # Test the market utils
    print(f"Current market time: {MarketUtils.get_current_market_time()}")
    print(f"Is weekday: {MarketUtils.is_weekday()}")
    print(f"Is holiday: {MarketUtils.is_holiday()}")
    print(f"Is market open: {MarketUtils.is_market_open()}")
    print(f"Should send message: {MarketUtils.should_send_message()}")
