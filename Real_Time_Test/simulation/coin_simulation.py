from .historical_trade_simulator import HistoricalTradeSimulator
from .real_time_trade_simulator import RealTimeTradeSimulator
from .config import BINANCE_API_KEY, BINANCE_API_SECRET
from .logger import logger
from binance.client import Client
from datetime import datetime
import threading


def simulate_coin_trade(coin, start_time, amount_usd, target_price):
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    except Exception as e:
        logger.error(f"An error occurred while creating the Client for {coin}: {e}")
        return

    if start_time.date() == datetime.today().date():
        # If start_time is today's date, start real-time trading directly
        try:
            real_time_simulator = RealTimeTradeSimulator(client, logger, coin, target_price, amount_usd)
            real_time_simulator.simulate_trade()
        except Exception as e:
            logger.error(f"An error occurred while simulating real-time trade for {coin}: {e}")
    else:
        try:
            historical_simulator = HistoricalTradeSimulator(client, logger, coin, start_time, amount_usd, target_price)
            new_amount_usd = historical_simulator.simulate_trade()
        except Exception as e:
            logger.error(f"An error occurred while simulating historical trade for {coin}: {e}")
            return

        if new_amount_usd is not None:
            try:
                real_time_simulator = RealTimeTradeSimulator(client, logger, coin, target_price, new_amount_usd)
                real_time_simulator.simulate_trade()
            except Exception as e:
                logger.error(f"An error occurred while simulating real-time trade for {coin}: {e}")