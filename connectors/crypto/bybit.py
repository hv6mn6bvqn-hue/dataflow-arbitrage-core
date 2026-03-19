import requests

class Connector:
    BASE_URL = "https://api.bybit.com/v2/public"

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[BYBIT] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"BYBIT_{symbol}_{side}"}

    def fetch_tickers(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/tickers", timeout=5)
            resp.raise_for_status()
            return resp.json().get("result", [])
        except Exception as e:
            print(f"[BYBIT] request error: {e}")
            return []