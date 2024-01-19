import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

API_URL = 'https://api.binance.com/api/v3'

class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError("API keys not found in environment variables")

        self.headers = {'X-MBX-APIKEY': self.api_key}

    def get_trading_pairs(self):
        url = f"{API_URL}/exchangeInfo"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching exchange info: {e}")
            return None

        try:
            data = response.json()
            return [symbol['symbol'] for symbol in data['symbols']]
        except (ValueError, KeyError):
            logging.error("Error: Unable to parse JSON response or key not found")
            return None