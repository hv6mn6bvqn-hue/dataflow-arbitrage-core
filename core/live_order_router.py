# core/live_order_router.py
import json
import os

INPUT_FILE = "sources/executed_signals.json"
OUTPUT_FILE = "sources/routed_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[LIVE_ROUTER] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Роутинг на PRIMARY/SECONDARY
        s["route"] = "PRIMARY"

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[LIVE_ROUTER] routed: {len(signals)}")

if __name__ == "__main__":
    print("[LIVE_ROUTER] start")
    run()