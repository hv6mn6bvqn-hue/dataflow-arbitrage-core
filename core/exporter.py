import json
import os

INPUT_FILE = "sources/arbitrage.json"
OUTPUT_FILE = "public/arbitrage_feed.json"


def load_arbitrage():

    try:

        with open(INPUT_FILE, "r") as f:
            return json.load(f)

    except Exception as e:

        print("[EXPORTER] load error:", e)

        return []


def save_feed(data):

    try:

        os.makedirs("public", exist_ok=True)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(data, f, indent=2)

        print(f"[EXPORTER] public feed updated: {len(data)} signals")

    except Exception as e:

        print("[EXPORTER] save error:", e)


def main():

    print("[EXPORTER] collecting arbitrage signals")

    signals = load_arbitrage()

    print(f"[EXPORTER] signals found: {len(signals)}")

    save_feed(signals)