import json
import os

INPUT_FILE = "sources/policy_decision.json"


def load_decision():

    if not os.path.exists(INPUT_FILE):
        print("[ENGINE] policy file missing")
        return None

    with open(INPUT_FILE) as f:
        return json.load(f)


def execute(decision):

    action = decision.get("action", "HOLD")

    if action == "EXECUTE_FULL":
        print("[ENGINE] full execution approved")

    elif action == "EXECUTE_SMALL":
        print("[ENGINE] reduced execution approved")

    elif action == "HOLD":
        print("[ENGINE] hold state")

    else:
        print("[ENGINE] unknown action")


def run():

    print("[ENGINE] starting action engine")

    decision = load_decision()

    if not decision:
        return

    execute(decision)

    print("[ENGINE] completed")


def main():
    run()