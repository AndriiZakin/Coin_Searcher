from binance.client import Client

class HistoricalTradeSimulator:
    def __init__(self, client, logger, symbol, start_time, amount_usd, target_price):
        self.client = client
        self.logger = logger
        self.symbol = symbol
        self.start_time = start_time
        self.amount_usd = amount_usd
        self.target_price = target_price

    def simulate_trade(self):
        # Get historical klines data from start_time to now
        klines = self.client.get_historical_klines(self.symbol, Client.KLINE_INTERVAL_1HOUR, self.start_time)

        # Simulate buying the coin at the start_time price
        start_price = float(klines[0][1])
        quantity = self.amount_usd / start_price
        self.logger.info(f"Simulating buying {quantity} {self.symbol} for {self.amount_usd} USD at {start_price}...")

        # Simulate the strategy based on historical data
        for kline in klines:
            close_price = float(kline[4])
            if close_price >= self.target_price:
                self.logger.info(f"Simulated selling {quantity} {self.symbol} at {close_price}...")
                return

        self.logger.info(f"Target price not reached in historical data, continuing with real-time data...")
        new_amount_usd = quantity * close_price
        return new_amount_usd