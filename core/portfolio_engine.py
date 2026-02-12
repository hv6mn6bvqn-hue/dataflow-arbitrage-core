import json
import os
from datetime import datetime

STATE_FILE = "core/state.json"
PORTFOLIO_FILE = "core/portfolio_state.json"
PUBLIC_FILE = "docs/portfolio/index.json"

INITIAL_CAPITAL = 10000
MAX_RISK_PCT = 0.02   # 2% risk per trade
RETURN_FACTOR = 1     # placeholder market return


def load_decision():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
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


def publish_portfolio(data):
    os.makedirs("docs/portfolio", exist_ok=True)
    with open(PUBLIC_FILE, "w") as f:
        json.dump(data, f, indent=2)


def calculate_drawdown(history):
    peak = 0
    max_dd = 0

    for point in history:
        equity = point["equity"]
        if equity > peak:
            peak = equity
        dd = peak - equity
        if dd > max_dd:
            max_dd = dd

    return max_dd


def main():
    decision = load_decision()
    if not decision:
        print("[PORTFOLIO] no decision found")
        return

    portfolio = load_portfolio()

    action = decision.get("action")
    confidence = decision.get("confidence", 0)
    engine_version = decision.get("engine_version")

    if action == "EXECUTE":
        capital = portfolio["equity"]

        risk_amount = capital * MAX_RISK_PCT
        position_size = risk_amount * confidence
        pnl = position_size * RETURN_FACTOR

        portfolio["equity"] += pnl

        portfolio["history"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "position_size": round(position_size, 2),
            "pnl": round(pnl, 2),
            "equity": round(portfolio["equity"], 2)
        })

        print(f"[PORTFOLIO] executed trade, pnl={pnl}")

    drawdown = calculate_drawdown(portfolio["history"])

    public_data = {
        "engine_version": engine_version,
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "capital": portfolio["capital"],
        "equity": round(portfolio["equity"], 2),
        "total_trades": len(portfolio["history"]),
        "drawdown": round(drawdown, 2)
    }

    save_portfolio(portfolio)
    publish_portfolio(public_data)

    print("[PORTFOLIO] updated")


if __name__ == "__main__":
    main()