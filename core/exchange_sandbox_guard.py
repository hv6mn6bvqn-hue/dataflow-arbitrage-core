import json
from pathlib import Path

INPUT_FILE = "data/recovered_execution_signals.json"
OUTPUT_FILE = "data/sandbox_execution_signals.json"


def load_data():
    path = Path(INPUT_FILE)
    if not path.exists():
        return []

    with open(path, "r") as f:
        return json.load(f)


def apply_guard(signals):
    result = []

    for signal in signals:
        signal["sandbox_mode"] = True
        signal["live_execution_allowed"] = False
        result.append(signal)

    return result


def save_data(data):
    Path("data").mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    print("[SANDBOX_GUARD] start")

    signals = load_data()
    guarded = apply_guard(signals)
    save_data(guarded)

    print(f"[SANDBOX_GUARD] guarded: {len(guarded)}")


if __name__ == "__main__":
    main()