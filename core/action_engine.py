from datetime import datetime

from core.feed_loader import load_latest_signal
from core.signal_policy import evaluate_signal
from core.state_manager import transition
from core.audit_logger import log_audit
from core.telegram_adapter import send_telegram
from core.events.event_store import append_event

ENGINE_VERSION = "v1.2.0"


def main():
    signal = load_latest_signal()
    append_event("signal_loaded", signal)

    decision = evaluate_signal(signal)
    append_event("decision_made", decision)

    state = transition("ACTIVE")

    result = {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": state["state"],
        "action": decision["action"],
        "confidence": decision["confidence"],
        "note": decision["note"],
        "execution": None
    }

    append_event("state_transition", state)

    if decision["allow"] and decision["action"] in ("EXECUTE", "ALERT"):
        execution = {
            "timestamp": result["generated_at"],
            "action": decision["action"],
            "confidence": decision["confidence"],
            "dry_run": decision["dry_run"]
        }

        result["execution"] = execution
        append_event("action_executed", execution)

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
    append_event("audit_logged", result)


if __name__ == "__main__":
    main()