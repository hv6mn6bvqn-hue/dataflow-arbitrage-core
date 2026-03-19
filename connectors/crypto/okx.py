# connectors/crypto/okx.py
import requests

class Connector:
    def __init__(self):
        self.name = "okx"
        self.base_url = "https://www.okx.com/api/spot/v3"

    def get_tickers(self):
        try:
            r = requests.get(f"{self.base_url}/instruments/ticker")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[OKX] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[OKX] placing {side} {quantity} {symbol} at {price}")
        return {"id": "TEST_OKX"}