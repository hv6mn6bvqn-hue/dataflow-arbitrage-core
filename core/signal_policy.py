import json
import os
from datetime import datetime

INPUT_FILE = "data/ranked_opportunities.json"
OUTPUT_FILE = "data/policy_decision.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def evaluate_signal(signals):

    if not signals:
        return {
            "engine_version": "v3.3.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "WAIT",
            "confidence": 0.55,
            "avg_score": 0,
            "signals": 0,
            "state": "IDLE"
        }

    avg_score = round(
        sum(signal.get("spread_pct", 0) for signal in signals) / len(signals),
        4
    )

    if avg_score <= 0:
        action = "WAIT"
        confidence = 0.55
    elif avg_score < 0.003:
        action = "EXECUTE_PARTIAL"
        confidence = 0.68
    else:
        action = "EXECUTE"
        confidence = 0.84

    return {
        "engine_version": "v3.3.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "avg_score": avg_score,
        "signals": len(signals),
        "state": "ACTIVE"
    }


def main():

    print("[POLICY] evaluating signal")

    signals = load_signals()

    decision = evaluate_signal(signals)

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(decision, f, indent=4)

    print(f"[POLICY] action={decision['action']}")
    print("[POLICY] decision saved")


if __name__ == "__main__":
    main()