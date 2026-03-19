# connectors/crypto/bybit.py
import requests

class Connector:
    def __init__(self):
        self.name = "bybit"
        self.base_url = "https://api.bybit.com/v2/public"

    def get_tickers(self):
        try:
            r = requests.get(f"{self.base_url}/tickers")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[BYBIT] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[BYBIT] placing {side} {quantity} {symbol} at {price}")
        return {"id": "TEST_BYBIT"}