import requests

class Connector:
    BASE_URL = "https://api.kraken.com/0/public"

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[KRAKEN] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"KRAKEN_{symbol}_{side}"}

    def fetch_tickers(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/Ticker?pair=ETHUSD,BTCUSD", timeout=5)
            resp.raise_for_status()
            return resp.json().get("result", {})
        except Exception as e:
            print(f"[KRAKEN] request error: {e}")
            return {}