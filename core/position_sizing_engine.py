import json
import os

INPUT_FILE = "sources/capital_allocated.json"
OUTPUT_FILE = "sources/position_sized.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[SIZE] execution file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def size(signal):

    capital = signal.get("capital", 0)

    signal["position_size"] = round(capital * 0.25, 2)

    return signal


def run():

    print("[SIZE] position sizing start")

    signals = load_signals()

    sized = [size(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(sized, f, indent=2)

    print(f"[SIZE] signals sized: {len(sized)}")


def main():
    run()