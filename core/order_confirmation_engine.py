# core/order_confirmation_engine.py
import json
import os
from connectors import binance, bybit, coinbase, kraken, kucoin, okx

INPUT_FILE = "sources/live_routed.json"
OUTPUT_FILE = "sources/order_confirmed.json"

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
        print("[CONFIRMATION] input missing")
        signals = []
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    confirmed_signals = []
    for s in signals:
        ex = s.get("exchange")
        if ex not in EXCHANGE_MAP or not s.get("routed"):
            s["confirmed"] = False
            confirmed_signals.append(s)
            continue

        connector = EXCHANGE_MAP[ex]

        try:
            status = connector.check_order_status(s.get("order_id"))
            s["confirmed"] = status == "FILLED"
        except Exception as e:
            s["confirmed"] = False
            s["error"] = str(e)

        confirmed_signals.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(confirmed_signals, f)

    print(f"[CONFIRMATION] confirmed: {len([s for s in confirmed_signals if s['confirmed']])}")

if __name__ == "__main__":
    print("[CONFIRMATION] start")
    run()