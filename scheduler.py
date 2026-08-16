"""Scheduler for running the financial reporter at market open."""

import logging
import schedule
import time
from market_utils import MarketUtils
from financial_reporter import send_daily_market_update

logger = logging.getLogger(__name__)

def scheduled_job():
    """Job to run at scheduled time."""
    logger.info("Scheduled job triggered")
    send_daily_market_update()

def start_scheduler():
    """
    Start the schedule loop.
    
    This will run the financial reporter once per day at market open.
    For production, use system-level schedulers (cron, Task Scheduler, etc.)
    """
    from config import Config
    
    message_time = Config.MESSAGE_TIME  # Format: "09:30"
    
    logger.info(f"Scheduler started - will run daily at {message_time}")
    
    # Schedule the job
    schedule.every().day.at(message_time).do(scheduled_job)
    
    # Keep scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        start_scheduler()
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
