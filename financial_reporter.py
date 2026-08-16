"""Main financial reporter script - sends daily market updates to Slack."""

import logging
from config import Config
from market_utils import MarketUtils
from slack_utils import SlackUtils
from financial_api import FinancialAPI

logger = logging.getLogger(__name__)

def send_daily_market_update():
    """
    Main function to send daily market update to Slack.

    The script should send a message every time it runs. When the market is closed,
    it sends a status update instead of silently skipping.
    """
    logger.info("=" * 50)
    logger.info("Starting daily market update routine...")
    logger.info("=" * 50)

    try:
        # Validate configuration
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        return False

    # Initialize Slack client early so the status can always be sent on run.
    slack = SlackUtils()

    # Test Slack connection
    if not slack.test_connection():
        logger.error("Failed to connect to Slack")
        return False

    # Check if market is open
    if not MarketUtils.is_market_open():
        logger.info("Market is not open. Sending status message to Slack.")
        closed_message = "INFO: Market is not open. Skipping scheduled market update."
        sent = slack.send_message(closed_message)
        if sent:
            logger.info("Closed-market notification sent successfully.")
            return True
        else:
            logger.error("Failed to send closed-market notification to Slack")
            return False

    # Fetch financial data
    logger.info("Fetching financial data...")
    rates = FinancialAPI.get_all_rates()

    if not rates:
        logger.error("Failed to fetch financial data")

        # Send error notification
        error_message = "❌ Failed to fetch market data. Please check API status."
        slack.send_message(error_message)
        return False

    # Prepare and send message
    usd_ils = rates.get("usd_ils")
    btc_usd = rates.get("btc_usd")

    if usd_ils and btc_usd:
        # Create formatted message blocks
        blocks = SlackUtils.create_market_update_blocks(
            usd_ils_rate=usd_ils,
            btc_usd_price=btc_usd,
            market_status="OPEN"
        )

        # Send to Slack
        if slack.send_formatted_message(blocks):
            logger.info("✅ Market update sent successfully!")
            return True
        else:
            logger.error("Failed to send market update to Slack")
            return False
    else:
        logger.error("Missing required financial data")
        return False

if __name__ == "__main__":
    # Run the reporter
    success = send_daily_market_update()
    
    if success:
        print("\nMarket update completed successfully.")
    else:
        print("\nMarket update failed. Check logs/financial_reporter.log for details.")
