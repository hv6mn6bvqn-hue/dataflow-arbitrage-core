import json
import os

INPUT_FILE = "sources/execution_scored.json"
OUTPUT_FILE = "sources/slippage_safe.json"


def load_signals():
    if not os.path.exists(INPUT_FILE):
        print("[SLIPPAGE] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def run():

    print("[SLIPPAGE] guard start")

    signals = load_signals()

    filtered = []

    for s in signals:
        slippage = s.get("slippage", 0.05)

        if slippage < 0.25:
            filtered.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(filtered, f, indent=2)

    print(f"[SLIPPAGE] approved: {len(filtered)}")


def main():
    run()