import requests

class Connector:
    BASE_URL = "https://www.okx.com/api/spot/v3"

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[OKX] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"OKX_{symbol}_{side}"}

    def fetch_tickers(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/instruments/ticker", timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"[OKX] request error: {e}")
            return []