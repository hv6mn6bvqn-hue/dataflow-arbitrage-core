# core/orderbook_engine.py
import json
import os

INPUT_FILE = "sources/fee_filtered_signals.json"
OUTPUT_FILE = "sources/orderbook_signals.json"

def enrich_signal(signal):
    # пример enrichment: добавление текущих bid/ask с биржи
    signal["orderbook"] = {
        "bid": signal.get("best_bid", 0),
        "ask": signal.get("best_ask", 0)
    }
    return signal

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ORDERBOOK] input missing, file: {INPUT_FILE}")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    with open(INPUT_FILE, "r") as f:
        signals = json.load(f)

    enriched = [enrich_signal(s) for s in signals]
    with open(OUTPUT_FILE, "w") as f:
        json.dump(enriched, f, indent=2)

    print(f"[ORDERBOOK] signals saved: {len(enriched)}")

if __name__ == "__main__":
    main()