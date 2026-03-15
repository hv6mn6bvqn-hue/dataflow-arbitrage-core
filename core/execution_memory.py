import json
import os

INPUT_FILE = "sources/decay_filtered.json"
OUTPUT_FILE = "data/execution_memory.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def enrich_memory(signals):

    memory = []

    for signal in signals:

        score = signal.get("score", 0)

        signal["memory_weight"] = round(score * 1.15, 4)

        memory.append(signal)

    return memory


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[MEMORY] start")

    signals = load_signals()

    enriched = enrich_memory(signals)

    save_signals(enriched)

    print(f"[MEMORY] stored: {len(enriched)}")


if __name__ == "__main__":
    main()