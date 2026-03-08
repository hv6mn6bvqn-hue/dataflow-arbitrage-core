import json
import os
from datetime import datetime

INPUT_FILE = "sources/arbitrage_matrix.json"
OUTPUT_FILE = "sources/arbitrage.json"

SPREAD_MIN = 0.004
SPREAD_MAX = 0.05


def load_matrix():

    try:

        with open(INPUT_FILE, "r") as f:

            return json.load(f)

    except Exception as e:

        print("[ARBITRAGE] load error:", e)

        return []


def filter_opportunities(matrix):

    results = []

    for m in matrix:

        spread = m.get("spread")

        if spread is None:
            continue

        if spread < SPREAD_MIN:
            continue

        if spread > SPREAD_MAX:
            continue

        results.append({

            "timestamp": datetime.utcnow().isoformat() + "Z",

            "symbol": m["symbol"],

            "buy_exchange": m["buy_exchange"],
            "buy_price": m["buy_price"],

            "sell_exchange": m["sell_exchange"],
            "sell_price": m["sell_price"],

            "spread": spread

        })

    return results


def save_results(results):

    try:

        os.makedirs("sources", exist_ok=True)

        with open(OUTPUT_FILE, "w") as f:

            json.dump(results, f, indent=2)

        print(f"[ARBITRAGE] opportunities saved: {len(results)}")

    except Exception as e:

        print("[ARBITRAGE] save error:", e)


def main():

    print("[ARBITRAGE] loading matrix opportunities")

    matrix = load_matrix()

    print(f"[ARBITRAGE] matrix loaded: {len(matrix)}")

    opportunities = filter_opportunities(matrix)

    print(f"[ARBITRAGE] opportunities found: {len(opportunities)}")

    save_results(opportunities)