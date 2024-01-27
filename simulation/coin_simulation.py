from .historical_trade_simulator import HistoricalTradeSimulator
from .real_time_trade_simulator import RealTimeTradeSimulator
from main_config import BINANCE_API_KEY, BINANCE_API_SECRET
from main_logger import setup_logger
from binance.client import Client
from datetime import datetime


class CoinTradeSimulator:
    def __init__(self, coin, start_time, amount_usd, target_price):
        self.coin = coin
        self.start_time = start_time
        self.amount_usd = amount_usd
        self.target_price = target_price
        self.logger = setup_logger()
        try:
            self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        except Exception as e:
            self.logger.error(f"An error occurred while creating the Client for {self.coin}: {e}")
            return

    async def simulate_trade(self):
        current_date_timestamp = int(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)

        if int(self.start_time) == current_date_timestamp:
            await self._simulate_real_time_trade()
        else:
            await self._simulate_historical_and_real_time_trade()

    async def _simulate_real_time_trade(self):
        try:
            real_time_simulator = RealTimeTradeSimulator(self.client, self.logger, self.coin, self.target_price, self.amount_usd)
            await real_time_simulator.simulate_trade()
        except Exception as e:
            self.logger.error(f"An error occurred while simulating real-time trade for {self.coin}: {e}")

    async def _simulate_historical_and_real_time_trade(self):
        try:
            historical_simulator = HistoricalTradeSimulator(self.client, self.logger, self.coin, self.start_time, self.amount_usd, self.target_price)
            new_amount_usd = await historical_simulator.simulate_trade()
        except Exception as e:
            self.logger.error(f"An error occurred while simulating historical trade for {self.coin}: {e}")
            return

        if new_amount_usd is not None:
            try:
                real_time_simulator = RealTimeTradeSimulator(self.client, self.logger, self.coin, self.target_price, new_amount_usd)
                await real_time_simulator.simulate_trade()
            except Exception as e:
                self.logger.error(f"An error occurred while simulating real-time trade for {self.coin}: {e}")