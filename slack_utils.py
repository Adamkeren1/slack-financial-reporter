"""Slack API integration utilities."""

import logging
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import Config

logger = logging.getLogger(__name__)

class SlackUtils:
    """Utilities for Slack API interactions."""
    
    def __init__(self):
        """Initialize Slack client."""
        self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
        logger.info("Slack client initialized")
    
    def send_message(self, message_text, channel_id=None):
        """
        Send a message to Slack channel.
        
        Args:
            message_text (str): Plain text message
            channel_id (str): Slack channel ID (uses default if not provided)
        
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        channel_id = channel_id or Config.SLACK_CHANNEL_ID
        
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=message_text
            )
            logger.info(f"Message sent successfully to {channel_id}")
            return True
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            return False
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False
    
    def send_formatted_message(self, blocks, channel_id=None):
        """
        Send a formatted message with blocks to Slack channel.
        
        Args:
            blocks (list): List of block dictionaries for formatting
            channel_id (str): Slack channel ID (uses default if not provided)
        
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        channel_id = channel_id or Config.SLACK_CHANNEL_ID
        
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                blocks=blocks
            )
            logger.info(f"Formatted message sent successfully to {channel_id}")
            return True
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            return False
        except Exception as e:
            logger.error(f"Failed to send formatted message: {str(e)}")
            return False
    
    def test_connection(self):
        """
        Test connection to Slack API.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            response = self.client.auth_test()
            logger.info(f"✅ Connected to Slack as: {response['user_id']}")
            return True
        except SlackApiError as e:
            logger.error(f"❌ Slack connection failed: {e.response['error']}")
            return False
        except Exception as e:
            logger.error(f"❌ Connection error: {str(e)}")
            return False
    
    @staticmethod
    def create_market_update_blocks(usd_ils_rate, btc_usd_price, market_status="OPEN"):
        """
        Create formatted message blocks for market update.
        
        Args:
            usd_ils_rate (float): USD to ILS exchange rate
            btc_usd_price (float): BTC to USD price
            market_status (str): Market status indicator
        
        Returns:
            list: List of block dictionaries for Slack
        """
        status_emoji = "✅" if market_status == "OPEN" else "🔴"
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*📊 Daily Market Update*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*🇺🇸 USD / ILS*\n`{usd_ils_rate:.4f}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*₿ BTC / USD*\n`${btc_usd_price:,.2f}`"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Market Status: {status_emoji} {market_status}\nNext update: Tomorrow 9:30 AM ET"
                }
            }
        ]
        
        return blocks

if __name__ == "__main__":
    # Test Slack connection
    slack = SlackUtils()
    
    if slack.test_connection():
        print("✅ Slack connection successful!")
        
        # Send a test message
        test_blocks = SlackUtils.create_market_update_blocks(
            usd_ils_rate=3.65,
            btc_usd_price=42350.00,
            market_status="OPEN"
        )
        
        slack.send_formatted_message(test_blocks)
    else:
        print("❌ Failed to connect to Slack")
