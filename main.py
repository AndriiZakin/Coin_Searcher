import asyncio
import os
import json
from simulation import CoinTradeSimulator
from find_coins import FindCoins
from config_logs.logger import setup_logger
from config_logs.config import load_configuration

class SimulationManager:
    def __init__(self):
        self.logger = setup_logger()
        self.coins_list, self.start_time, self.amount_usd, self.target_price, self.num_coins = load_configuration()

    def fetch_symbols(self):
        fetcher = FindCoins()
        fetcher.fetch_klines_data("1 Jan, 2017", None)

    async def start_simulations(self):
        if os.path.exists(self.coins_list):
            with open(self.coins_list, 'r') as f:
                coins = json.load(f)
        else:
            coins = []

        coins = coins[-self.num_coins:]

        # Calculate the amount to be used for each coin
        amount_per_coin = self.amount_usd / len(coins)

        # Create a list to hold our tasks
        tasks = []

        # Create a task for each coin simulation
        for coin in coins:
            self.logger.info(f"Starting simulation for {coin}")
            simulator = CoinTradeSimulator(coin, self.start_time, amount_per_coin, self.target_price)
            task = asyncio.create_task(simulator.simulate_trade())
            tasks.append(task)

        # Run the tasks concurrently
        await asyncio.gather(*tasks)

def main():
    manager = SimulationManager()

    # Fetch symbols
    manager.fetch_symbols()

    # Start simulations
    manager.logger.info("Starting simulations")
    asyncio.run(manager.start_simulations())

if __name__ == "__main__":
    main()