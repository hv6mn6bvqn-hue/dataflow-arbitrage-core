import json
import os
import random

INPUT_FILE = "sources/policy_decision.json"
OUTPUT_FILE = "sources/portfolio_report.json"


def load_decision():

    if not os.path.exists(INPUT_FILE):
        print("[PORTFOLIO] decision file not found")
        return None

    with open(INPUT_FILE) as f:
        return json.load(f)


def run():

    print("[PORTFOLIO] starting")

    decision = load_decision()

    if not decision:
        print("[PORTFOLIO] no decision available")
        return

    print("[PORTFOLIO] loaded decision:", decision)

    equity = 10000

    action = decision.get("action")

    if action == "EXECUTE_FULL":
        pnl = random.uniform(-150, 250)

    elif action == "EXECUTE_SMALL":
        pnl = random.uniform(-50, 120)

    else:
        pnl = 0

    equity += pnl

    report = {
        "action": action,
        "pnl": round(pnl, 2),
        "equity": round(equity, 2)
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[PORTFOLIO] trade executed | pnl={round(pnl,2)} | equity={round(equity,2)}")
    print("[PORTFOLIO] completed")


def main():
    run()