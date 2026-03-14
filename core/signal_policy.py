import json
import os
from datetime import datetime

INPUT_FILE = "sources/latency_checked.json"
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
            "engine_version": "v3.1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "HOLD",
            "confidence": 0.0,
            "state": "ACTIVE"
        }

    total_score = 0

    for signal in signals:

        score = signal.get("execution_score", 0)
        latency = signal.get("latency", 0)

        adjusted = score - latency

        total_score += adjusted

    avg = total_score / len(signals)

    if avg > 0.9:
        action = "EXECUTE_FULL"
        confidence = 0.93

    elif avg > 0.45:
        action = "EXECUTE_PARTIAL"
        confidence = 0.76

    else:
        action = "HOLD"
        confidence = 0.40

    return {
        "engine_version": "v3.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "avg_score": round(avg, 4),
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