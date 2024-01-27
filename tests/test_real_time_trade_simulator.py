import asyncio
from datetime import datetime
from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from simulation.real_time_trade_simulator import RealTimeTradeSimulator

class TestRealTimeTradeSimulator(TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.symbol = "BTCUSDT"
        self.target_price = 50000
        self.amount_usd = 1000

    def test_simulate_trade_target_price_reached(self):
        # Simulate the case where the target price is reached
        ticker = {'price': '50000'}
        self.client.get_symbol_ticker.return_value = ticker
        simulator = RealTimeTradeSimulator(self.client, self.logger, self.symbol, self.target_price, self.amount_usd)
        simulator.process_message = MagicMock()
        simulator.simulate_trade()
        self.logger.info.assert_called_with(f"Simulating buying 0.02 BTCUSDT for 1000 USD at 50000.0...")
        simulator.process_message.assert_called_with({'e': 'error'})

    def test_simulate_trade_target_price_not_reached(self):
        # Simulate the case where the target price is not reached
        ticker = {'price': '40000'}
        self.client.get_symbol_ticker.return_value = ticker
        simulator = RealTimeTradeSimulator(self.client, self.logger, self.symbol, self.target_price, self.amount_usd)
        simulator.process_message = MagicMock()
        simulator.simulate_trade()
        self.logger.info.assert_called_with(f"Simulating buying 0.025 BTCUSDT for 1000 USD at 40000.0...")
        simulator.process_message.assert_called_with({'e': 'error'})

class TestRealTimeTradeSimulatorAsync(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.symbol = "BTCUSDT"
        self.target_price = 50000
        self.amount_usd = 1000

    async def test_simulate_trade_target_price_reached(self):
        # Simulate the case where the target price is reached
        ticker = {'price': '50000'}
        self.client.get_symbol_ticker.return_value = ticker
        simulator = RealTimeTradeSimulator(self.client, self.logger, self.symbol, self.target_price, self.amount_usd)
        simulator.process_message = MagicMock()
        await simulator.simulate_trade()
        self.logger.info.assert_called_with(f"Simulating buying 0.02 BTCUSDT for 1000 USD at 50000.0...")
        simulator.process_message.assert_called_with({'e': 'error'})

    async def test_simulate_trade_target_price_not_reached(self):
        # Simulate the case where the target price is not reached
        ticker = {'price': '40000'}
        self.client.get_symbol_ticker.return_value = ticker
        simulator = RealTimeTradeSimulator(self.client, self.logger, self.symbol, self.target_price, self.amount_usd)
        simulator.process_message = MagicMock()
        await simulator.simulate_trade()
        self.logger.info.assert_called_with(f"Simulating buying 0.025 BTCUSDT for 1000 USD at 40000.0...")
        simulator.process_message.assert_called_with({'e': 'error'})