import json
import os
from datetime import datetime

INPUT_FILE = "sources/risk_checked.json"
OUTPUT_FILE = "sources/policy_decision.json"


def run():

    print("[POLICY] evaluating signal")

    action = "HOLD"
    confidence = 0.50

    if os.path.exists(INPUT_FILE):

        with open(INPUT_FILE) as f:
            data = json.load(f)

        if len(data) > 10:
            action = "EXECUTE_FULL"
            confidence = 0.91
        elif len(data) > 3:
            action = "EXECUTE_SMALL"
            confidence = 0.78
        elif len(data) > 0:
            action = "HOLD"
            confidence = 0.61

    decision = {
        "engine_version": "v2.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "state": "ACTIVE"
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(decision, f, indent=2)

    print(f"[POLICY] action={action}")
    print("[POLICY] decision saved")


def main():
    run()