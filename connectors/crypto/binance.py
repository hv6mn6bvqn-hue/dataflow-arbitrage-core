import requests

class Connector:
    BASE_URL = "https://api.binance.com/api/v3"

    def place_order(self, symbol, side, quantity, price=None):
        # Заглушка: здесь можно подключить реальный REST API с API ключами
        print(f"[BINANCE] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"BIN_{symbol}_{side}"}

    def fetch_tickers(self):
        try:
            resp = requests.get(f"{self.BASE_URL}/ticker/price", timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"[BINANCE] request error: {e}")
            return []