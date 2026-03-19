import json
import os

INPUT_FILE = "sources/capital_fragmented.json"
OUTPUT_FILE = "sources/exchange_executed.json"


def load_data():

    if not os.path.exists(INPUT_FILE):
        print("[API_EXECUTOR] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return []

            return data

    except Exception as e:
        print(f"[API_EXECUTOR] load error: {e}")
        return []


def execute(signals):

    executed = []

    for signal in signals:

        signal["exchange_execution"] = "SIMULATED_OK"
        signal["execution_status"] = "FILLED"
        signal["executed_fragments"] = signal.get("capital_fragments", 1)

        executed.append(signal)

    return executed


def save(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[API_EXECUTOR] executed: {len(data)}")


def main():

    print("[API_EXECUTOR] start")

    signals = load_data()

    result = execute(signals)

    save(result)


if __name__ == "__main__":
    main()