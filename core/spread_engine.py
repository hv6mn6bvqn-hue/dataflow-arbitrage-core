import json
from collections import defaultdict
from datetime import datetime


INPUT_FILE = "sources/signals.json"
OUTPUT_FILE = "sources/spreads.json"

SPREAD_THRESHOLD = 0.004   # 0.4%


def load_signals():

    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("[SPREAD] failed to load signals:", e)
        return []


def group_by_symbol(signals):

    markets = defaultdict(list)

    for s in signals:

        symbol = s.get("symbol")
        source = s.get("source")
        price = s.get("price")

        if not symbol or not source or not price:
            continue

        markets[symbol].append({
            "exchange": source,
            "price": price
        })

    return markets


def calculate_spreads(grouped):

    opportunities = []

    for symbol, quotes in grouped.items():

        if len(quotes) < 2:
            continue

        min_q = min(quotes, key=lambda x: x["price"])
        max_q = max(quotes, key=lambda x: x["price"])

        min_price = min_q["price"]
        max_price = max_q["price"]

        if min_price <= 0:
            continue

        spread = (max_price - min_price) / min_price

        if spread < SPREAD_THRESHOLD:
            continue

        opportunities.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "symbol": symbol,
            "buy_from": min_q["exchange"],
            "buy_price": min_price,
            "sell_to": max_q["exchange"],
            "sell_price": max_price,
            "spread": round(spread, 6)
        })

    return opportunities


def save_spreads(spreads):

    try:

        with open(OUTPUT_FILE, "w") as f:
            json.dump(spreads, f, indent=2)

        print(f"[SPREAD] opportunities saved: {len(spreads)}")

    except Exception as e:

        print("[SPREAD] save error:", e)


def main():

    print("[SPREAD] engine start")

    signals = load_signals()

    print(f"[SPREAD] signals loaded: {len(signals)}")

    grouped = group_by_symbol(signals)

    spreads = calculate_spreads(grouped)

    print(f"[SPREAD] opportunities found: {len(spreads)}")

    save_spreads(spreads)