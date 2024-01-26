import json
import os
from collections import OrderedDict
from datetime import datetime

class DataProcessor:
    """
    A class for processing kline data fetched from Binance.

    Methods:
        sort_and_prepare_data(new_symbol_dates): Sorts and prepares the fetched kline data for JSON.
        append_data_to_symbols(new_data, symbols_path): Appends the prepared data to 'symbols.json'.
        append_data_to_fetched_symbols(sorted_new_symbols, fetched_symbols_path): Appends the fetched symbols to 'fetched_symbols.json'.
    """

    @staticmethod
    def sort_and_prepare_data(new_symbol_dates):
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

    @staticmethod
    def append_data_to_symbols(new_data, symbols_path):
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

    @staticmethod
    def append_data_to_fetched_symbols(sorted_new_symbols, fetched_symbols_path):
        """
        Appends the fetched symbols to 'fetched_symbols.json'.

        Args:
            sorted_new_symbols (list): A list of tuples containing the symbol info, date, open price, high price, low price, and close price of the first kline.
            fetched_symbols_path (str): The path to the 'fetched_symbols.json' file.

        """
        # Append new symbols to 'fetched_symbols.json'
        new_symbols = [symbol for (symbol, base, quote), date, open, high, low, close in sorted_new_symbols]
        new_symbols_dict = OrderedDict.fromkeys(new_symbols)

        if os.path.exists(fetched_symbols_path):
            with open(fetched_symbols_path, 'r') as f:
                existing_symbols = OrderedDict.fromkeys(json.load(f))
            existing_symbols.update(new_symbols_dict)
            new_symbols_json = json.dumps(list(existing_symbols.keys()))
        else:
            new_symbols_json = json.dumps(list(new_symbols_dict.keys()))

        with open(fetched_symbols_path, 'w') as f:
            f.write(new_symbols_json)