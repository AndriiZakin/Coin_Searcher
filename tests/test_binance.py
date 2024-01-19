import unittest
from unittest.mock import patch, MagicMock
from binance.exceptions import BinanceAPIException, BinanceRequestException
from src.binance import BinanceClient
from binance.client import Client

class TestBinanceClient(unittest.TestCase):
    def setUp(self):
        self.client = BinanceClient()

    def test_calculate_volatility(self):
        self.assertEqual(self.client.calculate_volatility(200), 2)

    @patch('requests.get')
    def test_get_trading_pairs(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'symbols': [{'symbol': 'BTCUSDT'}, {'symbol': 'ETHUSDT'}]}
        mock_get.return_value = mock_response

        result = self.client.get_trading_pairs()
        self.assertEqual(result, ['BTCUSDT', 'ETHUSDT'])

    @patch('requests.get')
    def test_get_trading_pairs_rate_limited(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '1'}
        mock_get.return_value = mock_response

        result = self.client.get_trading_pairs()
        self.assertIsNone(result)

    @patch.object(BinanceClient, 'calculate_volatility')
    @patch.object(Client, 'get_ticker')
    def test_get_symbol_data(self, mock_get_ticker, mock_calculate_volatility):
        mock_get_ticker.return_value = {
            'symbol': 'BTCUSDT',
            'status': 'TRADING',
            'volume': '20000',
            'quoteVolume': '15000',
            'priceChangePercent': '15.0',
            'priceChange': '3000'
        }
        mock_calculate_volatility.return_value = 0.15

        result = self.client.get_symbol_data('BTCUSDT')
        expected_result = {
            'symbol': 'BTCUSDT',
            'status': 'TRADING',
            'volume': '20000',
            'liquidity': '15000',
            'priceChangePercent': '15.0',
            'volatility': 0.15,
            'price_change': '3000'
        }
        self.assertEqual(result, expected_result)

    @patch.object(Client, 'get_ticker')
    def test_get_symbol_data_api_exception(self, mock_get_ticker):
        mock_get_ticker.side_effect = BinanceAPIException

        result = self.client.get_symbol_data('BTCUSDT')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()