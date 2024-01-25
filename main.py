import json
from simulation import simulate_coin_trade
import threading
from find_coins import DataFetcher
from main_logger import setup_logger
from main_config import load_configuration

logger = setup_logger()
coins_list, start_time, amount_usd, target_price, num_coins = load_configuration()

def fetch_symbols():

    fetcher = DataFetcher()
    fetcher.fetch_klines_data("1 Jan, 2017", None)

def start_simulations():
    with open(coins_list, 'r') as f:
        coins = json.load(f)

    coins = coins[-num_coins:]

    # Calculate the amount to be used for each coin
    amount_per_coin = amount_usd / len(coins)

    # Create a new thread for each coin
    for coin in coins:
        logger.info(f"Starting simulation for {coin}")
        threading.Thread(target=simulate_coin_trade, args=(coin, start_time, amount_per_coin, target_price)).start()
def main():
    # Fetch symbols
    fetch_symbols()

    # Start simulations
    logger.info("Starting simulations")
    start_simulations()

if __name__ == "__main__":
    main()