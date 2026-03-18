import json
import os

INPUT_FILE = "sources/arbitrage_opportunities.json"
OUTPUT_FILE = "sources/arbitrage_after_fees.json"

FEES = {
    "binance": 0.001,
    "okx": 0.001,
    "kucoin": 0.001,
    "coinbase": 0.002,
    "kraken": 0.0026
}

MIN_PROFIT = 0.001


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[FEES] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def calculate_real_profit(signal):

    buy_ex = signal.get("buy_exchange", "").lower()
    sell_ex = signal.get("sell_exchange", "").lower()

    spread = signal.get("spread", 0)

    fee_buy = FEES.get(buy_ex, 0.002)
    fee_sell = FEES.get(sell_ex, 0.002)

    signal["real_profit"] = spread - fee_buy - fee_sell

    return signal


def filter_signals(signals):

    result = []

    for s in signals:
        s = calculate_real_profit(s)

        if s["real_profit"] > MIN_PROFIT:
            result.append(s)

    return result


def save_signals(signals):

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[FEES] signals saved:", len(signals))


def run():

    print("[FEES] fee engine start")

    signals = load_signals()

    filtered = filter_signals(signals)

    print("[FEES] signals after fees:", len(filtered))

    save_signals(filtered)


def main():
    run()


if __name__ == "__main__":
    main()