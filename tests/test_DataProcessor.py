import os
import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from find_coins.DataProcessor import DataProcessor

class TestDataProcessor(TestCase):
    def setUp(self):
        self.symbols_path = "symbols.json"
        self.fetched_symbols_path = "fetched_symbols.json"

    def tearDown(self):
        if os.path.exists(self.symbols_path):
            os.remove(self.symbols_path)
        if os.path.exists(self.fetched_symbols_path):
            os.remove(self.fetched_symbols_path)

    def test_sort_and_prepare_data(self):
        # Test sorting and preparing data
        new_symbol_dates = [
            (("BTC/USDT", "BTC", "USDT"), datetime(2022, 1, 1), 40000, 41000, 39000, 40500),
            (("ETH/USDT", "ETH", "USDT"), datetime(2022, 1, 2), 3000, 3100, 2900, 3050),
            (("XRP/USDT", "XRP", "USDT"), datetime(2022, 1, 3), 0.5, 0.6, 0.4, 0.55)
        ]
        expected_result = [
            {
                "symbol": "BTC/USDT",
                "date": "2022-01-01T00:00:00",
                "open": 40000,
                "high": 41000,
                "low": 39000,
                "close": 40500
            },
            {
                "symbol": "ETH/USDT",
                "date": "2022-01-02T00:00:00",
                "open": 3000,
                "high": 3100,
                "low": 2900,
                "close": 3050
            },
            {
                "symbol": "XRP/USDT",
                "date": "2022-01-03T00:00:00",
                "open": 0.5,
                "high": 0.6,
                "low": 0.4,
                "close": 0.55
            }
        ]
        result = DataProcessor.sort_and_prepare_data(new_symbol_dates)
        self.assertEqual(result, expected_result)

    def test_append_data_to_symbols_empty_file(self):
        # Test appending data to empty 'symbols.json' file
        new_data = [
            {
                "symbol": "BTC/USDT",
                "date": "2022-01-01T00:00:00",
                "open": 40000,
                "high": 41000,
                "low": 39000,
                "close": 40500
            }
        ]
        DataProcessor.append_data_to_symbols(new_data, self.symbols_path)
        with open(self.symbols_path, 'r') as f:
            result = json.load(f)
        self.assertEqual(result, new_data)

    def test_append_data_to_symbols_existing_file(self):
        # Test appending data to existing 'symbols.json' file
        existing_data = [
            {
                "symbol": "ETH/USDT",
                "date": "2022-01-02T00:00:00",
                "open": 3000,
                "high": 3100,
                "low": 2900,
                "close": 3050
            }
        ]
        new_data = [
            {
                "symbol": "BTC/USDT",
                "date": "2022-01-01T00:00:00",
                "open": 40000,
                "high": 41000,
                "low": 39000,
                "close": 40500
            }
        ]
        expected_result = [
            {
                "symbol": "BTC/USDT",
                "date": "2022-01-01T00:00:00",
                "open": 40000,
                "high": 41000,
                "low": 39000,
                "close": 40500
            },
            {
                "symbol": "ETH/USDT",
                "date": "2022-01-02T00:00:00",
                "open": 3000,
                "high": 3100,
                "low": 2900,
                "close": 3050
            }
        ]
        with open(self.symbols_path, 'w') as f:
            json.dump(existing_data, f)
        DataProcessor.append_data_to_symbols(new_data, self.symbols_path)
        with open(self.symbols_path, 'r') as f:
            result = json.load(f)
        self.assertEqual(result, expected_result)

    def test_append_data_to_fetched_symbols_existing_file(self):
        # Test appending data to existing 'fetched_symbols.json' file
        existing_symbols = ["ETH/USDT"]
        sorted_new_symbols = [
            (("BTC/USDT", "BTC", "USDT"), datetime(2022, 1, 1), 40000, 41000, 39000, 40500),
            (("XRP/USDT", "XRP", "USDT"), datetime(2022, 1, 3), 0.5, 0.6, 0.4, 0.55)
        ]
        expected_result = ["ETH/USDT", "BTC/USDT", "XRP/USDT"]
        with open(self.fetched_symbols_path, 'w') as f:
            json.dump(existing_symbols, f)
        DataProcessor.append_data_to_fetched_symbols(sorted_new_symbols, self.fetched_symbols_path)
        with open(self.fetched_symbols_path, 'r') as f:
            result = json.load(f)
        self.assertEqual(result, expected_result)

    def test_append_data_to_fetched_symbols_new_file(self):
        # Test appending data to new 'fetched_symbols.json' file
        sorted_new_symbols = [
            (("BTC/USDT", "BTC", "USDT"), datetime(2022, 1, 1), 40000, 41000, 39000, 40500),
            (("XRP/USDT", "XRP", "USDT"), datetime(2022, 1, 3), 0.5, 0.6, 0.4, 0.55)
        ]
        expected_result = ["BTC/USDT", "XRP/USDT"]
        DataProcessor.append_data_to_fetched_symbols(sorted_new_symbols, self.fetched_symbols_path)
        with open(self.fetched_symbols_path, 'r') as f:
            result = json.load(f)
        self.assertEqual(result, expected_result)