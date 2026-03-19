# core/portfolio_engine.py
import json
import os

INPUT_FILE = "sources/action_executed.json"
OUTPUT_FILE = "sources/portfolio_state.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print("[PORTFOLIO] input missing")
        portfolio = {"state": "IDLE", "signals": 0, "equity": 10000}
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)
        executed_signals = [s for s in signals if s.get("executed")]
        portfolio = {
            "state": "ACTIVE" if executed_signals else "IDLE",
            "signals": len(executed_signals),
            "equity": 10000  # placeholder
        }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(portfolio, f)

    print(f"[PORTFOLIO] loaded decision: {portfolio}")

if __name__ == "__main__":
    print("[PORTFOLIO] starting")
    run()