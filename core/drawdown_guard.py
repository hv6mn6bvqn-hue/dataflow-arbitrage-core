import json
import os

INPUT_FILE = "sources/position_ready.json"
OUTPUT_FILE = "sources/risk_checked.json"


def run():

    print("[RISK] drawdown guard start")

    if not os.path.exists(INPUT_FILE):
        print("[RISK] position file missing")
        return

    with open(INPUT_FILE) as f:
        data = json.load(f)

    equity = 10000

    result = []

    for signal in data:

        if equity < 9500:
            signal["risk_mode"] = "REDUCED"
            signal["position_size"] *= 0.5
        else:
            signal["risk_mode"] = "NORMAL"

        result.append(signal)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[RISK] signals approved:", len(result))


def main():
    run()