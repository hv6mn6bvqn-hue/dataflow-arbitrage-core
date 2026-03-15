import json
import os

INPUT_FILE = "data/partial_fill_guard.json"
OUTPUT_FILE = "data/recovered_execution_signals.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def recover(signals):

    recovered = []

    for signal in signals:

        recovered.append({
            "exchange": signal.get("exchange", "unknown"),
            "symbol": signal.get("symbol", "unknown"),
            "net_profit": signal.get("net_profit", 0),
            "score": signal.get("score", 0),
            "status": "RECOVERED"
        })

    return recovered


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[RECOVERY] start")

    signals = load_signals()

    recovered = recover(signals)

    save_signals(recovered)

    print(f"[RECOVERY] ready: {len(recovered)}")


if __name__ == "__main__":
    main()