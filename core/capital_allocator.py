# core/capital_allocator.py
import json
import os

INPUT_FILE = "sources/recovered_signals.json"
OUTPUT_FILE = "sources/allocated_signals.json"

CAPITAL = 10000

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[CAPITAL_FRAGMENT] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        s["allocated"] = CAPITAL / max(len(signals), 1)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[CAPITAL_FRAGMENT] fragmented: {len(signals)}")

if __name__ == "__main__":
    print("[CAPITAL_FRAGMENT] start")
    run()