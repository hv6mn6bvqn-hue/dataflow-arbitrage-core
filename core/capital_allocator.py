import json
import os

INPUT_FILE = "sources/strategy_signals.json"
OUTPUT_FILE = "sources/capital_allocated.json"


def allocate(signal):

    strategy = signal.get("strategy")

    if strategy == "cross_exchange":
        signal["capital"] = 3000

    elif strategy == "triangular":
        signal["capital"] = 2000

    else:
        signal["capital"] = 1000

    return signal


def run():

    print("[ALLOCATOR] capital allocator start")

    if not os.path.exists(INPUT_FILE):
        print("[ALLOCATOR] strategy file missing")
        return

    with open(INPUT_FILE) as f:
        signals = json.load(f)

    result = [allocate(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[ALLOCATOR] allocated:", len(result))


def main():
    run()