import json
from Searcher.src.binance_work import BinanceClient
from Searcher.src.criterias import meets_criterias

def load_valid_data(filename, data):
    try:
        with open(filename, 'r') as f:
            old_data = json.load(f)
        combined_data = list(set(old_data).union(set(data)))
        with open(filename, 'w') as f:
            json.dump(combined_data, f, indent=4)
    except FileNotFoundError:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
def update_data(filename, fetch_func):
    try:
        with open(filename, 'r') as f:
            old_data = set(json.load(f))
        data = set(fetch_func())
        new_data = list(data - old_data)
        data = list(old_data.union(new_data))
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
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

    trading_pairs = update_data('trading_pairs.json', fetch_func)

    valid_pairs = get_valid_pairs(trading_pairs)
    load_valid_data('valid_pairs.json', valid_pairs)

if __name__ == '__main__':
    get_all_trading_pairs()