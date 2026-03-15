import json
import os

INPUT_FILE = "sources/fill_guarded.json"
OUTPUT_FILE = "sources/recovered_execution.json"


def load():
    if not os.path.exists(INPUT_FILE):
        print("[RECOVERY] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def enrich(signal):

    signal["recovery_ready"] = True

    return signal


def run():

    print("[RECOVERY] start")

    signals = load()

    output = [enrich(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[RECOVERY] ready: {len(output)}")


def main():
    run()