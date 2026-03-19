# core/fee_engine.py
import json
import os

INPUT_FILE = "sources/orderbook_signals.json"
OUTPUT_FILE = "sources/fee_filtered_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print(f"[FEES] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    filtered = []
    for s in signals:
        fee = s.get("price", 0) * 0.001
        if fee < s.get("price", 0):
            s["fee"] = fee
            filtered.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(filtered, f)

    print(f"[FEES] signals saved: {len(filtered)}")
    print(f"[FEES] file: {OUTPUT_FILE}")

if __name__ == "__main__":
    print("[FEES] fee engine start")
    run()