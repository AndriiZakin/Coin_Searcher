import unittest
from unittest.mock import patch, MagicMock
from find_coins import DataFetcher
from datetime import datetime

class TestDataFetcher(unittest.TestCase):
    @patch('find_coins.find_coins.Client')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=MagicMock)
    def test_init(self, mock_open, mock_exists, mock_client):
        # Mock the os.path.exists function to return True
        mock_exists.return_value = True

        # Mock the open function to return a file with the content ['BTCUSDT']
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.read.return_value = '["BTCUSDT"]'
        mock_open.return_value = mock_file

        # Initialize the DataFetcher
        fetcher = DataFetcher()

        # Assert that the Binance client was initialized
        mock_client.assert_called_once()

        # Assert that the fetched symbols were loaded correctly
        self.assertEqual(fetcher.fetched_symbols, set(['BTCUSDT']))

    @patch('find_coins.find_coins.Client')
    def test_fetch_kline(self, mock_client):
        # Mock the Binance client and its get_historical_klines method
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.get_historical_klines.return_value = [[1617235200000, '58000.00000000', '59000.00000000', '57000.00000000', '58000.00000000', '100.00000000']]

        # Initialize the DataFetcher and set the fetched symbols
        fetcher = DataFetcher()
        fetcher.fetched_symbols = set(['ETHUSDT'])

        # Call the fetch_kline method
        result = fetcher.fetch_kline(('BTCUSDT', 'BTC', 'USDT'), "1 year ago UTC")

        # Assert that the get_historical_klines method was called with the correct arguments
        mock_client_instance.get_historical_klines.assert_called_once_with('BTCUSDT', mock_client_instance.KLINE_INTERVAL_1DAY, "1 year ago UTC")

        # Assert that the method returned the correct result
        self.assertEqual(result, (('BTCUSDT', 'BTC', 'USDT'), datetime.fromtimestamp(1617235200000 / 1000), '58000.00000000', '59000.00000000', '57000.00000000', '58000.00000000'))

    @patch('find_coins.find_coins.Client')
    def test_get_symbols(self, mock_client):
        # Mock the Binance client and its get_exchange_info method
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.get_exchange_info.return_value = {'symbols': [{'symbol': 'BTCUSDT', 'baseAsset': 'BTC', 'quoteAsset': 'USDT'}, {'symbol': 'ETHUSDT', 'baseAsset': 'ETH', 'quoteAsset': 'USDT'}]}

        # Initialize the DataFetcher
        fetcher = DataFetcher()

        # Call the get_symbols method
        result = fetcher.get_symbols(1)

        # Assert that the get_exchange_info method was called
        mock_client_instance.get_exchange_info.assert_called_once()

        # Assert that the method returned the correct result
        self.assertEqual(result, [('BTCUSDT', 'BTC', 'USDT')])

    # Add more tests for the other methods...

if __name__ == '__main__':
    unittest.main()