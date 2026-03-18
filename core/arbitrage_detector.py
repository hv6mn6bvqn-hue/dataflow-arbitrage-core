import json
import os

INPUT_FILE = "sources/matrix_opportunities.json"
OUTPUT_FILE = "sources/arbitrage_opportunities.json"

MIN_SPREAD = 0.001


def load_matrix():

    if not os.path.exists(INPUT_FILE):
        print("[ARBITRAGE] matrix file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[ARBITRAGE] matrix loaded:", len(data))

    return data


def extract_spread(item):

    candidates = [
        item.get("spread"),
        item.get("spread_pct"),
        item.get("profit"),
        item.get("net_spread"),
        item.get("margin")
    ]

    for value in candidates:
        if isinstance(value, (int, float)):
            return value

    return 0


def normalize_signal(item, spread):

    item["spread"] = spread

    if "buy_exchange" not in item:
        item["buy_exchange"] = item.get("exchange_a", "unknown")

    if "sell_exchange" not in item:
        item["sell_exchange"] = item.get("exchange_b", "unknown")

    return item


def filter_opportunities(matrix):

    opportunities = []

    for m in matrix:

        spread = extract_spread(m)

        if spread > MIN_SPREAD:
            m = normalize_signal(m, spread)
            opportunities.append(m)

    return opportunities


def save_opportunities(opps):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(opps, f, indent=2)

    print("[ARBITRAGE] opportunities saved:", len(opps))


def run():

    print("[ARBITRAGE] loading matrix opportunities")

    matrix = load_matrix()

    opportunities = filter_opportunities(matrix)

    print("[ARBITRAGE] opportunities found:", len(opportunities))

    save_opportunities(opportunities)


def main():
    run()