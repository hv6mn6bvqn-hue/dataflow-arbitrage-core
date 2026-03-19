import requests

class Connector:
    def __init__(self):
        self.name = "Coinbase"
        self.base_url = "https://api.exchange.coinbase.com/products/ticker"

    def get_snapshot(self):
        symbols = ["BTC-USD","ETH-USD"]  # можно расширить
        snapshots = []
        try:
            for s in symbols:
                resp = requests.get(f"https://api.exchange.coinbase.com/products/{s}/ticker", timeout=5)
                d = resp.json()
                snapshots.append({"symbol": s, "price": float(d["price"])})
            return snapshots
        except Exception as e:
            print(f"[COINBASE] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[COINBASE] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{symbol}-{side}-test"}