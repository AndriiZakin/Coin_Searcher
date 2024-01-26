from datetime import datetime
import concurrent.futures
from main_logger import setup_logger
from main_config import FETCHED_SYMBOLS_PATH
import os
import json

from .BinanceClient import Client
from .decorators import timer_decorator

class DataFetcher:
    """
    A class for fetching kline data from Binance.

    Attributes:
        client (Client): The Binance client for making API requests.
        fetched_symbols (set): A set of symbols that have already been fetched.

    Methods:
        __init__(): Initializes the BinanceDataFetcher class.
        fetch_kline(symbol_info, start_date): Fetches kline data for a specific symbol.
        get_symbols(symbol_limit): Retrieves a list of symbols from the Binance exchange.
        fetch_all_klines(symbols, start_date): Fetches kline data for all symbols concurrently.
    """

    def __init__(self):

        self.logger = setup_logger()

        self.client = Client()

        self.fetched_symbols = set()
        if os.path.exists(FETCHED_SYMBOLS_PATH):
            with open(FETCHED_SYMBOLS_PATH, 'r') as f:
                self.fetched_symbols = set(json.load(f))

    @timer_decorator
    def fetch_kline(self, symbol_info, start_date):
        symbol, base, quote = symbol_info
        if symbol in self.fetched_symbols:
            self.logger.info(f"Skipping {symbol} as it has already been fetched")
            return None
        self.logger.info(f"Fetching klines for symbol {symbol}")
        try:
            klines = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date)
            if klines:
                first_kline = klines[0]
                date = datetime.fromtimestamp(first_kline[0] / 1000)
                self.logger.info(f"First kline for symbol {symbol} is at {date}")
                self.fetched_symbols.add(symbol)  # Add symbol to fetched_symbols
                return (symbol_info, date, first_kline[1], first_kline[2], first_kline[3], first_kline[4])
        except Exception as e:
            self.logger.error(f"Could not fetch klines for symbol {symbol}: {e}")

    def get_symbols(self, symbol_limit):
        info = self.client.get_exchange_info()
        symbols = [(symbol_info['symbol'], symbol_info['baseAsset'], symbol_info['quoteAsset']) for symbol_info in info['symbols']]
        if symbol_limit is not None:
            symbols = symbols[:symbol_limit]
        return symbols

    def fetch_all_klines(self, symbols, start_date):
        symbol_info_and_start_date = [(symbol_info, start_date) for symbol_info in symbols]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            symbol_dates = list(executor.map(lambda p: self.fetch_kline(*p), symbol_info_and_start_date))
        new_symbol_dates = [x for x in symbol_dates if x is not None]
        return new_symbol_dates