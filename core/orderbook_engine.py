# core/orderbook_engine.py
import json
import os

INPUT_FILE = "sources/signals.json"
OUTPUT_FILE = "sources/orderbook_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print(f"[ORDERBOOK] input missing")
        signals = []
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    enriched = []
    for s in signals:
        s["orderbook"] = {"bid": s.get("price", 0)*0.99, "ask": s.get("price", 0)*1.01}
        enriched.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(enriched, f)

    print(f"[ORDERBOOK] signals enriched: {len(enriched)}")
    print(f"[ORDERBOOK] signals saved: {len(enriched)}")
    print(f"[ORDERBOOK] file: {OUTPUT_FILE}")

if __name__ == "__main__":
    print("[ORDERBOOK] orderbook engine start")
    run()