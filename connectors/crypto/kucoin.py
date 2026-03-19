import requests

class Connector:
    BASE_URL = "https://api.kucoin.com/api/v1"

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[KUCOIN] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"KUCOIN_{symbol}_{side}"}

    def fetch_tickers(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/market/allTickers", timeout=5)
            resp.raise_for_status()
            return resp.json().get("data", {}).get("ticker", [])
        except Exception as e:
            print(f"[KUCOIN] request error: {e}")
            return []