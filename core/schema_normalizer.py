import json
import os

INPUT_FILE = "sources/risk_approved.json"
OUTPUT_FILE = "sources/normalized_signals.json"


def load():

    if not os.path.exists(INPUT_FILE):
        print("[NORMALIZER] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def normalize(signal):

    return {
        "symbol": signal.get("symbol"),
        "buy_exchange": signal.get("buy_exchange"),
        "sell_exchange": signal.get("sell_exchange"),
        "spread": signal.get("spread", 0),
        "execution_score": signal.get("execution_score", 0),
        "position_size": signal.get("position_size", 0),
        "risk_status": signal.get("risk_status", "unknown")
    }


def run():

    print("[NORMALIZER] start")

    data = load()

    normalized = [normalize(s) for s in data]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(normalized, f, indent=2)

    print(f"[NORMALIZER] normalized: {len(normalized)}")


def main():
    run()