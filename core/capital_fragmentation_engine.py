import json
import os

INPUT_FILE = "sources/recovered_execution_signals.json"
OUTPUT_FILE = "sources/capital_fragmented.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[CAPITAL_FRAGMENT] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return []

            return data

    except Exception as e:
        print(f"[CAPITAL_FRAGMENT] load error: {e}")
        return []


def fragment(signals):

    fragmented = []

    for signal in signals:

        fill_probability = signal.get("score", signal.get("fill_probability", 0))

        fragments = 1

        if fill_probability >= 0.9:
            fragments = 3
        elif fill_probability >= 0.7:
            fragments = 2

        signal["capital_fragments"] = fragments
        signal["fragment_size"] = round(1000 / fragments, 2)

        fragmented.append(signal)

    return fragmented


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[CAPITAL_FRAGMENT] fragmented: {len(data)}")


def main():

    print("[CAPITAL_FRAGMENT] start")

    signals = load_signals()

    fragmented = fragment(signals)

    save_signals(fragmented)


if __name__ == "__main__":
    main()