from binance.client import AsyncClient
from datetime import datetime
import asyncio

class HistoricalTradeSimulator:
    def __init__(self, client, logger, symbol, start_time, amount_usd, target_price):
        self.client = client
        self.logger = logger
        self.symbol = symbol
        self.start_time = start_time
        self.amount_usd = amount_usd
        self.target_price = target_price

    async def simulate_trade(self):
        klines = await asyncio.to_thread(self.client.get_historical_klines, self.symbol, AsyncClient.KLINE_INTERVAL_1HOUR, self.start_time)

        if not klines:
            self.logger.error(f"The coin {self.symbol} did not exist at the given start time.")
            return

        start_price = float(klines[0][1])
        quantity = self.amount_usd / start_price

        timestamp = int(klines[0][0])
        buy_date = datetime.fromtimestamp(timestamp / 1000)

        self.logger.info(f"Simulating buying {quantity} {self.symbol} for {self.amount_usd} USD at {start_price} on {buy_date}...")

        for kline in klines:
            close_price = float(kline[4])
            total_value = quantity * close_price  # Calculate the total value of the coins
            if total_value >= self.target_price:
                # Convert the timestamp to a datetime object
                timestamp = int(kline[0])
                sell_date = datetime.fromtimestamp(timestamp / 1000)
                self.logger.info(f"Simulated selling {quantity} {self.symbol} at {close_price} on {sell_date}...")
                return

        self.logger.info(f"Target price not reached in historical data, continuing with real-time data...")
        new_amount_usd = quantity * close_price
        return new_amount_usd