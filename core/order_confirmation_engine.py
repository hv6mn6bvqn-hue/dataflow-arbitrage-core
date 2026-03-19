# core/order_confirmation_engine.py
from core.exchange_loader import load_connectors
import json
import os

INPUT_FILE = "sources/live_routed.json"
OUTPUT_FILE = "sources/live_confirmed.json"

def run():
    connectors = load_connectors()

    if not os.path.exists(INPUT_FILE):
        print("[CONFIRMATION] input missing")
        signals = []
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    confirmed_signals = []
    for s in signals:
        ex = s.get("exchange")
        connector = connectors.get(ex)
        if not connector:
            print(f"[CONFIRMATION] unknown exchange {ex}")
            continue

        if not s.get("routed"):
            s["confirmed"] = False
            s["error"] = "Not routed"
            confirmed_signals.append(s)
            continue

        try:
            status = connector.check_order(s["order_id"])
            s["confirmed"] = status.get("filled", False)
        except Exception as e:
            s["confirmed"] = False
            s["error"] = str(e)

        confirmed_signals.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(confirmed_signals, f)

    print(f"[CONFIRMATION] confirmed: {len(confirmed_signals)}")

if __name__ == "__main__":
    run()