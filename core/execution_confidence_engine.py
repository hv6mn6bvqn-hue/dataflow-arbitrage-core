import json
import os

INPUT_FILE = "data/order_confirmed.json"
OUTPUT_FILE = "data/execution_confidence.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def score_confidence(signals):

    scored = []

    for signal in signals:

        fill_prob = signal.get("fill_probability", 0.5)
        spread = signal.get("spread_pct", 0)

        confidence = round((fill_prob * 0.7) + (spread * 10), 4)

        signal["execution_confidence"] = confidence

        scored.append(signal)

    return scored


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[EXEC_CONFIDENCE] start")

    signals = load_signals()

    scored = score_confidence(signals)

    save_signals(scored)

    print(f"[EXEC_CONFIDENCE] scored: {len(scored)}")


if __name__ == "__main__":
    main()