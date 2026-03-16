import json
import os

INPUT_FILE = "data/recovered_execution_signals.json"
OUTPUT_FILE = "data/capital_fragmented.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def fragment(signals):

    fragmented = []

    for signal in signals:

        fill_probability = signal.get("fill_probability", 0)

        fragments = 1

        if fill_probability > 0.9:
            fragments = 3
        elif fill_probability > 0.75:
            fragments = 2

        signal["capital_fragments"] = fragments
        signal["fragment_size"] = round(1000 / fragments, 2)

        fragmented.append(signal)

    return fragmented


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[CAPITAL_FRAGMENT] start")

    signals = load_signals()

    fragmented = fragment(signals)

    save_signals(fragmented)

    print(f"[CAPITAL_FRAGMENT] fragmented: {len(fragmented)}")


if __name__ == "__main__":
    main()