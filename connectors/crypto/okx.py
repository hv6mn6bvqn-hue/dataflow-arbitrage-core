import requests

class Connector:
    def __init__(self):
        self.name = "OKX"
        self.base_url = "https://www.okx.com/api/spot/v3/instruments/ticker"

    def get_snapshot(self):
        try:
            resp = requests.get(self.base_url, timeout=5)
            data = resp.json()
            return [{"symbol": d["instId"], "price": float(d["last"])} for d in data]
        except Exception as e:
            print(f"[OKX] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[OKX] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{symbol}-{side}-test"}