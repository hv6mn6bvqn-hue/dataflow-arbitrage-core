import json
import os

INPUT_FILE = "sources/orderbook_signals.json"
OUTPUT_FILE = "sources/repeatability_signals.json"


def load_signals():

    print(f"[REPEAT] reading: {INPUT_FILE}")

    if not os.path.exists(INPUT_FILE):
        print("[REPEAT] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("[REPEAT] invalid format")
            return []

        return data

    except Exception as e:
        print(f"[REPEAT] load error: {e}")
        return []


def process(signals):

    processed = []

    for signal in signals:

        spread = signal.get("spread_pct", 0)

        repeat_score = 0.2

        if spread >= 0.02:
            repeat_score = 0.9
        elif spread >= 0.01:
            repeat_score = 0.7
        elif spread >= 0.005:
            repeat_score = 0.5

        signal["repeatability_score"] = repeat_score

        processed.append(signal)

    return processed


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[REPEAT] processed: {len(data)}")


def main():

    print("[REPEAT] start")

    signals = load_signals()

    processed = process(signals)

    save_signals(processed)


if __name__ == "__main__":
    main()