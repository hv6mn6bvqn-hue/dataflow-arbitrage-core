import json
from pathlib import Path
from datetime import datetime

INPUT_FILE = "data/execution_confidence.json"
OUTPUT_FILE = "data/policy_ready_signals.json"


def load_data():
    path = Path(INPUT_FILE)
    if not path.exists():
        return []
    with open(path, "r") as f:
        return json.load(f)


def transform(signals):
    result = []

    for signal in signals:
        confidence = signal.get("execution_confidence", 0)

        signal["policy_score"] = confidence
        signal["policy_ready"] = confidence >= 0.60
        signal["bridge_timestamp"] = datetime.utcnow().isoformat()

        result.append(signal)

    return result


def save_data(data):
    Path("data").mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    print("[EXEC_POLICY_BRIDGE] start")

    signals = load_data()
    transformed = transform(signals)
    save_data(transformed)

    print(f"[EXEC_POLICY_BRIDGE] bridged: {len(transformed)}")


if __name__ == "__main__":
    main()