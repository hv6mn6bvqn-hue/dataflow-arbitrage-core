import json
import os
from datetime import datetime

INPUT_FILE = "sources/capital_allocated.json"
OUTPUT_FILE = "sources/decision.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[POLICY] capital file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def evaluate(signals):

    if not signals:
        return {
            "engine_version": "v3.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "HOLD",
            "confidence": 0.0,
            "state": "ACTIVE"
        }

    total_score = 0

    for signal in signals:

        spread = signal.get("spread_pct", 0)
        slippage = signal.get("slippage", 0)
        capital = signal.get("capital", 0)
        strategy = signal.get("strategy", "")

        score = spread - slippage

        if strategy == "cross_exchange":
            score += 0.25

        elif strategy == "triangular":
            score += 0.15

        elif strategy == "micro_scalp":
            score += 0.05

        if capital >= 3000:
            score += 0.10

        total_score += score

    avg_score = total_score / len(signals)

    if avg_score > 0.9:
        action = "EXECUTE_FULL"
        confidence = 0.93

    elif avg_score > 0.45:
        action = "EXECUTE_PARTIAL"
        confidence = 0.76

    else:
        action = "HOLD"
        confidence = 0.42

    return {
        "engine_version": "v3.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "avg_score": round(avg_score, 4),
        "signals": len(signals),
        "state": "ACTIVE"
    }


def run():

    print("[POLICY] evaluating signal")

    signals = load_signals()

    decision = evaluate(signals)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(decision, f, indent=2)

    print(f"[POLICY] action={decision['action']}")
    print("[POLICY] decision saved")


def main():
    run()