import json
import unittest
from unittest.mock import patch

from get_trading_pairs import get_all_trading_pairs

class TestGetAllTradingPairs(unittest.TestCase):
    @patch('get_trading_pairs.get_exchange_info')
    def test_get_all_trading_pairs(self, mock_get_exchange_info):
        # Mock the return value of get_exchange_info
        mock_get_exchange_info.return_value = {
            'symbols': [
                {
                    'symbol': 'BTCUSDT',
                    'baseAsset': 'BTC',
                    'quoteAsset': 'USDT',
                    'status': 'TRADING',
                    'baseAssetPrecision': 8,
                    'quoteAssetPrecision': 2
                },
                {
                    'symbol': 'ETHUSDT',
                    'baseAsset': 'ETH',
                    'quoteAsset': 'USDT',
                    'status': 'TRADING',
                    'baseAssetPrecision': 8,
                    'quoteAssetPrecision': 2
                }
            ]
        }

        # Call the function
        get_all_trading_pairs()

        # Verify that the file is created and contains the expected data
        with open('all_trading_pairs.json', 'r') as file:
            trading_pairs_info = json.load(file)
            self.assertEqual(trading_pairs_info, [
                {
                    'symbol': 'BTCUSDT',
                    'baseAsset': 'BTC',
                    'quoteAsset': 'USDT',
                    'status': 'TRADING',
                    'baseAssetPrecision': 8,
                    'quoteAssetPrecision': 2
                },
                {
                    'symbol': 'ETHUSDT',
                    'baseAsset': 'ETH',
                    'quoteAsset': 'USDT',
                    'status': 'TRADING',
                    'baseAssetPrecision': 8,
                    'quoteAssetPrecision': 2
                }
            ])

if __name__ == '__main__':
    unittest.main()