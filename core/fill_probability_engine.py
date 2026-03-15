import json
import os

INPUT_FILE = "data/execution_memory.json"
OUTPUT_FILE = "data/fill_probability.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def score_fill(signals):

    scored = []

    for signal in signals:

        score = signal.get("score", 0)

        fill_probability = 0.05

        if score > 0.8:
            fill_probability = 0.9
        elif score > 0.6:
            fill_probability = 0.7
        elif score > 0.4:
            fill_probability = 0.5
        elif score > 0.2:
            fill_probability = 0.3
        elif score > 0:
            fill_probability = 0.1

        signal["fill_probability"] = fill_probability

        scored.append(signal)

    return scored


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[FILL] start")

    signals = load_signals()

    scored = score_fill(signals)

    save_signals(scored)

    print(f"[FILL] scored: {len(scored)}")


if __name__ == "__main__":
    main()