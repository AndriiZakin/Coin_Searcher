from binance import BinanceClient

class TradingPair:
    def __init__(self, trading_pair):
        self.trading_pair = trading_pair

    def meets_criteria(self):
        if self.trading_pair['status'] != 'TRADING':
            return False

        if not (self.trading_pair['volume'] > 10000 and self.trading_pair['liquidity'] > 10000):
            return False

        if not float(self.trading_pair['priceChangePercent']) > 10:
            return False
        
        return True

    

def meets_criterias(symbol):
    fetcher = BinanceClient()
    trading_pair = fetcher.get_symbol_data(symbol)

    if trading_pair is None:
        return False

    trading_pair = TradingPair(trading_pair)
    return trading_pair.meets_criteria()



'''# Check if the trading pair has price patterns and trends
        # Placeholder: Replace with actual analysis
        if not True:
            return False

        # Check if the trading pair has good historical performance
        # Placeholder: Replace with actual analysis
        if not True:
            return False

        # Check if the trading pair has positive fundamental analysis
        # Placeholder: Replace with actual analysis
        if not True:
            return False

        # Check if the trading pair has positive technical indicators
        # Placeholder: Replace with actual analysis
        if not True:
            return False

        # If all checks passed, return True
        return True'''