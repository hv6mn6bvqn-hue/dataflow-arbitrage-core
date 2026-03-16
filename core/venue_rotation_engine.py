import json
import os

INPUT_FILE = "data/execution_confidence.json"
OUTPUT_FILE = "data/venue_rotated.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def rotate_venues(signals):

    rotated = []

    blocked = ["bybit", "binance"]

    for signal in signals:

        venue = str(signal.get("exchange", "")).lower()

        if venue in blocked:
            continue

        rotated.append(signal)

    return rotated


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[VENUE_ROTATION] start")

    signals = load_signals()

    rotated = rotate_venues(signals)

    save_signals(rotated)

    print(f"[VENUE_ROTATION] active: {len(rotated)}")


if __name__ == "__main__":
    main()