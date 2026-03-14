import json
import os

INPUT_FILE = "sources/routed_signals.json"
OUTPUT_FILE = "sources/capital_allocated.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[ALLOCATOR] strategy file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def allocate(signal):

    strategy = signal.get("strategy", "")

    if strategy == "cross_exchange":
        signal["capital"] = 3000

    elif strategy == "triangular":
        signal["capital"] = 2000

    else:
        signal["capital"] = 1000

    return signal


def run():

    print("[ALLOCATOR] capital allocator start")

    signals = load_signals()

    allocated = [allocate(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(allocated, f, indent=2)

    print(f"[ALLOCATOR] allocated: {len(allocated)}")


def main():
    run()