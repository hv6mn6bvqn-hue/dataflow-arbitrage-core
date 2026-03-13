import json
import os

INPUT_FILE = "sources/arbitrage_after_fees.json"
OUTPUT_FILE = "sources/arbitrage_liquid.json"

MIN_NOTIONAL = 1000        # минимальный объём сделки в quote (например USDT)
MAX_SPREAD_SLIPPAGE = 0.0015  # допустимое ухудшение цены (0.15%)

def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[LIQ] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[LIQ] signals loaded:", len(data))
    return data


def estimate_depth(signal):

    """
    Упрощённая модель ликвидности.
    Если есть поля bid/ask/volume — используем их.
    Иначе применяем консервативную оценку.
    """

    bid = signal.get("bid", signal.get("price", 0))
    ask = signal.get("ask", signal.get("price", 0))
    volume = signal.get("volume", 0)

    mid_price = (bid + ask) / 2 if bid and ask else signal.get("price", 0)

    notional = volume * mid_price

    slippage = abs(ask - bid) / mid_price if mid_price else 1

    signal["estimated_notional"] = notional
    signal["estimated_slippage"] = slippage

    return signal


def filter_liquidity(signals):

    filtered = []

    for s in signals:

        s = estimate_depth(s)

        if s["estimated_notional"] < MIN_NOTIONAL:
            continue

        if s["estimated_slippage"] > MAX_SPREAD_SLIPPAGE:
            continue

        filtered.append(s)

    return filtered


def save_signals(signals):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[LIQ] signals saved:", len(signals))


def run():

    print("[LIQ] liquidity engine start")

    signals = load_signals()

    filtered = filter_liquidity(signals)

    print("[LIQ] signals after liquidity filter:", len(filtered))

    save_signals(filtered)


def main():
    run()