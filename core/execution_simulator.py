import json
import os
import random

INPUT_FILE = "sources/liquidity_signals.json"
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

    bid = signal.get("bid", 0)
    ask = signal.get("ask", 0)

    if bid == 0 or ask == 0:
        return None

    latency = random.randint(20, 100)
    slippage = ask * random.uniform(0.0001, 0.0012)

    entry = ask + slippage
    exit_price = bid - slippage

    pnl = exit_price - entry

    signal["latency_ms"] = latency
    signal["slippage"] = round(slippage, 8)
    signal["execution_pnl"] = round(pnl, 8)

    if pnl > 0:
        signal["execution_score"] = "PASS"
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

    print("[EXECUTION] execution-valid signals:", len(result))

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[EXECUTION] signals saved:", len(result))


def main():
    run()