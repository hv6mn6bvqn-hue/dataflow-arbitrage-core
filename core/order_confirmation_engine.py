# core/order_confirmation_engine.py
import json
import os

INPUT_FILE = "sources/routed_signals.json"
OUTPUT_FILE = "sources/confirmed_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[CONFIRMATION] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        s["confirmed"] = True

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[CONFIRMATION] confirmed: {len(signals)}")

if __name__ == "__main__":
    print("[CONFIRMATION] start")
    run()