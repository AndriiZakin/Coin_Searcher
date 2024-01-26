import unittest
from unittest.mock import MagicMock
from simulation.real_time_trade_simulator import RealTimeTradeSimulator

class TestRealTimeTradeSimulator(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.symbol = 'BTCUSDT'
        self.target_price = 50000
        self.amount_usd = 1000
        self.simulator = RealTimeTradeSimulator(self.client, self.logger, self.symbol, self.target_price, self.amount_usd)

    def test_process_message(self):
        msg = {'e': 'trade', 'p': '48000'}
        self.simulator.quantity = 10
        self.simulator.conn_key = 'test_conn_key'

        # Test when the message is not an error
        self.simulator.process_message(msg)

        self.logger.info.assert_called_with("Current price of BTCUSDT: 48000")
        self.logger.info.assert_called_with("Simulating selling 10 BTCUSDT at 48000...")
        self.simulator.bm.stop_socket.assert_called_with('test_conn_key')

        # Test when the message is an error
        msg = {'e': 'error', 'm': 'An error occurred'}
        self.simulator.process_message(msg)

        self.logger.error.assert_called_with("An error occurred")

    def test_simulate_trade(self):
        ticker = {'price': '48000'}
        self.client.get_symbol_ticker.return_value = ticker

        self.simulator.simulate_trade()

        self.client.get_symbol_ticker.assert_called_with(symbol='BTCUSDT')
        self.logger.info.assert_called_with("Simulating buying 0.020833333333333332 BTCUSDT for 1000 USD at 48000...")
        self.simulator.bm.start_symbol_ticker_socket.assert_called_with('BTCUSDT', self.simulator.process_message)
        self.simulator.bm.start.assert_called()

if __name__ == '__main__':
    unittest.main()