# connectors/crypto/kraken.py
import requests

class Connector:
    def __init__(self):
        self.name = "kraken"
        self.base_url = "https://api.kraken.com/0/public"

    def get_tickers(self):
        try:
            r = requests.get(f"{self.base_url}/Ticker?pair=BTCUSD,ETHUSD")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[KRAKEN] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[KRAKEN] placing {side} {quantity} {symbol} at {price}")
        return {"id": "TEST_KRAKEN"}