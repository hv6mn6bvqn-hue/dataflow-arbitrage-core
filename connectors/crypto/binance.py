class Connector:
    def place_order(self, symbol, side, quantity, price=None):
        print(f"[BINANCE] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"binance-{symbol}-{side}"}

    def check_order(self, order_id):
        return {"filled": True}