import json
import os
import itertools

SIGNALS_FILE = "sources/signals.json"
SPREAD_FILE = "sources/spread_opportunities.json"


def load_signals():

    if not os.path.exists(SIGNALS_FILE):
        print("[SPREAD] signals file missing")
        return []

    with open(SIGNALS_FILE) as f:
        return json.load(f)


def group_by_symbol(signals):

    markets = {}

    for s in signals:

        symbol = s.get("symbol")

        if not symbol:
            continue

        if symbol not in markets:
            markets[symbol] = []

        markets[symbol].append(s)

    return markets


def find_spreads(markets):

    opportunities = []

    for symbol, listings in markets.items():

        if len(listings) < 2:
            continue

        for a, b in itertools.combinations(listings, 2):

            price_a = a.get("price")
            price_b = b.get("price")

            if not price_a or not price_b:
                continue

            try:

                spread = abs(price_a - price_b) / min(price_a, price_b)

            except ZeroDivisionError:
                continue

            if spread > 0.002:  # 0.2%

                opp = {
                    "symbol": symbol,
                    "exchange_a": a.get("exchange"),
                    "exchange_b": b.get("exchange"),
                    "price_a": price_a,
                    "price_b": price_b,
                    "spread": spread
                }

                opportunities.append(opp)

    return opportunities


def save_opportunities(opps):

    os.makedirs("sources", exist_ok=True)

    with open(SPREAD_FILE, "w") as f:
        json.dump(opps, f, indent=2)

    print("[SPREAD] opportunities saved:", len(opps))


def run():

    print("[SPREAD] engine start")

    signals = load_signals()

    print("[SPREAD] signals loaded:", len(signals))

    markets = group_by_symbol(signals)

    opportunities = find_spreads(markets)

    print("[SPREAD] opportunities found:", len(opportunities))

    save_opportunities(opportunities)


def main():
    run()