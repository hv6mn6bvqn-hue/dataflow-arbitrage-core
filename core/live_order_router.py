# core/live_order_router.py
import json
import os
from connectors import binance, bybit, coinbase, kraken, kucoin, okx

INPUT_FILE = "sources/live_export.json"
OUTPUT_FILE = "sources/live_routed.json"

EXCHANGE_MAP = {
    "binance": binance,
    "bybit": bybit,
    "coinbase": coinbase,
    "kraken": kraken,
    "kucoin": kucoin,
    "okx": okx
}

def run():
    if not os.path.exists(INPUT_FILE):
        print("[LIVE_ROUTER] input file missing")
        signals = []
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    routed_signals = []
    for s in signals:
        ex = s.get("exchange")
        if ex not in EXCHANGE_MAP:
            print(f"[LIVE_ROUTER] unknown exchange {ex}")
            continue

        connector = EXCHANGE_MAP[ex]

        try:
            # Отправка ордера на биржу
            result = connector.place_order(
                symbol=s["symbol"],
                side=s["side"],
                quantity=s["quantity"],
                price=s.get("price")
            )
            s["routed"] = True
            s["order_id"] = result.get("id", None)
        except Exception as e:
            s["routed"] = False
            s["error"] = str(e)

        routed_signals.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(routed_signals, f)

    print(f"[LIVE_ROUTER] routed: {len(routed_signals)}")

if __name__ == "__main__":
    print("[LIVE_ROUTER] start")
    run()