import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
FETCHED_SYMBOLS_PATH = os.getenv('FETCHED_SYMBOLS_PATH')
SYMBOLS_PATH = os.getenv('SYMBOLS_PATH')

def load_configuration():
    # Load environment variables from .env file
    coins_list = os.getenv('FETCHED_SYMBOLS_PATH')

    # Set up other configuration variables
    start_time = str(int(datetime(2022, 1, 1).timestamp() * 1000))
    amount_usd = 1000
    target_price = 1200
    num_coins = 1

    return coins_list, start_time, amount_usd, target_price, num_coins