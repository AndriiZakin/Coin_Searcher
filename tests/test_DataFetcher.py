import os
import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from binance.client import Client
from find_coins.DataFetcher import DataFetcher

class TestDataFetcher(TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.fetcher = DataFetcher()
        self.fetcher.client = self.client
        self.fetcher.logger = self.logger

    def test_fetch_kline_symbol_already_fetched(self):
        # Simulate the case where the symbol has already been fetched
        symbol_info = ('BTCUSDT', 'BTC', 'USDT')
        self.fetcher.fetched_symbols = {'BTCUSDT'}
        result = self.fetcher.fetch_kline(symbol_info, datetime.now())
        self.assertIsNone(result)
        self.logger.info.assert_called_with("Skipping BTCUSDT as it has already been fetched")

    def test_fetch_kline_successful(self):
        # Simulate the case where fetching kline data is successful
        symbol_info = ('BTCUSDT', 'BTC', 'USDT')
        start_date = datetime.now()
        klines = [[1620000000000, '50000', '55000', '49000', '52000']]
        self.client.get_historical_klines.return_value = klines
        result = self.fetcher.fetch_kline(symbol_info, start_date)
        expected_result = ('BTCUSDT', start_date, '50000', '55000', '49000', '52000')
        self.assertEqual(result, expected_result)
        self.logger.info.assert_called_with("Fetching klines for symbol BTCUSDT")
        self.logger.info.assert_called_with("First kline for symbol BTCUSDT is at <datetime>")
        self.assertIn('BTCUSDT', self.fetcher.fetched_symbols)

    def test_fetch_kline_exception(self):
        # Simulate the case where an exception occurs during fetching kline data
        symbol_info = ('BTCUSDT', 'BTC', 'USDT')
        start_date = datetime.now()
        error_message = "Connection error"
        self.client.get_historical_klines.side_effect = Exception(error_message)
        result = self.fetcher.fetch_kline(symbol_info, start_date)
        self.assertIsNone(result)
        self.logger.error.assert_called_with(f"Could not fetch klines for symbol BTCUSDT: {error_message}")

    def test_get_symbols_no_limit(self):
        # Simulate the case where no symbol limit is specified
        symbol_limit = None
        exchange_info = {
            'symbols': [
                {'symbol': 'BTCUSDT', 'baseAsset': 'BTC', 'quoteAsset': 'USDT'},
                {'symbol': 'ETHUSDT', 'baseAsset': 'ETH', 'quoteAsset': 'USDT'}
            ]
        }
        self.client.get_exchange_info.return_value = exchange_info
        result = self.fetcher.get_symbols(symbol_limit)
        expected_result = [
            ('BTCUSDT', 'BTC', 'USDT'),
            ('ETHUSDT', 'ETH', 'USDT')
        ]
        self.assertEqual(result, expected_result)

    def test_get_symbols_with_limit(self):
        # Simulate the case where a symbol limit is specified
        symbol_limit = 1
        exchange_info = {
            'symbols': [
                {'symbol': 'BTCUSDT', 'baseAsset': 'BTC', 'quoteAsset': 'USDT'},
                {'symbol': 'ETHUSDT', 'baseAsset': 'ETH', 'quoteAsset': 'USDT'}
            ]
        }
        self.client.get_exchange_info.return_value = exchange_info
        result = self.fetcher.get_symbols(symbol_limit)
        expected_result = [('BTCUSDT', 'BTC', 'USDT')]
        self.assertEqual(result, expected_result)

    def test_fetch_all_klines(self):
        # Simulate the case where fetching kline data for all symbols is successful
        symbols = [('BTCUSDT', 'BTC', 'USDT'), ('ETHUSDT', 'ETH', 'USDT')]
        start_date = datetime.now()
        self.fetcher.fetch_kline = MagicMock(side_effect=[('BTCUSDT', start_date, '50000', '55000', '49000', '52000'), None])
        result = self.fetcher.fetch_all_klines(symbols, start_date)
        expected_result = [('BTCUSDT', start_date, '50000', '55000', '49000', '52000')]
        self.assertEqual(result, expected_result)
        self.fetcher.fetch_kline.assert_called_with(('BTCUSDT', 'BTC', 'USDT'), start_date)
        self.fetcher.fetch_kline.assert_called_with(('ETHUSDT', 'ETH', 'USDT'), start_date)