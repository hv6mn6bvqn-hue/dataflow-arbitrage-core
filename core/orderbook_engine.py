import json
import os

INPUT_FILE = "sources/fee_filtered_signals.json"
OUTPUT_FILE = "sources/orderbook_signals.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[ORDERBOOK] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("[ORDERBOOK] invalid format")
            return []

        return data

    except Exception as e:
        print(f"[ORDERBOOK] load error: {e}")
        return []


def enrich(signals):

    enriched = []

    for signal in signals:

        spread = signal.get("spread_pct", 0)

        liquidity_score = 0.5

        if spread >= 0.02:
            liquidity_score = 0.9
        elif spread >= 0.01:
            liquidity_score = 0.7

        signal["liquidity_score"] = liquidity_score
        signal["orderbook_depth"] = 100000

        enriched.append(signal)

    return enriched


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[ORDERBOOK] signals saved: {len(data)}")
    print(f"[ORDERBOOK] file: {OUTPUT_FILE}")


def main():

    print("[ORDERBOOK] orderbook engine start")

    signals = load_signals()

    enriched = enrich(signals)

    save_signals(enriched)


if __name__ == "__main__":
    main()