from get_all_trading_pairs import get_all_trading_pairs
import time 

def main():
    while True:
        get_all_trading_pairs()
        time.sleep(60 * 60 * 24)


if __name__ == '__main__':
    main()