import json
import uuid
from datetime import datetime
from pathlib import Path

from core.signal_policy import evaluate_signal
from core.state_manager import transition, load_state
from core.telegram_adapter import send_telegram
from core.audit_logger import log_audit

ENGINE_VERSION = "v1.1.0"

ACTIONS_PATH = Path("docs/actions/index.json")


def main():
    run_id = str(uuid.uuid4())
    generated_at = datetime.utcnow().isoformat() + "Z"

    # test signal (как сейчас)
    signal = {
        "confidence": 0.1,
        "note": "confidence 0.1 below threshold after decay"
    }

    decision = evaluate_signal(signal)

    state = load_state()
    action = decision["action"]

    execution = None
    if decision["allow"]:
        transition("ACTIVE")
        execution = {
            "timestamp": generated_at,
            "action": action,
            "confidence": decision["confidence"],
            "note": decision["note"],
            "dry_run": True
        }

        send_telegram(
            title="🚀 DataFlow EXECUTED",
            payload={
                "run_id": run_id,
                "version": ENGINE_VERSION,
                "action": action,
                "confidence": decision["confidence"],
                "note": decision["note"]
            }
        )

    output = {
        "engine_version": ENGINE_VERSION,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": state["state"],
        "action": action,
        "confidence": decision["confidence"],
        "note": decision["note"],
        "execution": execution
    }

    ACTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ACTIONS_PATH.write_text(json.dumps(output, indent=2))

    log_audit(output)


if __name__ == "__main__":
    main()