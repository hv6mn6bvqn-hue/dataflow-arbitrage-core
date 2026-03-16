import json
import os

INPUT_FILE = "data/real_pnl.json"
OUTPUT_FILE = "data/live_capital_state.json"

BASE_CAPITAL = 10000


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def calculate_capital(signals):

    total_pnl = sum(signal.get("real_pnl", 0) for signal in signals)

    equity = round(BASE_CAPITAL + total_pnl, 4)

    state = {
        "base_capital": BASE_CAPITAL,
        "realized_pnl": round(total_pnl, 4),
        "equity": equity,
        "active_signals": len(signals)
    }

    return state


def save_state(state):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(state, f, indent=4)


def main():

    print("[LIVE_CAPITAL] start")

    signals = load_signals()

    state = calculate_capital(signals)

    save_state(state)

    print(f"[LIVE_CAPITAL] equity: {state['equity']}")


if __name__ == "__main__":
    main()