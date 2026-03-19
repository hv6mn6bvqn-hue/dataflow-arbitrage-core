import requests

class Connector:
    def __init__(self):
        self.name = "Kraken"
        self.base_url = "https://api.kraken.com/0/public/Ticker?pair=ETHUSD,BTCUSD"

    def get_snapshot(self):
        try:
            resp = requests.get(self.base_url, timeout=5)
            result = resp.json().get("result", {})
            snapshots = []
            for k, v in result.items():
                snapshots.append({"symbol": k, "price": float(v["c"][0])})
            return snapshots
        except Exception as e:
            print(f"[KRAKEN] request error: {e}")
            return []

    def place_order(self, symbol, side, quantity, price=None):
        print(f"[KRAKEN] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{symbol}-{side}-test"}