import requests

class Connector:
    def __init__(self):
        self.name = "KuCoin"
        self.base_url = "https://api.kucoin.com/api/v1/market/allTickers"

    def get_snapshot(self):
        try:
            resp = requests.get(self.base_url, timeout=5)
            data = resp.json().get("data", {}).get("ticker", [])
            return [{"symbol": d["symbol"], "price": float(d["last"])} for d in data]
        except Exception as e:
            print(f"[KUCOIN] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[KUCOIN] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{symbol}-{side}-test"}