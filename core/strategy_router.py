import json
import os

INPUT_FILE = "sources/latency_checked.json"
OUTPUT_FILE = "sources/routed_signals.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[ROUTER] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def route(signal):

    spread = signal.get("spread_pct", 0)

    if spread > 1.2:
        signal["strategy"] = "cross_exchange"

    elif spread > 0.7:
        signal["strategy"] = "triangular"

    else:
        signal["strategy"] = "micro_scalp"

    return signal


def run():

    print("[ROUTER] strategy router start")

    signals = load_signals()

    routed = [route(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(routed, f, indent=2)

    print(f"[ROUTER] routed signals: {len(routed)}")


def main():
    run()