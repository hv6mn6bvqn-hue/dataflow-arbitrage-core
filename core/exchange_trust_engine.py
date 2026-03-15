import json
import os

INPUT_FILE = "sources/ranked_signals.json"
OUTPUT_FILE = "sources/trusted_signals.json"

TRUST = {
    "okx": 0.95,
    "coinbase": 0.92,
    "kucoin": 0.88,
    "kraken": 0.90,
    "binance": 0.91,
    "bybit": 0.85
}


def load():
    if not os.path.exists(INPUT_FILE):
        print("[TRUST] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def enrich(signal):

    buy = str(signal.get("buy_exchange", "")).lower()
    sell = str(signal.get("sell_exchange", "")).lower()

    trust_buy = TRUST.get(buy, 0.80)
    trust_sell = TRUST.get(sell, 0.80)

    signal["trust_score"] = round((trust_buy + trust_sell) / 2, 2)

    return signal


def run():

    print("[TRUST] start")

    signals = load()

    output = [enrich(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[TRUST] trusted: {len(output)}")


def main():
    run()