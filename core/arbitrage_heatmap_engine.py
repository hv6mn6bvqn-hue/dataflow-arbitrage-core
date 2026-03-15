import json
import os
from datetime import datetime

INPUT_FILE = "data/recovered_execution_signals.json"
OUTPUT_FILE = "data/arbitrage_heatmap.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def build_heatmap(signals):

    heatmap = {}

    for signal in signals:

        exchange = signal.get("exchange", "unknown")
        pair = signal.get("symbol", "unknown")

        key = f"{exchange}:{pair}"

        if key not in heatmap:
            heatmap[key] = {
                "exchange": exchange,
                "symbol": pair,
                "count": 0,
                "avg_profit": 0
            }

        heatmap[key]["count"] += 1
        heatmap[key]["avg_profit"] += signal.get("net_profit", 0)

    result = []

    for _, value in heatmap.items():

        count = value["count"]

        if count > 0:
            value["avg_profit"] = round(value["avg_profit"] / count, 6)

        result.append(value)

    result.sort(key=lambda x: x["count"], reverse=True)

    return result


def save_heatmap(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "heatmap": data
        }, f, indent=4)


def main():

    print("[HEATMAP] start")

    signals = load_signals()

    heatmap = build_heatmap(signals)

    save_heatmap(heatmap)

    print(f"[HEATMAP] zones: {len(heatmap)}")


if __name__ == "__main__":
    main()