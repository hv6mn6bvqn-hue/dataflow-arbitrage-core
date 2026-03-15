import json
import os

INPUT_FILE = "sources/fill_probability.json"
OUTPUT_FILE = "sources/fill_guarded.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[FILL_GUARD] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def filter_signal(signal):

    if signal.get("fill_probability", 0) >= 0.5:
        return signal

    return None


def run():

    print("[FILL_GUARD] start")

    signals = load()

    output = [s for s in (filter_signal(x) for x in signals) if s]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[FILL_GUARD] kept: {len(output)}")


def main():
    run()