from datetime import datetime
import json

from core.signal_policy import evaluate_signal
from core.state_manager import transition, load_state
from core.audit_logger import log_audit
from core.telegram_adapter import send_telegram
from core.feed_loader import load_latest_signal

ENGINE_VERSION = "v1.0.0"


def main():
    signal = load_latest_signal()
    state = load_state()

    if not signal:
        print("[ENGINE] No signal found")
        return

    decision = evaluate_signal(signal)

    action = decision["decision"]  # ← КЛЮЧЕВОЕ ИЗМЕНЕНИЕ
    confidence = decision["confidence"]

    execution = None

    if action == "EXECUTE":
        transition("ACTIVE")
        execution = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "EXECUTE",
            "confidence": confidence,
            "note": decision["explanation"],
            "dry_run": True,
        }

        send_telegram(
            title="🚀 DataFlow EXECUTED",
            message=(
                f"Version: {ENGINE_VERSION}\n"
                f"Action: EXECUTE\n"
                f"Confidence: {confidence}\n"
                f"Reason: {decision['explanation']}"
            )
        )

    elif action == "MONITOR":
        transition("ACTIVE")

    else:  # IGNORE
        transition("IDLE")

    output = {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": load_state()["state"],
        "action": action,
        "confidence": confidence,
        "note": decision["explanation"],
        "execution": execution,
    }

    print(json.dumps(output, indent=2))
    log_audit(output)


if __name__ == "__main__":
    main()