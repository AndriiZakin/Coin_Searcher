from unittest import TestCase
from unittest.mock import MagicMock

from find_coins.BinanceClient import BinanceClient

class TestBinanceClient(TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.binance_client = BinanceClient()
        self.binance_client.client = self.client

    def test_get_exchange_info(self):
        # Test the get_exchange_info method
        self.client.get_exchange_info.return_value = {'symbols': ['BTCUSDT', 'ETHUSDT']}
        exchange_info = self.binance_client.get_exchange_info()
        self.assertEqual(exchange_info, {'symbols': ['BTCUSDT', 'ETHUSDT']})
        self.client.get_exchange_info.assert_called_once()

    def test_get_historical_klines(self):
        # Test the get_historical_klines method
        symbol = 'BTCUSDT'
        interval = '1d'
        start_date = '2022-01-01'
        self.client.get_historical_klines.return_value = [['1640995200000', '50000', '55000', '45000', '48000']]
        klines = self.binance_client.get_historical_klines(symbol, interval, start_date)
        self.assertEqual(klines, [['1640995200000', '50000', '55000', '45000', '48000']])
        self.client.get_historical_klines.assert_called_once_with(symbol, interval, start_date)