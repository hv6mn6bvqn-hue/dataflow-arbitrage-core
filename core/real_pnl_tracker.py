# core/real_pnl_tracker.py
import json
import os

INPUT_FILE = "sources/confirmed_signals.json"
OUTPUT_FILE = "sources/pnl_tracked.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[REAL_PNL] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Для простоты: PnL = (executed_price - target_price) * size
        s["pnl"] = (s.get("fill_price", 0) - s.get("price", 0)) * s.get("size", 0)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[REAL_PNL] tracked: {len(signals)}")

if __name__ == "__main__":
    print("[REAL_PNL] start")
    run()