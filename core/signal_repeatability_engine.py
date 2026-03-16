import json
import os

INPUT_FILE = "sources/trusted_signals.json"
OUTPUT_FILE = "sources/repeatable_signals.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[REPEAT] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def enrich(signal):
    confidence = signal.get("confidence", 0)
    score = signal.get("score", 0)

    signal["repeatability"] = round((confidence + score) / 2, 2)

    return signal


def run():
    print("[REPEAT] start")

    signals = load()

    output = [enrich(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[REPEAT] processed: {len(output)}")


def main():
    run()


if __name__ == "__main__":
    main()