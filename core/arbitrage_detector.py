# core/arbitrage_detector.py
import json
import os

INPUT_FILE = "sources/triangular_opportunities.json"
OUTPUT_FILE = "sources/arbitrage_opportunities.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[ARBITRAGE] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    detected = []
    for s in signals:
        if s.get("tri_arb", False):
            s["arbitrage"] = True
            detected.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(detected, f)

    print(f"[ARBITRAGE] matrix loaded: {len(signals)}")
    print(f"[ARBITRAGE] opportunities found: {len(detected)}")
    print(f"[ARBITRAGE] opportunities saved: {len(detected)}")

if __name__ == "__main__":
    print("[ARBITRAGE] loading matrix opportunities")
    run()