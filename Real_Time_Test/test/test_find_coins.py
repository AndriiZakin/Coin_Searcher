import unittest
from unittest.mock import patch, MagicMock
from find_coins import fetch_klines_data
import json

class TestFetchKlinesData(unittest.TestCase):
    @patch('find_coins.client')
    @patch('find_coins.concurrent.futures.ThreadPoolExecutor')
    @patch('find_coins.fetch_kline')
    def test_fetch_klines_data(self, mock_fetch_kline, mock_ThreadPoolExecutor, mock_client):
        # Mock the client and its get_exchange_info method
        mock_exchange_info = {
            'symbols': [
                {'symbol': 'BTCUSDT', 'baseAsset': 'BTC', 'quoteAsset': 'USDT'},
                {'symbol': 'ETHUSDT', 'baseAsset': 'ETH', 'quoteAsset': 'USDT'}
            ]
        }
        mock_client.get_exchange_info.return_value = mock_exchange_info

        # Mock the fetch_kline function
        mock_fetch_kline.return_value = ('BTCUSDT', '2022-01-01', 40000, 42000, 38000, 41000)

        # Mock the ThreadPoolExecutor
        mock_executor = MagicMock()
        mock_executor.map.return_value = [('BTCUSDT', '2022-01-01', 40000, 42000, 38000, 41000)]
        mock_ThreadPoolExecutor.return_value = mock_executor

        # Call the fetch_klines_data function
        fetch_klines_data(start_date='1 Jan, 2017', symbol_limit=100)

        # Assert that the client's get_exchange_info method was called
        mock_client.get_exchange_info.assert_called_once()

        # Assert that the fetch_kline function was called with the correct arguments
        mock_fetch_kline.assert_called_once_with(('BTCUSDT', 'BTC', 'USDT'), '1 Jan, 2017')

        # Assert that the ThreadPoolExecutor was called with the correct arguments
        mock_ThreadPoolExecutor.assert_called_once()

        # Assert that the data was written to the 'symbols.json' file
        with open('symbols.json', 'r') as f:
            data = f.readlines()
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0], '{"symbol": "BTC/USDT", "date": "2022-01-01", "open": 40000, "high": 42000, "low": 38000, "close": 41000}\n')

        # Assert that the fetched symbols were saved to the 'fetched_symbols.json' file
        with open('fetched_symbols.json', 'r') as f:
            fetched_symbols = json.load(f)
            self.assertEqual(fetched_symbols, ['BTCUSDT'])

if __name__ == '__main__':
    unittest.main()