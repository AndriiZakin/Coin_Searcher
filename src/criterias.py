

def meets_criteria(trading_pair):
    # Check if the trading pair is currently trading
    if trading_pair['status'] != 'TRADING':
        return False

    # Check if the base asset precision is 8
    if trading_pair['baseAssetPrecision'] != 8:
        return False

    # Check if the quote asset is USDT
    if trading_pair['quoteAsset'] != 'USDT':
        return False

    # Check if the price change in the last 24 hours is more than 10%
    if float(trading_pair['priceChangePercent']) < 10:
        return False

    # If all checks pass, return True
    return True