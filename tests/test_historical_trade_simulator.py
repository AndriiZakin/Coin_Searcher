import asyncio
from datetime import datetime
from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from simulation.historical_trade_simulator import HistoricalTradeSimulator

class TestHistoricalTradeSimulator(TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.symbol = "BTCUSDT"
        self.start_time = 1630000000000
        self.amount_usd = 1000
        self.target_price = 50000

    def test_simulate_trade_coin_not_exist(self):
        # Simulate the case where the coin does not exist at the given start time
        self.client.get_historical_klines.return_value = []
        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        simulator.simulate_trade()
        self.logger.error.assert_called_with(f"The coin {self.symbol} did not exist at the given start time.")

    def test_simulate_trade_target_price_reached(self):
        # Simulate the case where the target price is reached
        klines = [
            [1630000000000, "40000", "41000", "39000", "40500"],
            [1630003600000, "40500", "41500", "40000", "41000"],
            [1630007200000, "41000", "42000", "40500", "41500"],
            [1630010800000, "41500", "42500", "41000", "42000"],
            [1630014400000, "42000", "43000", "41500", "42500"],
        ]
        self.client.get_historical_klines.return_value = klines
        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        simulator.simulate_trade()
        self.logger.info.assert_called_with(f"Simulated selling 0.024691358024691357 BTCUSDT at 42500.0 on {datetime.fromtimestamp(1630014400000 / 1000)}...")

    def test_simulate_trade_target_price_not_reached(self):
        # Simulate the case where the target price is not reached
        klines = [
            [1630000000000, "40000", "41000", "39000", "40500"],
            [1630003600000, "40500", "41500", "40000", "41000"],
            [1630007200000, "41000", "42000", "40500", "41500"],
            [1630010800000, "41500", "42500", "41000", "42000"],
            [1630014400000, "42000", "43000", "41500", "42000"],
        ]
        self.client.get_historical_klines.return_value = klines
        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        new_amount_usd = simulator.simulate_trade()
        self.logger.info.assert_called_with("Target price not reached in historical data, continuing with real-time data...")
        self.assertEqual(new_amount_usd, 10370.37037037037)

class TestHistoricalTradeSimulatorAsync(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = MagicMock()
        self.logger = MagicMock()
        self.symbol = "BTCUSDT"
        self.start_time = 1630000000000
        self.amount_usd = 1000
        self.target_price = 50000

    async def test_simulate_trade_coin_not_exist(self):
        # Simulate the case where the coin does not exist at the given start time
        self.client.get_historical_klines.return_value = []
        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        await simulator.simulate_trade()
        self.logger.error.assert_called_with(f"The coin {self.symbol} did not exist at the given start time.")

    async def test_simulate_trade_target_price_reached(self):
        # Simulate the case where the target price is reached
        klines = [
            [1630000000000, "40000", "41000", "39000", "40500"],
            [1630003600000, "40500", "41500", "40000", "41000"],
            [1630007200000, "41000", "42000", "40500", "41500"],
            [1630010800000, "41500", "42500", "41000", "42000"],
            [1630014400000, "42000", "43000", "41500", "42500"],
        ]
        self.client.get_historical_klines.return_value = klines
        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        await simulator.simulate_trade()
        self.logger.info.assert_called_with(f"Simulated selling 0.024691358024691357 BTCUSDT at 42500.0 on {datetime.fromtimestamp(1630014400000 / 1000)}...")

    async def test_simulate_trade_target_price_not_reached(self):
        # Simulate the case where the target price is not reached
        klines = [
            [1630000000000, "40000", "41000", "39000", "40500"],
            [1630003600000, "40500", "41500", "40000", "41000"],
            [1630007200000, "41000", "42000", "40500", "41500"],
            [1630010800000, "41500", "42500", "41000", "42000"],
            [1630014400000, "42000", "43000", "41500", "42000"],
        ]
        self.client.get_historical_klines.return_value = klines
        simulator = HistoricalTradeSimulator(self.client, self.logger, self.symbol, self.start_time, self.amount_usd, self.target_price)
        new_amount_usd = await simulator.simulate_trade()
        self.logger.info.assert_called_with("Target price not reached in historical data, continuing with real-time data...")
        self.assertEqual(new_amount_usd, 10370.37037037037)