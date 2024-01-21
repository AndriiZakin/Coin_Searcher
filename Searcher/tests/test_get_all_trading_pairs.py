import unittest
from unittest.mock import patch, MagicMock
from main_search import get_all_trading_pairs
from src.binance_work import get_valid_pairs

class TestGetAllTradingPairs(unittest.TestCase):
    @patch('src.get_all_trading_pairs.BinanceClient')
    @patch('src.get_all_trading_pairs.load_or_fetch_data')
    @patch('src.get_all_trading_pairs.update_data')
    @patch('src.get_all_trading_pairs.get_valid_pairs')
    def test_get_all_trading_pairs(self, mock_get_valid_pairs, mock_update_data, mock_load_or_fetch_data, mock_BinanceClient):
        # Mock the BinanceClient and its get_trading_pairs method
        mock_client = MagicMock()
        mock_BinanceClient.return_value = mock_client
        mock_client.get_trading_pairs.return_value = ['BTCUSDT', 'ETHUSDT']

        # Mock the load_or_fetch_data and update_data functions
        mock_load_or_fetch_data.return_value = ['BTCUSDT', 'ETHUSDT']
        mock_update_data.return_value = ['BTCUSDT', 'ETHUSDT']

        # Mock the get_valid_pairs function
        mock_get_valid_pairs.return_value = ['BTCUSDT']

        result = get_all_trading_pairs()

        # Assert that the BinanceClient was initialized
        mock_BinanceClient.assert_called_once()

        # Assert that the load_or_fetch_data and update_data functions were called with the correct arguments
        mock_load_or_fetch_data.assert_called_once_with('trading_pairs.json', mock_client.get_trading_pairs)
        mock_update_data.assert_any_call('trading_pairs.json', ['BTCUSDT', 'ETHUSDT'], mock_client.get_trading_pairs)
        mock_update_data.assert_any_call('valid_pairs.json', ['BTCUSDT'], get_valid_pairs)

        # Assert that the get_valid_pairs function was called with the correct argument
        mock_get_valid_pairs.assert_called_once_with(['BTCUSDT', 'ETHUSDT'])

        # Assert that the function returned the correct result
        self.assertEqual(result, ['BTCUSDT'])

if __name__ == '__main__':
    unittest.main()