import json
import os

INPUT_FILE = "sources/execution_memory.json"
OUTPUT_FILE = "sources/fill_probability.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[FILL] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def enrich(signal):

    score = signal.get("execution_score", 0)

    signal["fill_probability"] = round(min(max(score + 0.5, 0), 1), 2)

    return signal


def run():

    print("[FILL] start")

    signals = load()

    output = [enrich(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[FILL] scored: {len(output)}")


def main():
    run()