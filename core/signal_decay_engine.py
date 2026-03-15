import json
import os

INPUT_FILE = "sources/venue_quality.json"
OUTPUT_FILE = "sources/decay_filtered.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[DECAY] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def filter_signal(signal):

    quality = signal.get("venue_quality", 0)

    if quality >= 1.5:
        return signal

    return None


def run():

    print("[DECAY] start")

    signals = load()

    output = [s for s in (filter_signal(x) for x in signals) if s]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[DECAY] kept: {len(output)}")


def main():
    run()