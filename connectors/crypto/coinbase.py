# connectors/crypto/coinbase.py
import requests

class Connector:
    def __init__(self):
        self.name = "coinbase"
        self.base_url = "https://api.exchange.coinbase.com"

    def get_tickers(self):
        try:
            r = requests.get(f"{self.base_url}/products")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[COINBASE] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[COINBASE] placing {side} {quantity} {symbol} at {price}")
        return {"id": "TEST_COINBASE"}