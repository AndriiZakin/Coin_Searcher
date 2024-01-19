import os
import time
import requests
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

class BinanceClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.api_url = os.getenv('API_URL')
        self.client = Client(self.api_key, self.api_secret)

        if not self.api_key or not self.api_secret:
            raise ValueError("API keys not found in environment variables")

        self.headers = {'X-MBX-APIKEY': self.api_key}

    @staticmethod
    def calculate_volatility(price_change_percent):
        return price_change_percent / 100

    def get_trading_pairs(self):
        url = f"{self.api_url}/exchangeInfo"
    
        while True:
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
    
                if response.status_code == 429 or response.status_code == 418:
                    # We're being rate limited
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        time.sleep(int(retry_after))
                    else:
                        time.sleep(60)  # Default to waiting 60 seconds
                    continue
                
                data = response.json()
                return [symbol['symbol'] for symbol in data['symbols']]
            except (requests.exceptions.RequestException, ValueError, KeyError) as e:
                logging.error("Error fetching exchange info")
                return None

    def get_symbol_data(self, pair):
        try:
            stats = self.client.get_ticker(symbol=pair)
        except (BinanceAPIException, BinanceRequestException) as e:
            logging.error("Error fetching ticker info")
            return None

        if 'priceChangePercent' not in stats:
            logging.error("Unexpected data format")
            return None

        volatility = self.calculate_volatility(stats.get('priceChangePercent', 0))

        trading_pair = {
            'symbol': pair,
            'status': stats.get('status'),
            'volume': stats.get('volume'),
            'liquidity': stats.get('quoteVolume'), 
            'priceChangePercent': stats.get('priceChangePercent'),
            'volatility': volatility,
            'price_change': stats.get('priceChange')
        }

        return trading_pair