from binance.streams import ThreadedWebsocketManager 

class RealTimeTradeSimulator:
    def __init__(self, client, logger, symbol, target_price, amount_usd):
        self.client = client
        self.logger = logger
        self.symbol = symbol
        self.target_price = target_price
        self.amount_usd = amount_usd
        self.bm = ThreadedWebsocketManager(self.client)

    def process_message(self, msg):
        if msg['e'] != 'error':
            current_price = float(msg['p'])
            self.logger.info(f"Current price of {self.symbol}: {current_price}")
            if current_price >= self.target_price:
                self.logger.info(f"Simulating selling {self.quantity} {self.symbol} at {current_price}...")
                self.bm.stop_socket(self.conn_key)
        else:
            self.logger.error(msg['m'])

    def simulate_trade(self):
        # Get the current price of the coin
        ticker = self.client.get_symbol_ticker(symbol=self.symbol)
        current_price = float(ticker['price'])

        # Calculate the quantity that can be bought with the amount_usd at the current price
        self.quantity = self.amount_usd / current_price

        self.logger.info(f"Simulating buying {self.quantity} {self.symbol} for {self.amount_usd} USD at {current_price}...")
        self.logger.info("Target price not reached in historical data, continuing with real-time data...")

        self.conn_key = self.bm.start_symbol_ticker_socket(self.symbol, self.process_message)
        self.bm.start()