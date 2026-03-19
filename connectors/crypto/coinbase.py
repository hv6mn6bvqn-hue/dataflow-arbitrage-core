import requests

class Connector:
    BASE_URL = "https://api.exchange.coinbase.com"

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[COINBASE] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"COINBASE_{symbol}_{side}"}

    def fetch_tickers(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/products/ticker", timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"[COINBASE] request error: {e}")
            return []