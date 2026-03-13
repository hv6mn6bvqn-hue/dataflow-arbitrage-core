import json
import os

INPUT_FILE = "sources/execution_ready.json"
OUTPUT_FILE = "sources/strategy_signals.json"


def classify(signal):

    spread = signal.get("spread_pct", 0)

    if spread > 0.8:
        signal["strategy"] = "cross_exchange"
    elif spread > 0.4:
        signal["strategy"] = "triangular"
    else:
        signal["strategy"] = "micro_scalp"

    return signal


def run():

    print("[ROUTER] strategy router start")

    if not os.path.exists(INPUT_FILE):
        print("[ROUTER] execution file missing")
        return

    with open(INPUT_FILE) as f:
        signals = json.load(f)

    result = [classify(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[ROUTER] routed signals:", len(result))


def main():
    run()