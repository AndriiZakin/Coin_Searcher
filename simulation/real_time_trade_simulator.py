from binance.streams import ThreadedWebsocketManager 
from datetime import datetime

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
            total_value = self.quantity * current_price  # Calculate the total value of the coins
            self.logger.info(f"Current price of {self.symbol}: {current_price}")
            if total_value >= self.target_price:
                sell_date = datetime.now()
                self.logger.info(f"Simulating selling {self.quantity} {self.symbol} at {current_price} on {sell_date}...")
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

        self.conn_key = self.bm.start_symbol_ticker_socket(self.symbol, self.process_message)
        self.bm.start()

        if not self.bm.is_alive():
            self.logger.error("WebSocket connection failed.")
            return False
        
        return True