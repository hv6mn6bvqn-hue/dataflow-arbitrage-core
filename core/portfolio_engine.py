import json
import os
import random

INPUT_FILE = "sources/decision.json"
OUTPUT_FILE = "sources/portfolio_state.json"


def load_decision():

    if not os.path.exists(INPUT_FILE):
        print("[PORTFOLIO] decision file not found")
        return None

    with open(INPUT_FILE) as f:
        return json.load(f)


def simulate_pnl(action):

    if action == "EXECUTE_FULL":
        return round(random.uniform(-200, 400), 2)

    if action == "EXECUTE_PARTIAL":
        return round(random.uniform(-80, 180), 2)

    return 0


def run():

    print("[PORTFOLIO] starting")

    decision = load_decision()

    if not decision:
        print("[PORTFOLIO] no decision available")
        return

    print("[PORTFOLIO] loaded decision:", decision)

    action = decision.get("action")
    pnl = simulate_pnl(action)

    equity = 10000 + pnl

    state = {
        "action": action,
        "pnl": pnl,
        "equity": equity
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(state, f, indent=2)

    print(f"[PORTFOLIO] trade executed | pnl={pnl} | equity={equity}")
    print("[PORTFOLIO] completed")


def main():
    run()