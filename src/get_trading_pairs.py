import json
from binance import BinanceClient
from criterias import meets_criteria

def get_all_trading_pairs():
    client = BinanceClient()
    trading_pairs = client.get_trading_pairs()
    valid_pairs = []

    for pair in trading_pairs:
        if meets_criteria(pair):
            valid_pairs.append(pair)

    with open('valid_pairs.json', 'w') as f:
        json.dump(valid_pairs, f, indent=4)
