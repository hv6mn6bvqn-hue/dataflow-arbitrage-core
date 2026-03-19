import requests

class Connector:
    def __init__(self):
        self.name = "Binance"
        self.base_url = "https://api.binance.com/api/v3/ticker/price"

    def get_snapshot(self):
        try:
            resp = requests.get(self.base_url, timeout=5)
            data = resp.json()
            return [{"symbol": d["symbol"], "price": float(d["price"])} for d in data]
        except Exception as e:
            print(f"[BINANCE] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        # Здесь можно симулировать order_id
        print(f"[BINANCE] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{symbol}-{side}-test"}