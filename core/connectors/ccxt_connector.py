import ccxt
import time

class Connector:
    def __init__(self):
        # Список бирж для нашей стратегии
        self.exchanges = {
            "binance": ccxt.binance(),
            "kraken": ccxt.kraken(),
            "coinbase": ccxt.coinbasepro(),
            "kucoin": ccxt.kucoin(),
            # сюда можно добавить другие биржи
        }

    def fetch_tickers(self):
        all_tickers = {}
        for name, exchange in self.exchanges.items():
            try:
                tickers = exchange.fetch_tickers()
                all_tickers[name] = tickers
            except Exception as e:
                print(f"[{name}] fetch error: {str(e)}")
                all_tickers[name] = {}
            time.sleep(0.2)  # чтобы не попасть в rate limit
        return all_tickers