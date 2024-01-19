# src/main.py
import json
from get_trading_pairs import get_all_trading_pairs
from binance import BinanceClient
import time

def main():
    while True:
        # Fetch all trading pairs and save them to a JSON file
        get_all_trading_pairs()

        with open('all_trading_pairs.json', 'r') as file:
            all_trading_pairs = json.load(file)


        # Sleep for a day (adjust the duration as needed)
        time.sleep(24 * 60 * 60)  # Sleep for 24 hours

if __name__ == '__main__':
    main()
