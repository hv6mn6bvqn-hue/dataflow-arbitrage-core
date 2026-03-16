import json
import os
import random

INPUT_FILE = "data/policy_decision.json"
OUTPUT_FILE = "data/portfolio_state.json"


def load_decision():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return None


def main():

    print("[PORTFOLIO] starting")

    decision = load_decision()

    if not decision:
        print("[PORTFOLIO] decision file not found")
        return

    print(f"[PORTFOLIO] loaded decision: {decision}")

    action = decision.get("action")

    if action == "WAIT":
        print("[PORTFOLIO] no execution")
        return

    pnl = round(random.uniform(5, 150), 2)

    equity = round(10000 + pnl, 2)

    result = {
        "pnl": pnl,
        "equity": equity
    }

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[PORTFOLIO] trade executed | pnl={pnl} | equity={equity}")
    print("[PORTFOLIO] completed")


if __name__ == "__main__":
    main()