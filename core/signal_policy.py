import json
import os
from datetime import datetime

INPUT_FILE = "sources/risk_approved.json"
OUTPUT_FILE = "sources/decision.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[POLICY] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def evaluate(signals):

    if not signals:
        return {
            "engine_version": "v3.2.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "HOLD",
            "confidence": 0.0,
            "state": "ACTIVE"
        }

    scores = []

    for signal in signals:
        score = signal.get("execution_score", 0)
        scores.append(score)

    avg_score = round(sum(scores) / len(scores), 4)

    confidence = round(min(len(signals) / 50, 1.0), 2)

    if avg_score > 0.02 and confidence >= 0.5:
        action = "EXECUTE_FULL"

    elif avg_score > -0.02 and confidence >= 0.4:
        action = "EXECUTE_PARTIAL"

    else:
        action = "HOLD"

    return {
        "engine_version": "v3.2.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "avg_score": avg_score,
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