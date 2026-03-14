import json
import os

INPUT_FILE = "sources/decision.json"


def load_decision():

    if not os.path.exists(INPUT_FILE):
        print("[ENGINE] decision file missing")
        return None

    with open(INPUT_FILE) as f:
        return json.load(f)


def run():

    print("[ENGINE] starting action engine")

    decision = load_decision()

    if not decision:
        return

    action = decision.get("action")

    if action == "EXECUTE_FULL":
        print("[ENGINE] full execution approved")

    elif action == "EXECUTE_PARTIAL":
        print("[ENGINE] partial execution approved")

    else:
        print("[ENGINE] hold state")

    print("[ENGINE] completed")


def main():
    run()