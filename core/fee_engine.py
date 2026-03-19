import json
import os

INPUT_FILE = "sources/arbitrage_opportunities.json"
OUTPUT_FILE = "sources/fee_filtered_signals.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[FEES] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("[FEES] invalid format")
            return []

        return data

    except Exception as e:
        print(f"[FEES] load error: {e}")
        return []


def apply_fees(signals):

    filtered = []

    for signal in signals:

        spread = signal.get("spread_pct", 0)

        fee = 0.002

        net = spread - fee

        if net > 0:
            signal["fee_pct"] = fee
            signal["net_spread"] = net
            filtered.append(signal)

    return filtered


def save_signals(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[FEES] signals saved: {len(data)}")
    print(f"[FEES] file: {OUTPUT_FILE}")


def main():

    print("[FEES] fee engine start")

    signals = load_signals()

    filtered = apply_fees(signals)

    save_signals(filtered)


if __name__ == "__main__":
    main()