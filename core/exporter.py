import json
import os

INPUT_FILE = "sources/arbitrage_opportunities.json"
OUTPUT_FILE = "public/arbitrage_signals.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[EXPORTER] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[EXPORTER] signals found:", len(data))
    return data


def save_public_feed(signals):

    os.makedirs("public", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[EXPORTER] public feed updated:", len(signals), "signals")


def run():

    print("[EXPORTER] collecting arbitrage signals")

    signals = load_signals()

    save_public_feed(signals)


def main():
    run()