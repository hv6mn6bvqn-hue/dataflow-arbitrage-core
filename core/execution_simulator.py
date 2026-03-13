import json
import os
import random

INPUT_FILE = "sources/arbitrage_liquid.json"
OUTPUT_FILE = "sources/execution_ready.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[EXECUTION] liquidity file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[EXECUTION] signals loaded:", len(data))
    return data


def process_signal(signal):

    spread = signal.get("spread_pct", 0)

    if spread == 0:
        spread = random.uniform(0.15, 1.2)

    slippage = random.uniform(0.02, 0.15)

    execution_edge = spread - slippage

    signal["spread_pct"] = round(spread, 4)
    signal["slippage"] = round(slippage, 4)
    signal["execution_pnl"] = round(execution_edge, 4)

    if execution_edge > 0:
        return signal

    return None


def run():

    print("[EXECUTION] execution simulator start")

    signals = load_signals()

    result = []

    for signal in signals:
        processed = process_signal(signal)

        if processed:
            result.append(processed)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[EXECUTION] execution-valid signals:", len(result))
    print("[EXECUTION] signals saved:", len(result))


def main():
    run()