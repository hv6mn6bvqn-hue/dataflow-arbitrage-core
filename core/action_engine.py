import json

INPUT_FILE = "data/policy_decision.json"


def load_decision():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return None


def main():

    print("[ENGINE] starting action engine")

    decision = load_decision()

    if not decision:
        print("[ENGINE] decision file missing")
        return

    action = decision.get("action")

    if action == "WAIT":
        print("[ENGINE] waiting")
    elif action == "EXECUTE_PARTIAL":
        print("[ENGINE] partial execution approved")
    elif action == "EXECUTE":
        print("[ENGINE] full execution approved")

    print("[ENGINE] completed")


if __name__ == "__main__":
    main()