from binance.client import Client

class BinanceClient:
    def __init__(self):
        self.client = Client()

    def get_exchange_info(self):
        return self.client.get_exchange_info()

    def get_historical_klines(self, symbol, interval, start_date):
        return self.client.get_historical_klines(symbol, interval, start_date)