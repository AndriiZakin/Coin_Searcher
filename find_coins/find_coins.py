from .DataFetcher import DataFetcher
from .DataProcessor import DataProcessor
from .decorators import timer_decorator
from config_logs.config import FETCHED_SYMBOLS_PATH, SYMBOLS_PATH

class FindCoins:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.data_processor = DataProcessor()

    @timer_decorator
    def fetch_klines_data(self, start_date, symbol_limit):
        """
        Fetches and processes kline data for all symbols.

        Args:
            start_date (str): The start date for fetching the kline data.
            symbol_limit (int): The maximum number of symbols to fetch data for.
        """
        symbols = self.data_fetcher.get_symbols(symbol_limit)
        new_symbol_dates = self.data_fetcher.fetch_all_klines(symbols, start_date)
        new_data = self.data_processor.sort_and_prepare_data(new_symbol_dates)
        self.data_processor.append_data_to_symbols(new_data, SYMBOLS_PATH)
        self.data_processor.append_data_to_fetched_symbols(new_symbol_dates, FETCHED_SYMBOLS_PATH)