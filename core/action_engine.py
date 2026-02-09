# core/action_engine.py

from datetime import datetime

from core.feed_loader import load_latest_signal
from core.signal_policy import evaluate_signal
from core.state_manager import transition
from core.audit_logger import log_audit
from core.telegram_adapter import send_telegram

ENGINE_VERSION = "v1.1.0"


def main():
    signal = load_latest_signal()
    decision = evaluate_signal(signal)

    result = {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": transition("ACTIVE")["state"],
        "action": decision["action"],
        "confidence": decision["confidence"],
        "note": decision["note"],
        "execution": None
    }

    if decision["allow"]:
        if decision["action"] in ("EXECUTE", "ALERT"):
            result["execution"] = {
                "timestamp": result["generated_at"],
                "action": decision["action"],
                "confidence": decision["confidence"],
                "dry_run": decision["dry_run"]
            }

            send_telegram(
                title=f"🚀 DataFlow {decision['action']}",
                message=(
                    f"Version: {ENGINE_VERSION}\n"
                    f"Confidence: {decision['confidence']}\n"
                    f"Note: {decision['note']}\n"
                    f"Dry run: {decision['dry_run']}"
                )
            )

    log_audit(result)


if __name__ == "__main__":
    main()