import json
import os

INPUT_FILE = "sources/normalized_signals.json"
OUTPUT_FILE = "sources/ranked_signals.json"


def load():

    if not os.path.exists(INPUT_FILE):
        print("[RANKER] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def run():

    print("[RANKER] ranking start")

    signals = load()

    ranked = sorted(
        signals,
        key=lambda x: x.get("execution_score", 0),
        reverse=True
    )

    with open(OUTPUT_FILE, "w") as f:
        json.dump(ranked, f, indent=2)

    print(f"[RANKER] ranked: {len(ranked)}")


def main():
    run()