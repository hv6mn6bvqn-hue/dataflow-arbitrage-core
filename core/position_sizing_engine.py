import json
import os

INPUT_FILE = "sources/execution_ready.json"
OUTPUT_FILE = "sources/position_ready.json"


def run():

    print("[SIZE] position sizing start")

    if not os.path.exists(INPUT_FILE):
        print("[SIZE] execution file missing")
        return

    with open(INPUT_FILE) as f:
        data = json.load(f)

    result = []

    for signal in data:

        pnl = signal.get("execution_pnl", 0)

        if pnl > 1:
            size = 1.0
        elif pnl > 0.3:
            size = 0.5
        else:
            size = 0.2

        signal["position_size"] = size
        result.append(signal)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[SIZE] signals sized:", len(result))


def main():
    run()