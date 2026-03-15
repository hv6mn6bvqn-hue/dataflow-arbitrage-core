import json
import os

INPUT_FILE = "sources/ranked_signals.json"
OUTPUT_FILE = "sources/policy_v3.json"


def load():

    if not os.path.exists(INPUT_FILE):
        print("[POLICY_V3] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def classify(signal):

    score = signal.get("execution_score", 0)

    if score > 0.03:
        signal["tier"] = "A"

    elif score >= 0:
        signal["tier"] = "B"

    else:
        signal["tier"] = "C"

    return signal


def run():

    print("[POLICY_V3] start")

    signals = load()

    output = [classify(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[POLICY_V3] classified: {len(output)}")


def main():
    run()