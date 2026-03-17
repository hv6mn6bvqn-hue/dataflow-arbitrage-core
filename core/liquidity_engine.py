import json
import os

INPUT_FILE = "sources/orderbook_data.json"
OUTPUT_FILE = "sources/arbitrage_liquid.json"

MIN_NOTIONAL = 100
MAX_SLIPPAGE = 0.01


def load():

    if not os.path.exists(INPUT_FILE):
        print("[LIQ] orderbook file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[LIQ] signals loaded:", len(data))
    return data


def filter_liquidity(signals):

    filtered = []

    for s in signals:

        bid = s.get("bid", 0)
        ask = s.get("ask", 0)
        volume = s.get("volume", 0)

        if bid <= 0 or ask <= 0:
            continue

        mid = (bid + ask) / 2

        slippage = abs(ask - bid) / mid
        notional = volume * mid

        s["slippage"] = round(slippage, 6)
        s["notional"] = round(notional, 2)

        if notional < MIN_NOTIONAL:
            continue

        if slippage > MAX_SLIPPAGE:
            continue

        filtered.append(s)

    return filtered


def save(signals):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[LIQ] signals saved:", len(signals))


def run():

    print("[LIQ] liquidity engine start")

    signals = load()

    filtered = filter_liquidity(signals)

    print("[LIQ] signals after liquidity filter:", len(filtered))

    save(filtered)


def main():
    run()