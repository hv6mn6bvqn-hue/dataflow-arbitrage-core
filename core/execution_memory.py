import json
import os

INPUT_FILE = "sources/decay_filtered.json"
OUTPUT_FILE = "sources/execution_memory.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[MEMORY] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def run():

    print("[MEMORY] start")

    signals = load()

    for s in signals:
        s["memory_flag"] = True

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print(f"[MEMORY] stored: {len(signals)}")


def main():
    run()