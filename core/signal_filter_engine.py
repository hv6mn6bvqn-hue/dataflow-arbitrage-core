import json
import os

SPREAD_FILE = "sources/spread_opportunities.json"
SIGNAL_FILE = "sources/arbitrage_signals.json"

MIN_SPREAD = 0.003   # 0.3%
MAX_SIGNALS = 30


def load_spreads():

    if not os.path.exists(SPREAD_FILE):
        print("[SIGNAL] spread file missing")
        return []

    with open(SPREAD_FILE) as f:
        return json.load(f)


def filter_spreads(spreads):

    filtered = []

    for s in spreads:

        spread = s.get("spread", 0)

        if spread >= MIN_SPREAD:

            signal = {
                "symbol": s["symbol"],
                "buy_exchange": s["exchange_a"],
                "sell_exchange": s["exchange_b"],
                "buy_price": s["price_a"],
                "sell_price": s["price_b"],
                "spread": spread
            }

            filtered.append(signal)

    return filtered


def rank_signals(signals):

    ranked = sorted(
        signals,
        key=lambda x: x["spread"],
        reverse=True
    )

    return ranked[:MAX_SIGNALS]


def save_signals(signals):

    os.makedirs("sources", exist_ok=True)

    with open(SIGNAL_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[SIGNAL] signals saved:", len(signals))


def run():

    print("[SIGNAL] engine start")

    spreads = load_spreads()

    print("[SIGNAL] spreads loaded:", len(spreads))

    filtered = filter_spreads(spreads)

    print("[SIGNAL] spreads after filter:", len(filtered))

    ranked = rank_signals(filtered)

    print("[SIGNAL] top signals:", len(ranked))

    save_signals(ranked)


def main():
    run()