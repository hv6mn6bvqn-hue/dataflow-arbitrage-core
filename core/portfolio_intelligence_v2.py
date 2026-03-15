import json
import os

INPUT_FILE = "sources/policy_v3.json"
OUTPUT_FILE = "sources/portfolio_intelligence.json"


def load():

    if not os.path.exists(INPUT_FILE):
        print("[PORTFOLIO_INTEL] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def run():

    print("[PORTFOLIO_INTEL] start")

    signals = load()

    summary = {
        "tier_A": len([s for s in signals if s["tier"] == "A"]),
        "tier_B": len([s for s in signals if s["tier"] == "B"]),
        "tier_C": len([s for s in signals if s["tier"] == "C"])
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[PORTFOLIO_INTEL] saved")


def main():
    run()