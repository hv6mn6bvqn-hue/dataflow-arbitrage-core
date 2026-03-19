# connectors/crypto/binance.py
import requests

class Connector:
    def __init__(self):
        self.name = "binance"
        self.base_url = "https://api.binance.com/api/v3"

    def get_tickers(self):
        try:
            r = requests.get(f"{self.base_url}/ticker/price")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[BINANCE] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[BINANCE] placing {side} {quantity} {symbol} at {price}")
        return {"id": "TEST_BINANCE"}