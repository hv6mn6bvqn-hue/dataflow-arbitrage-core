# connectors/crypto/kucoin.py
import requests

class Connector:
    def __init__(self):
        self.name = "kucoin"
        self.base_url = "https://api.kucoin.com/api/v1"

    def get_tickers(self):
        try:
            r = requests.get(f"{self.base_url}/market/allTickers")
            r.raise_for_status()
            data = r.json()
            return data.get("data", {}).get("ticker", [])
        except Exception as e:
            print(f"[KUCOIN] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[KUCOIN] placing {side} {quantity} {symbol} at {price}")
        return {"id": "TEST_KUCOIN"}