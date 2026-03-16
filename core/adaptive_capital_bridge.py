import json
import os

LIVE_CAPITAL_FILE = "data/live_capital_state.json"
PORTFOLIO_FILE = "data/portfolio_state.json"
OUTPUT_FILE = "data/adaptive_capital_state.json"


def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default


def bridge_capital():

    live = load_json(LIVE_CAPITAL_FILE, {})
    portfolio = load_json(PORTFOLIO_FILE, {})

    live_equity = live.get("equity", 10000)
    portfolio_equity = portfolio.get("equity", 10000)

    consensus_equity = round((live_equity + portfolio_equity) / 2, 4)

    state = {
        "live_equity": live_equity,
        "portfolio_equity": portfolio_equity,
        "consensus_equity": consensus_equity
    }

    return state


def save_state(state):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(state, f, indent=4)


def main():

    print("[CAPITAL_BRIDGE] start")

    state = bridge_capital()

    save_state(state)

    print(f"[CAPITAL_BRIDGE] consensus: {state['consensus_equity']}")


if __name__ == "__main__":
    main()