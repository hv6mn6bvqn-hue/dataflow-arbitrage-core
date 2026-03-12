import json
import os
from collections import defaultdict
from core.utils.symbol_normalizer import normalize

INPUT_FILE = "sources/signals.json"
OUTPUT_FILE = "sources/matrix_opportunities.json"

SPREAD_THRESHOLD = 0.002


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[MATRIX] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[MATRIX] signals loaded:", len(data))
    return data


def build_symbol_matrix(signals):

    matrix = defaultdict(list)

    for s in signals:

        symbol = normalize(s["symbol"])

        if not symbol:
            continue

        entry = {
            "exchange": s["exchange"],
            "price": s["price"],
            "symbol": symbol
        }

        matrix[symbol].append(entry)

    return matrix


def detect_arbitrage(matrix):

    opportunities = []

    for symbol, markets in matrix.items():

        if len(markets) < 2:
            continue

        prices = sorted(markets, key=lambda x: x["price"])

        lowest = prices[0]
        highest = prices[-1]

        spread = (highest["price"] - lowest["price"]) / lowest["price"]

        if spread > SPREAD_THRESHOLD:

            opportunities.append({
                "symbol": symbol,
                "buy_exchange": lowest["exchange"],
                "sell_exchange": highest["exchange"],
                "buy_price": lowest["price"],
                "sell_price": highest["price"],
                "spread": spread
            })

    return opportunities


def save_opportunities(opps):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(opps, f, indent=2)

    print("[MATRIX] opportunities saved:", len(opps))


def run():

    print("[MATRIX] engine start")

    signals = load_signals()

    matrix = build_symbol_matrix(signals)

    opportunities = detect_arbitrage(matrix)

    print("[MATRIX] opportunities found:", len(opportunities))

    save_opportunities(opportunities)


def main():
    run()