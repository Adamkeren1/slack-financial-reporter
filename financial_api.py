"""Financial data fetching utilities."""

import logging
import time
import requests
from config import Config

logger = logging.getLogger(__name__)

class FinancialAPI:
    """Utilities for fetching financial data."""
    
    @staticmethod
    def fetch_with_retry(url, params=None, timeout=None):
        """
        Fetch data from URL with retry logic.
        
        Args:
            url (str): URL to fetch
            params (dict): Query parameters
            timeout (int): Request timeout in seconds
        
        Returns:
            dict: JSON response or None if failed
        """
        timeout = timeout or Config.REQUEST_TIMEOUT
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed (attempt {attempt + 1}/{Config.MAX_RETRIES}): {str(e)}")
                
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(Config.RETRY_DELAY)
                else:
                    logger.error(f"Failed to fetch data from {url} after {Config.MAX_RETRIES} attempts")
                    return None
    
    @staticmethod
    def get_usd_ils_rate():
        """
        Fetch USD to ILS exchange rate.
        
        Returns:
            float: Exchange rate or None if failed
        """
        logger.info("Fetching USD/ILS exchange rate...")
        
        try:
            data = FinancialAPI.fetch_with_retry(
                f"{Config.EXCHANGERATE_API_URL}/USD",
                params={"base": "USD"}
            )
            
            if data and "rates" in data:
                rate = data["rates"].get("ILS")
                if rate:
                    logger.info(f"USD/ILS rate: {rate:.4f}")
                    return rate
                else:
                    logger.error("ILS rate not found in response")
                    return None
            else:
                logger.error("Invalid response format from exchange rate API")
                return None
        
        except Exception as e:
            logger.error(f"Error fetching USD/ILS rate: {str(e)}")
            return None
    
    @staticmethod
    def get_btc_usd_price():
        """
        Fetch BTC to USD price from CoinGecko API.
        
        Returns:
            float: BTC price in USD or None if failed
        """
        logger.info("Fetching BTC/USD price...")
        
        try:
            data = FinancialAPI.fetch_with_retry(
                Config.COINGECKO_API_URL,
                params={
                    "ids": "bitcoin",
                    "vs_currencies": "usd",
                    "include_market_cap": "false",
                    "include_24hr_vol": "false"
                }
            )
            
            if data and "bitcoin" in data:
                price = data["bitcoin"].get("usd")
                if price:
                    logger.info(f"BTC/USD price: ${price:,.2f}")
                    return price
                else:
                    logger.error("USD price not found in response")
                    return None
            else:
                logger.error("Invalid response format from CoinGecko API")
                return None
        
        except Exception as e:
            logger.error(f"Error fetching BTC/USD price: {str(e)}")
            return None
    
    @staticmethod
    def get_all_rates():
        """
        Fetch all required financial data.
        
        Returns:
            dict: Dictionary with 'usd_ils' and 'btc_usd' keys, or empty dict if failed
        """
        results = {}
        
        usd_ils = FinancialAPI.get_usd_ils_rate()
        btc_usd = FinancialAPI.get_btc_usd_price()
        
        if usd_ils is not None:
            results["usd_ils"] = usd_ils
        if btc_usd is not None:
            results["btc_usd"] = btc_usd
        
        return results

if __name__ == "__main__":
    # Test API calls
    print("Testing financial API...")
    
    rates = FinancialAPI.get_all_rates()
    
    if rates:
        print(f"✅ API test successful!")
        print(f"   USD/ILS: {rates.get('usd_ils', 'N/A')}")
        print(f"   BTC/USD: ${rates.get('btc_usd', 'N/A'):,.2f}" if 'btc_usd' in rates else "   BTC/USD: N/A")
    else:
        print("❌ Failed to fetch data")
