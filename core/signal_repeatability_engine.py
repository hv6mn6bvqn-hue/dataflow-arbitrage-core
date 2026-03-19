# core/signal_repeatability_engine.py
import json
import os

INPUT_FILE = "sources/orderbook_signals.json"
OUTPUT_FILE = "sources/repeat_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print("[REPEAT] input missing")
        signals = []
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    repeated = []
    for s in signals:
        s["repeatable"] = True
        repeated.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(repeated, f)

    print(f"[REPEAT] processed: {len(repeated)}")
    print(f"[REPEAT] file: {OUTPUT_FILE}")

if __name__ == "__main__":
    print("[REPEAT] start")
    run()