import json
import os

INPUT_FILE = "data/failed_execution_recovery.json"
OUTPUT_FILE = "data/capital_fragmented.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def fragment(signals):

    result = []

    for signal in signals:

        fp = signal.get("fill_probability", 0)

        fragments = 1

        if fp > 0.9:
            fragments = 3
        elif fp > 0.75:
            fragments = 2

        signal["capital_fragments"] = fragments
        signal["fragment_size"] = round(1000 / fragments, 2)

        result.append(signal)

    return result


def save(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[CAPITAL_FRAGMENT] start")

    signals = load_signals()

    result = fragment(signals)

    save(result)

    print(f"[CAPITAL_FRAGMENT] fragmented: {len(result)}")


if __name__ == "__main__":
    main()