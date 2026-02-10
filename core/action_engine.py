import os
import json
from datetime import datetime

from core.feed_loader import load_latest_signal
from core.signal_policy import evaluate_signal
from core.audit_logger import log_audit
from core.telegram_notifier import send_telegram


ENGINE_VERSION = "v1.0.0"


def main():
    signal = load_latest_signal()
    decision = evaluate_signal(signal)

    execution = None

    if decision["action"] == "EXECUTE":
        execution = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": decision["action"],
            "confidence": decision["confidence"],
            "note": decision["note"],
            "mode": "PROD",
            "result": "EXECUTED",
        }

        send_telegram(
            title="🚀 DataFlow EXECUTED",
            payload={
                "Version": ENGINE_VERSION,
                "Action": decision["action"],
                "Confidence": decision["confidence"],
                "Result": "EXECUTED",
            },
        )

    record = {
        "logged_at": datetime.utcnow().isoformat() + "Z",
        "engine_version": ENGINE_VERSION,
        "generated_at": signal.get("generated_at"),
        "state": decision["state"],
        "action": decision["action"],
        "confidence": decision["confidence"],
        "note": decision["note"],
        "execution": execution,
    }

    log_audit(record)


if __name__ == "__main__":
    main()