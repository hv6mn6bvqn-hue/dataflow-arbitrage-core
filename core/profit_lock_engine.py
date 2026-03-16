import json
import os

INPUT_FILE = "data/live_capital_state.json"
OUTPUT_FILE = "data/profit_lock.json"


def load_state():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def lock_profit(state):

    equity = state.get("equity", 10000)

    locked = equity >= 10100

    return {
        "equity": equity,
        "profit_locked": locked
    }


def save_state(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[PROFIT_LOCK] start")

    state = load_state()

    result = lock_profit(state)

    save_state(result)

    print(f"[PROFIT_LOCK] locked: {result['profit_locked']}")


if __name__ == "__main__":
    main()