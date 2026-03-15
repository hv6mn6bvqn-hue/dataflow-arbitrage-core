import json
import os

INPUT_FILE = "data/fill_probability.json"
OUTPUT_FILE = "data/partial_fill_guard.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def guard(signals):

    approved = []

    for signal in signals:

        fill_probability = signal.get("fill_probability", 0)

        if fill_probability >= 0.1:
            approved.append(signal)

    return approved


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[FILL_GUARD] start")

    signals = load_signals()

    approved = guard(signals)

    save_signals(approved)

    print(f"[FILL_GUARD] kept: {len(approved)}")


if __name__ == "__main__":
    main()