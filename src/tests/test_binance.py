import os
import unittest
from unittest.mock import patch, MagicMock
from binance import BinanceClient

class TestBinanceClient(unittest.TestCase):
    def setUp(self):
        os.environ["BINANCE_API_KEY"] = "test_api_key"
        os.environ["BINANCE_API_SECRET"] = "test_api_secret"
        self.client = BinanceClient()

    @patch('requests.get')
    def test_get_exchange_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"symbol": "BTCUSDT", "priceChangePercent": "0.01"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.client.get_exchange_info("BTCUSDT")
        self.assertEqual(result, {"symbol": "BTCUSDT", "priceChangePercent": "0.01"})

    @patch('requests.get')
    def test_get_exchange_info_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("Error fetching exchange info")
        mock_get.return_value = mock_response

        result = self.client.get_exchange_info("BTCUSDT")
        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_trading_pairs(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"symbols": [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.client.get_trading_pairs()
        self.assertEqual(result, ["BTCUSDT", "ETHUSDT"])

    @patch('requests.get')
    def test_get_trading_pairs_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("Error fetching exchange info")
        mock_get.return_value = mock_response

        result = self.client.get_trading_pairs()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()