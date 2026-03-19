import requests

class Connector:
    def __init__(self):
        self.name = "Bybit"
        self.base_url = "https://api.bybit.com/v2/public/tickers"

    def get_snapshot(self):
        try:
            resp = requests.get(self.base_url, timeout=5)
            data = resp.json().get("result", [])
            return [{"symbol": d["symbol"], "price": float(d["last_price"])} for d in data]
        except Exception as e:
            print(f"[BYBIT] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[BYBIT] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{symbol}-{side}-test"}