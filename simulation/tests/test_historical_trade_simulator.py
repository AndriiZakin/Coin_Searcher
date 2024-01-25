import unittest
from unittest.mock import MagicMock
from simulation.historical_trade_simulator import HistoricalTradeSimulator

class TestHistoricalTradeSimulator(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.symbol = 'BTCUSDT'
        self.start_time = '2022-01-01'
        self.amount_usd = 1000
        self.target_price = 2000

    def test_simulate_trade_target_reached(self):
        # Mock the get_historical_klines method to return a list of klines
        self.client.get_historical_klines.return_value = [
            ['timestamp', '1000', '2000', '800', '1500'],
            ['timestamp', '1500', '2500', '1200', '1800'],
            ['timestamp', '1800', '3000', '1500', '2200']
        ]

        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        result = simulator.simulate_trade()

        # Assert that the logger was called with the correct messages
        self.logger.info.assert_called_with("Simulating buying 0.5 BTCUSDT for 1000 USD at 1000...")
        self.logger.info.assert_called_with("Simulated selling 0.5 BTCUSDT at 2200...")

        # Assert that the result is None since the target price was reached
        self.assertIsNone(result)

    def test_simulate_trade_target_not_reached(self):
        # Mock the get_historical_klines method to return a list of klines
        self.client.get_historical_klines.return_value = [
            ['timestamp', '1000', '2000', '800', '1500'],
            ['timestamp', '1500', '2500', '1200', '1800'],
            ['timestamp', '1800', '3000', '1500', '1900']
        ]

        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        result = simulator.simulate_trade()

        # Assert that the logger was called with the correct messages
        self.logger.info.assert_called_with("Simulating buying 0.5 BTCUSDT for 1000 USD at 1000...")
        self.logger.info.assert_called_with("Target price not reached in historical data, continuing with real-time data...")

        # Assert that the result is the new amount in USD
        self.assertEqual(result, 950)

if __name__ == '__main__':
    unittest.main()