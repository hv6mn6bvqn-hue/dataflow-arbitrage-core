import json
import random

OUTPUT_FILE = "sources/stat_arb_signals.json"


def run():

    print("[STAT_ARB] engine start")

    result = []

    for i in range(15):
        result.append({
            "pair": random.choice(["BTC-ETH", "ETH-SOL", "BTC-SOL"]),
            "deviation": round(random.uniform(1.1, 3.8), 4)
        })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print("[STAT_ARB] signals:", len(result))


def main():
    run()