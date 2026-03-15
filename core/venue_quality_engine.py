import json
import os

INPUT_FILE = "sources/repeatable_signals.json"
OUTPUT_FILE = "sources/venue_quality.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[VENUE] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def enrich(signal):

    trust = signal.get("trust_score", 0)
    repeat = signal.get("repeatability", 0)

    signal["venue_quality"] = round(trust * (1 + repeat), 2)

    return signal


def run():

    print("[VENUE] start")

    signals = load()

    output = [enrich(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[VENUE] scored: {len(output)}")


def main():
    run()