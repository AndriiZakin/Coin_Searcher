import json
from simulation import simulate_coin_trade
import threading
from find_coins import DataFetcher
from main_logger import setup_logger
from main_config import load_configuration


class SimulationManager:
    def __init__(self):
        self.logger = setup_logger()
        self.coins_list, self.start_time, self.amount_usd, self.target_price, self.num_coins = load_configuration()

    def fetch_symbols(self):
        fetcher = DataFetcher()
        fetcher.fetch_klines_data("1 Jan, 2017", None)

    def start_simulations(self):
        with open(self.coins_list, 'r') as f:
            coins = json.load(f)

        coins = coins[-self.num_coins:]

        # Calculate the amount to be used for each coin
        amount_per_coin = self.amount_usd / len(coins)

        # Create a new thread for each coin
        for coin in coins:
            self.logger.info(f"Starting simulation for {coin}")
            threading.Thread(target=simulate_coin_trade, args=(coin, self.start_time, amount_per_coin, self.target_price)).start()

def main():
    manager = SimulationManager()

    # Fetch symbols
    manager.fetch_symbols()

    # Start simulations
    manager.logger.info("Starting simulations")
    manager.start_simulations()

if __name__ == "__main__":
    main()