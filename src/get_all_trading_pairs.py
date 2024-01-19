import json
from binance import BinanceClient
from criterias import meets_criterias

def load_or_fetch_data(filename, fetch_func):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = fetch_func()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    return data

def update_data(filename, data, fetch_func):
    try:
        with open(filename, 'r') as f:
            old_data = json.load(f)
        new_data = list(set(data) - set(old_data))
        data += new_data
    except FileNotFoundError:
        data = fetch_func()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    return data

def get_valid_pairs(pairs):
    return [pair for pair in pairs if meets_criterias(pair)]

def get_all_trading_pairs():
    """
    Fetches all trading pairs from Binance exchange, updates the data files,
    and returns a list of valid trading pairs.

    Returns:
        list: A list of valid trading pairs.
    """
    client = BinanceClient()
    fetch_func = client.get_trading_pairs

    trading_pairs = load_or_fetch_data('trading_pairs.json', fetch_func)
    trading_pairs = update_data('trading_pairs.json', trading_pairs, fetch_func)

    valid_pairs = get_valid_pairs(trading_pairs)
    valid_pairs = update_data('valid_pairs.json', valid_pairs, get_valid_pairs)

    return valid_pairs