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
        if not s.get("routed"):
            s["confirmed"] = False
            s["error"] = "not routed"
            confirmed_signals.append(s)
            continue

        ex = s.get("exchange")
        connector = connectors.get(ex)
        if not connector:
            s["confirmed"] = False
            s["error"] = f"unknown exchange {ex}"
            confirmed_signals.append(s)
            continue

        try:
            status = connector.check_order_status(s["order_id"])
            s["confirmed"] = status.get("filled", False)
            s["filled_qty"] = status.get("filled_qty", 0)
        except Exception as e:
            s["confirmed"] = False
            s["error"] = str(e)

        confirmed_signals.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(confirmed_signals, f, indent=2)

    print(f"[CONFIRMATION] confirmed: {len(confirmed_signals)}")

if __name__ == "__main__":
    run()