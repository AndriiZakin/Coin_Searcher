import unittest
from src.criterias import TradingPair

class TestTradingPair(unittest.TestCase):
    def setUp(self):
        self.trading_pair_data = {
            'symbol': 'BTCUSDT',
            'status': 'TRADING',
            'volume': 20000,
            'liquidity': 15000,
            'priceChangePercent': '15.0'
        }
        self.trading_pair = TradingPair(self.trading_pair_data)

    def test_meets_criteria(self):
        self.assertTrue(self.trading_pair.meets_criteria())

    def test_meets_criteria_not_trading(self):
        self.trading_pair.trading_pair['status'] = 'NOT_TRADING'
        self.assertFalse(self.trading_pair.meets_criteria())

    def test_meets_criteria_low_volume(self):
        self.trading_pair.trading_pair['volume'] = 5000
        self.assertFalse(self.trading_pair.meets_criteria())

    def test_meets_criteria_low_liquidity(self):
        self.trading_pair.trading_pair['liquidity'] = 5000
        self.assertFalse(self.trading_pair.meets_criteria())

    def test_meets_criteria_low_price_change_percent(self):
        self.trading_pair.trading_pair['priceChangePercent'] = '5.0'
        self.assertFalse(self.trading_pair.meets_criteria())

if __name__ == '__main__':
    unittest.main()