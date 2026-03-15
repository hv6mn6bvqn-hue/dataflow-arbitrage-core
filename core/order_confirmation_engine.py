import json
import os

INPUT_FILE = "data/live_routed.json"
OUTPUT_FILE = "data/order_confirmed.json"


def load_data():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def confirm(signals):

    for signal in signals:
        signal["confirmation"] = "CONFIRMED"

    return signals


def save(data):

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[CONFIRMATION] start")

    signals = load_data()

    result = confirm(signals)

    save(result)

    print(f"[CONFIRMATION] confirmed: {len(result)}")


if __name__ == "__main__":
    main()