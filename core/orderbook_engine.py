import json
import os

INPUT_FILE = "sources/arbitrage_after_fees.json"
OUTPUT_FILE = "sources/orderbook_ready.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[ORDERBOOK] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def enrich(signals):

    enriched = []

    for s in signals:
        s["orderbook_depth"] = 1.0
        s["liquidity_score"] = 1.0
        enriched.append(s)

    return enriched


def save(signals):

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[ORDERBOOK] signals saved:", len(signals))


def run():

    print("[ORDERBOOK] orderbook engine start")

    signals = load_signals()

    enriched = enrich(signals)

    print("[ORDERBOOK] signals enriched:", len(enriched))

    save(enriched)


def main():
    run()


if __name__ == "__main__":
    main()