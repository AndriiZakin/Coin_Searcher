import json
from datetime import datetime
from simulation import simulate_coin_trade
import threading
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

coins_list = os.getenv('FETCHED_SYMBOLS_PATH')

def fetch_symbols():
    from find_coins import DataFetcher

    fetcher = DataFetcher()
    fetcher.fetch_klines_data("1 Jan, 2017", None)

def start_simulations(start_time, amount_usd, target_price, num_coins):
    with open(coins_list, 'r') as f:
        coins = json.load(f)

    coins = coins[-num_coins:]

    # Create a new thread for each coin
    for coin in coins:
        threading.Thread(target=simulate_coin_trade, args=(coin, start_time, amount_usd, target_price)).start()
def main():

    start_time = datetime.now()
    amount_usd = 1000
    target_price = 200
    num_coins = 1

    # Fetch symbols
    #fetch_symbols()

    # Start simulations
    start_simulations(start_time, amount_usd, target_price, num_coins)

if __name__ == "__main__":
    main()