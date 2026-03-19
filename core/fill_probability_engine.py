import json
import os

INPUT_FILE = "sources/orderbook_signals.json"
OUTPUT_FILE = "sources/fill_probability.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[FILL] input file missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

            if not isinstance(data, list):
                print("[FILL] invalid input format")
                return []

            return data

    except Exception as e:
        print(f"[FILL] load error: {e}")
        return []


def score_fill(signals):

    scored = []

    for signal in signals:

        real_profit = signal.get("real_profit", 0)

        fill_probability = 0.1

        if real_profit >= 0.02:
            fill_probability = 0.9
        elif real_profit >= 0.01:
            fill_probability = 0.7
        elif real_profit >= 0.005:
            fill_probability = 0.5
        elif real_profit >= 0.002:
            fill_probability = 0.3

        signal["fill_probability"] = fill_probability

        scored.append(signal)

    return scored


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[FILL] scored: {len(data)}")


def main():

    print("[FILL] start")

    signals = load_signals()

    print(f"[FILL] loaded: {len(signals)}")

    scored = score_fill(signals)

    save_signals(scored)


if __name__ == "__main__":
    main()