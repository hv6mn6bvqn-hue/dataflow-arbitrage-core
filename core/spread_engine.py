import json
import os
from collections import defaultdict

INPUT_FILE = "sources/signals.json"
OUTPUT_FILE = "sources/spread_opportunities.json"

MIN_SPREAD = 0.002


def load_data():

    if not os.path.exists(INPUT_FILE):
        print("[SPREAD] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[SPREAD] loaded:", len(data))
    return data


def group_by_symbol(data):

    grouped = defaultdict(list)

    for item in data:

        symbol = item.get("symbol")
        price = item.get("price")
        exchange = item.get("exchange")

        if not symbol or not price or not exchange:
            continue

        grouped[symbol].append(item)

    return grouped


def detect_spreads(grouped):

    spreads = []

    for symbol, entries in grouped.items():

        if len(entries) < 2:
            continue

        entries = sorted(entries, key=lambda x: x["price"])

        low = entries[0]
        high = entries[-1]

        spread = (high["price"] - low["price"]) / low["price"]

        if spread >= MIN_SPREAD:

            spreads.append({
                "symbol": symbol,
                "exchange_a": low["exchange"],
                "exchange_b": high["exchange"],
                "price_a": low["price"],
                "price_b": high["price"],
                "spread": spread
            })

    return spreads


def save_spreads(spreads):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(spreads, f, indent=2)

    print("[SPREAD] saved:", len(spreads))


def run():

    print("[SPREAD] engine start")

    data = load_data()

    grouped = group_by_symbol(data)

    spreads = detect_spreads(grouped)

    print("[SPREAD] opportunities:", len(spreads))

    save_spreads(spreads)


def main():
    run()


if __name__ == "__main__":
    main()