import json
import os
from core.exchange_loader import load_connectors

INPUT_FILE = "sources/live_routed.json"
OUTPUT_FILE = "sources/live_confirmed.json"

def run():
    connectors = load_connectors()

    if not os.path.exists(INPUT_FILE):
        print("[CONFIRMATION] input file missing")
        signals = []
    else:
        with open(INPUT_FILE, "r") as f:
            signals = json.load(f)

    confirmed_signals = []
    for s in signals:
        ex_name = s.get("exchange")
        connector = connectors.get(ex_name)
        if not connector or not s.get("routed"):
            s["confirmed"] = False
            s["error"] = s.get("error", "not routed or unknown exchange")
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

    print(f"[CONFIRMATION] confirmed: {len([s for s in confirmed_signals if s.get('confirmed')])}")

if __name__ == "__main__":
    run()