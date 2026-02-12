import json
import os
import random
from datetime import datetime

STATE_FILE = "core/state.json"
PORTFOLIO_FILE = "core/portfolio_state.json"
PUBLIC_FILE = "docs/portfolio/index.json"

INITIAL_CAPITAL = 10000
MAX_RISK_PCT = 0.02  # 2% per trade


def load_decision():
    if not os.path.exists(STATE_FILE):
        print("[PORTFOLIO] state.json not found")
        return None

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    print(f"[PORTFOLIO] loaded decision: {data}")
    return data


def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        print("[PORTFOLIO] initializing new portfolio")
        return {
            "capital": INITIAL_CAPITAL,
            "equity": INITIAL_CAPITAL,
            "history": []
        }

    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)


def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)


def publish_public(data):
    os.makedirs("docs/portfolio", exist_ok=True)

    public_data = {
        "engine_version": data.get("engine_version"),
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "capital": data["capital"],
        "equity": round(data["equity"], 2),
        "total_trades": len(data["history"]),
        "drawdown": calculate_drawdown(data["history"])
    }

    with open(PUBLIC_FILE, "w") as f:
        json.dump(public_data, f, indent=2)


def calculate_drawdown(history):
    peak = 0
    max_dd = 0

    for trade in history:
        eq = trade["equity"]
        if eq > peak:
            peak = eq
        dd = peak - eq
        if dd > max_dd:
            max_dd = dd

    return round(max_dd, 2)


def execute_trade(portfolio, decision):
    confidence = decision.get("confidence", 0)
    capital = portfolio["equity"]

    risk_amount = capital * MAX_RISK_PCT
    position_size = risk_amount * confidence

    # Random profit or loss
    return_factor = random.uniform(-1, 1)
    pnl = position_size * return_factor

    portfolio["equity"] += pnl

    portfolio["history"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "confidence": confidence,
        "position_size": round(position_size, 2),
        "return_factor": round(return_factor, 4),
        "pnl": round(pnl, 2),
        "equity": round(portfolio["equity"], 2)
    })

    print(f"[PORTFOLIO] trade executed pnl={round(pnl,2)}")


def main():
    print("[PORTFOLIO] starting")

    decision = load_decision()
    if not decision:
        print("[PORTFOLIO] no decision — exit")
        return

    portfolio = load_portfolio()

    if decision.get("action") == "EXECUTE":
        execute_trade(portfolio, decision)
    else:
        print("[PORTFOLIO] no EXECUTE action")

    portfolio["engine_version"] = decision.get("engine_version")

    save_portfolio(portfolio)
    publish_public(portfolio)

    print("[PORTFOLIO] updated successfully")


if __name__ == "__main__":
    main()