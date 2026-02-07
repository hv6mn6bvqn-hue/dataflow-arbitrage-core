from datetime import datetime
from pathlib import Path
import json

from core.state_manager import load_state
from core.execution_adapter import execute
from core.signal_policy import policy_allows_action
from core.telegram_adapter import send_telegram
from core.audit_logger import log_action

ENGINE_VERSION = "v1.0.0"
OUTPUT_PATH = Path("docs/actions/index.json")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    state = load_state()
    current_state = state.get("state", "IDLE")

    decision = policy_allows_action()

    if decision["allow"]:
        action = "EXECUTE"
        confidence = decision["confidence"]
        note = decision["reason"]

        execution = execute(
            action=action,
            confidence=confidence,
            note=note,
            dry_run=True
        )

        send_telegram(
            f"🚀 DataFlow Signal\n"
            f"Version: {ENGINE_VERSION}\n"
            f"Action: {action}\n"
            f"Confidence: {confidence}\n"
            f"Note: {note}"
        )
    else:
        action = "MONITOR"
        confidence = decision["confidence"]
        note = decision["reason"]
        execution = None

    payload = {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": current_state,
        "action": action,
        "confidence": confidence,
        "note": note,
        "execution": execution
    }

    log_action(payload)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
