import json
import os
from datetime import datetime

INPUT_FILE = "data/order_confirmed.json"
OUTPUT_FILE = "data/real_pnl.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def calculate_real_pnl(signals):

    tracked = []

    for signal in signals:

        spread = signal.get("spread_pct", 0)
        fragment_size = signal.get("fragment_size", 0)

        gross = fragment_size * spread / 100
        fee = fragment_size * 0.001

        pnl = round(gross - fee, 4)

        signal["real_pnl"] = pnl
        signal["pnl_timestamp"] = datetime.utcnow().isoformat()

        tracked.append(signal)

    return tracked


def save_signals(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[REAL_PNL] start")

    signals = load_signals()

    tracked = calculate_real_pnl(signals)

    save_signals(tracked)

    print(f"[REAL_PNL] tracked: {len(tracked)}")


if __name__ == "__main__":
    main()