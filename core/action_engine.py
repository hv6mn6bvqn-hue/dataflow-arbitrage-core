import json
from datetime import datetime

from core.signal_policy import evaluate_signal
from core.audit_logger import log_audit
from core.telegram_adapter import send_telegram  # ← ВАЖНО
from core.feed_loader import load_latest_signal


ENGINE_VERSION = "v1.0.0"


def main():
    signal = load_latest_signal()
    decision = evaluate_signal(signal)

    action = decision.get("action")
    confidence = decision.get("confidence")
    note = decision.get("note")

    execution = None

    if action == "EXECUTE":
        execution = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "confidence": confidence,
            "note": note,
            "mode": "PROD",
            "result": "EXECUTED",
        }

        send_telegram(
            title="🚀 DataFlow EXECUTED",
            payload={
                "Version": ENGINE_VERSION,
                "Action": action,
                "Confidence": confidence,
                "Result": "EXECUTED",
            },
        )

    record = {
        "logged_at": datetime.utcnow().isoformat() + "Z",
        "engine_version": ENGINE_VERSION,
        "generated_at": signal.get("generated_at"),
        "state": signal.get("state"),
        "action": action,
        "confidence": confidence,
        "note": note,
        "execution": execution,
    }

    log_audit(record)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()