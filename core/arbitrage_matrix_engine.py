import json
import os
from datetime import datetime
from itertools import permutations


INPUT_FILE = "sources/signals.json"
OUTPUT_FILE = "sources/arbitrage_matrix.json"

SPREAD_THRESHOLD = 0.004


def load_signals():

    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("[MATRIX] load error:", e)
        return []


def group_by_symbol(signals):

    markets = {}

    for s in signals:

        symbol = s.get("symbol")
        exchange = s.get("source")
        price = s.get("price")

        if not symbol or not exchange or not price:
            continue

        markets.setdefault(symbol, []).append({
            "exchange": exchange,
            "price": price
        })

    return markets


def compute_matrix(grouped):

    opportunities = []

    for symbol, quotes in grouped.items():

        if len(quotes) < 2:
            continue

        for a, b in permutations(quotes, 2):

            buy_price = a["price"]
            sell_price = b["price"]

            if buy_price <= 0:
                continue

            spread = (sell_price - buy_price) / buy_price

            if spread < SPREAD_THRESHOLD:
                continue

            opportunities.append({

                "timestamp": datetime.utcnow().isoformat() + "Z",
                "symbol": symbol,

                "buy_exchange": a["exchange"],
                "buy_price": buy_price,

                "sell_exchange": b["exchange"],
                "sell_price": sell_price,

                "spread": round(spread, 6)

            })

    return opportunities


def save_results(results):

    try:

        os.makedirs("sources", exist_ok=True)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2)

        print(f"[MATRIX] opportunities saved: {len(results)}")

    except Exception as e:

        print("[MATRIX] save error:", e)


def main():

    print("[MATRIX] engine start")

    signals = load_signals()

    print(f"[MATRIX] signals loaded: {len(signals)}")

    grouped = group_by_symbol(signals)

    opportunities = compute_matrix(grouped)

    print(f"[MATRIX] opportunities found: {len(opportunities)}")

    save_results(opportunities)