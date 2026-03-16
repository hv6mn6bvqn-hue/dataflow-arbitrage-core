import json
import os

INPUT_FILE = "data/adaptive_capital_state.json"
OUTPUT_FILE = "data/pnl_consensus.json"


def load_state():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def build_consensus(state):

    live_equity = state.get("live_equity", 10000)
    portfolio_equity = state.get("portfolio_equity", 10000)

    divergence = round(abs(live_equity - portfolio_equity), 4)

    result = {
        "live_equity": live_equity,
        "portfolio_equity": portfolio_equity,
        "divergence": divergence,
        "status": "OK" if divergence < 100 else "CHECK"
    }

    return result


def save_result(result):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=4)


def main():

    print("[PNL_CONSENSUS] start")

    state = load_state()

    result = build_consensus(state)

    save_result(result)

    print(f"[PNL_CONSENSUS] divergence: {result['divergence']}")


if __name__ == "__main__":
    main()