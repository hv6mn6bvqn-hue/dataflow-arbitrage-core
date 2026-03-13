import json
import random

OUTPUT_FILE = "sources/funding_recovery.json"


def run():

    print("[FUNDING_RECOVERY] engine start")

    result = []

    for i in range(12):
        result.append({
            "exchange": random.choice(["okx", "bybit", "kucoin"]),
            "symbol": random.choice(["BTCUSDT", "ETHUSDT", "SOLUSDT"]),
            "funding_edge": round(random.uniform(0.01, 0.18), 4)
        })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[FUNDING_RECOVERY] recovered:", len(result))


def main():
    run()