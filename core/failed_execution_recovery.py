import json
import os

INPUT_FILE = "sources/partial_fill_guard.json"
OUTPUT_FILE = "sources/recovered_execution_signals.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[RECOVERY] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return []

            return data

    except Exception as e:
        print(f"[RECOVERY] load error: {e}")
        return []


def recover(signals):

    recovered = []

    for signal in signals:

        recovered.append({
            "exchange": signal.get("exchange", signal.get("buy_exchange", "unknown")),
            "symbol": signal.get("symbol", "unknown"),
            "net_profit": signal.get("real_profit", signal.get("net_profit", 0)),
            "score": signal.get("fill_probability", 0),
            "status": "RECOVERED"
        })

    return recovered


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[RECOVERY] ready: {len(data)}")


def main():

    print("[RECOVERY] start")

    signals = load_signals()

    recovered = recover(signals)

    save_signals(recovered)


if __name__ == "__main__":
    main()