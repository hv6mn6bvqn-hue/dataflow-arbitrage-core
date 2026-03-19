# core/fill_probability_engine.py
import json
import os

INPUT_FILE = "sources/arbitrage_opportunities.json"
OUTPUT_FILE = "sources/fill_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[FILL] input file missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    filled = []
    for s in signals:
        s["fill_prob"] = 1.0  # максимально упрощённо для live
        filled.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(filled, f)

    print(f"[FILL] loaded: {len(filled)}")
    print(f"[FILL] scored: {len(filled)}")

if __name__ == "__main__":
    print("[FILL] start")
    run()