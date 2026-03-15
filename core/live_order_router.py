import json
import os

INPUT_FILE = "data/exchange_executed.json"
OUTPUT_FILE = "data/live_routed.json"


def load_data():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def route(signals):

    for signal in signals:
        signal["route"] = "PRIMARY"

    return signals


def save(data):

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[LIVE_ROUTER] start")

    signals = load_data()

    result = route(signals)

    save(result)

    print(f"[LIVE_ROUTER] routed: {len(result)}")


if __name__ == "__main__":
    main()