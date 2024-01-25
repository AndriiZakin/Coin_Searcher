from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime
import concurrent.futures
import logging
import time
import json
import os

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Function {func.__name__} took {elapsed_time} seconds to run.")
        return result
    return wrapper

class DataFetcher:
    """
    A class for fetching and processing kline data from Binance.

    Attributes:
        client (binance.Client): The Binance client for making API requests.
        fetched_symbols (set): A set of symbols that have already been fetched.
        total_time_dict (dict): A dictionary to keep track of the total time taken by the functions.

    Methods:
        __init__(): Initializes the BinanceDataFetcher class.
        timer_decorator(func): A decorator function to measure the execution time of a function.
        fetch_kline(symbol_info, start_date): Fetches kline data for a specific symbol.
        get_symbols(symbol_limit): Retrieves a list of symbols from the Binance exchange.
        fetch_all_klines(symbols, start_date): Fetches kline data for all symbols concurrently.
        sort_and_prepare_data(new_symbol_dates): Sorts and prepares the fetched kline data for JSON.
        append_data_to_symbols(new_data, symbols_path): Appends the prepared data to 'symbols.json'.
        append_data_to_fetched_symbols(sorted_new_symbols, fetched_symbols_path): Appends the fetched symbols to 'fetched_symbols.json'.
        fetch_klines_data(start_date, symbol_limit): Fetches and processes kline data for all symbols.

    """

    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize the Binance client
        self.client = Client()

        load_dotenv()

        # Load fetched symbols
        self.fetched_symbols = set()
        if os.path.exists('Real_Time_Test/data/fetched_symbols.json'):
            with open('Real_Time_Test/data/fetched_symbols.json', 'r') as f:
                self.fetched_symbols = set(json.load(f))

    @timer_decorator
    def fetch_kline(self, symbol_info, start_date):
        """
        Fetches kline data for a specific symbol.

        Args:
            symbol_info (tuple): A tuple containing the symbol, base asset, and quote asset.
            start_date (str): The start date for fetching the kline data.

        Returns:
            tuple: A tuple containing the symbol info, date, open price, high price, low price, and close price of the first kline.

        """
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
        """
        Retrieves a list of symbols from the Binance exchange.

        Args:
            symbol_limit (int): The maximum number of symbols to retrieve.

        Returns:
            list: A list of symbols, each represented as a tuple containing the symbol, base asset, and quote asset.

        """
        # Get exchange info
        info = self.client.get_exchange_info()
        # Extract symbols and their base and quote assets
        symbols = [(symbol_info['symbol'], symbol_info['baseAsset'], symbol_info['quoteAsset']) for symbol_info in info['symbols']]
        if symbol_limit is not None:
            symbols = symbols[:symbol_limit]
        return symbols
    
    def fetch_all_klines(self, symbols, start_date):
        """
        Fetches kline data for all symbols concurrently.

        Args:
            symbols (list): A list of symbols to fetch kline data for.
            start_date (str): The start date for fetching the kline data.

        Returns:
            list: A list of tuples, each containing the symbol info, date, open price, high price, low price, and close price of the first kline.

        """
        # Fetch kline data for all symbols concurrently
        symbol_info_and_start_date = [(symbol_info, start_date) for symbol_info in symbols]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            symbol_dates = list(executor.map(lambda p: self.fetch_kline(*p), symbol_info_and_start_date))
        # Remove None values (for symbols that we could not fetch klines for)
        new_symbol_dates = [x for x in symbol_dates if x is not None]
        return new_symbol_dates
    
    def sort_and_prepare_data(self, new_symbol_dates):
        """
        Sorts and prepares the fetched kline data for JSON.

        Args:
            new_symbol_dates (list): A list of tuples containing the symbol info, date, open price, high price, low price, and close price of the first kline.

        Returns:
            list: A list of dictionaries, each representing a kline with the symbol, date, open price, high price, low price, and close price.

        """
        # Sort new symbols by date, from oldest to newest
        sorted_new_symbols = sorted(new_symbol_dates, key=lambda x: x[1])
        # Prepare data for JSON
        new_data = [
            {
                "symbol": base + "/" + quote,
                "date": date.isoformat(),
                "open": open,
                "high": high,
                "low": low,
                "close": close
            }
            for (symbol, base, quote), date, open, high, low, close in sorted_new_symbols
        ]
        return new_data

    def append_data_to_symbols(self, new_data, symbols_path):
        """
        Appends the prepared data to 'symbols.json' in the correct order based on the "date".

        Args:
            new_data (list): A list of dictionaries representing the kline data.
            symbols_path (str): The path to the 'symbols.json' file.

        """
        # Check if 'symbols.json' exists and is not empty
        if not os.path.exists(symbols_path) or os.stat(symbols_path).st_size == 0:
            # If 'symbols.json' does not exist or is empty, write new data to it
            with open(symbols_path, 'w') as f:
                json.dump(new_data, f)
        else:
            # If 'symbols.json' does exist and is not empty, merge and sort data
            with open(symbols_path, 'r') as f:
                existing_data = json.load(f)

            merged_data = existing_data + new_data
            sorted_merged_data = sorted(merged_data, key=lambda x: x["date"])

            with open(symbols_path, 'w') as f:
                json.dump(sorted_merged_data, f)

    def append_data_to_fetched_symbols(self, sorted_new_symbols, fetched_symbols_path):
        """
        Appends the fetched symbols to 'fetched_symbols.json'.

        Args:
            sorted_new_symbols (list): A list of tuples containing the symbol info, date, open price, high price, low price, and close price of the first kline.
            fetched_symbols_path (str): The path to the 'fetched_symbols.json' file.

        """
        # Append new symbols to 'fetched_symbols.json'
        new_symbols = [symbol for (symbol, base, quote), date, open, high, low, close in sorted_new_symbols]
        new_symbols_json = json.dumps(new_symbols)

        if os.path.exists(fetched_symbols_path):
            with open(fetched_symbols_path, 'r') as f:
                existing_symbols = set(json.load(f))
            existing_symbols.update(new_symbols)
            new_symbols_json = json.dumps(list(existing_symbols))

        with open(fetched_symbols_path, 'w') as f:
            f.write(new_symbols_json)

    @timer_decorator
    def fetch_klines_data(self, start_date, symbol_limit):
        """
        Fetches and processes kline data for all symbols.

        Args:
            start_date (str): The start date for fetching the kline data.
            symbol_limit (int): The maximum number of symbols to fetch data for.

        """
        symbols = self.get_symbols(symbol_limit)
        new_symbol_dates = self.fetch_all_klines(symbols, start_date)
        new_data = self.sort_and_prepare_data(new_symbol_dates)
        self.append_data_to_symbols(new_data, os.getenv('SYMBOLS_PATH'))
        self.append_data_to_fetched_symbols(new_symbol_dates, os.getenv('FETCHED_SYMBOLS_PATH'))


