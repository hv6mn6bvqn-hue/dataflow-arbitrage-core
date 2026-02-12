import json
from datetime import datetime

DECISION_FILE = "core/last_decision.json"
ENGINE_VERSION = "v1.0.0"

EXECUTE_THRESHOLD = 0.75
ALERT_THRESHOLD = 0.50


def evaluate_signal(signal: dict) -> dict:
    confidence = float(signal.get("confidence", 0))

    if confidence >= EXECUTE_THRESHOLD:
        action = "EXECUTE"
        state = "ACTIVE"
    elif confidence >= ALERT_THRESHOLD:
        action = "ALERT"
        state = "ACTIVE"
    else:
        action = "SKIP"
        state = "IDLE"

    return {
        "engine_version": ENGINE_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": round(confidence, 4),
        "state": state
    }


def save_decision(decision: dict):
    with open(DECISION_FILE, "w") as f:
        json.dump(decision, f, indent=2)


def load_signal() -> dict:
    return {
        "confidence": 0.82
    }


def main():
    print("[POLICY] evaluating signal")

    signal = load_signal()
    decision = evaluate_signal(signal)

    save_decision(decision)

    print(f"[POLICY] action={decision['action']}")
    print("[POLICY] decision saved")


if __name__ == "__main__":
    main()