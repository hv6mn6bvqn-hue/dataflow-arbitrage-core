import json
import os

INPUT_FILE = "sources/fill_probability.json"
OUTPUT_FILE = "sources/partial_fill_guard.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[FILL_GUARD] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return []

            return data

    except Exception as e:
        print(f"[FILL_GUARD] load error: {e}")
        return []


def guard(signals):

    approved = []

    for signal in signals:

        fill_probability = signal.get("fill_probability", 0)

        if fill_probability >= 0.3:
            approved.append(signal)

    return approved


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[FILL_GUARD] kept: {len(data)}")


def main():

    print("[FILL_GUARD] start")

    signals = load_signals()

    approved = guard(signals)

    save_signals(approved)


if __name__ == "__main__":
    main()