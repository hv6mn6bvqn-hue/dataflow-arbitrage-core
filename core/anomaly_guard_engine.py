import json
import os

INPUT_FILE = "data/venue_rotated.json"
OUTPUT_FILE = "data/anomaly_guarded.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def guard(signals):

    approved = []

    for signal in signals:

        spread = signal.get("spread_pct", 0)

        if spread > 0.05:
            continue

        approved.append(signal)

    return approved


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[ANOMALY_GUARD] start")

    signals = load_signals()

    approved = guard(signals)

    save_signals(approved)

    print(f"[ANOMALY_GUARD] approved: {len(approved)}")


if __name__ == "__main__":
    main()