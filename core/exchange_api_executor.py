import json
import os

INPUT_FILE = "data/capital_fragmented.json"
OUTPUT_FILE = "data/exchange_executed.json"


def load_data():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def execute(signals):

    for signal in signals:
        signal["exchange_execution"] = "SIMULATED_OK"

    return signals


def save(data):

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[API_EXECUTOR] start")

    signals = load_data()

    result = execute(signals)

    save(result)

    print(f"[API_EXECUTOR] executed: {len(result)}")


if __name__ == "__main__":
    main()