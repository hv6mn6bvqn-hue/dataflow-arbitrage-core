from datetime import datetime
from pathlib import Path
import json

from core.signal_policy import policy_allows_action
from core.state_manager import load_state, transition
from core.execution_adapter import execute
from core.telegram_adapter import send_telegram

OUTPUT_PATH = Path("docs/actions/index.json")


def decide_next_state(confidence, current_state):
    if current_state == "IDLE" and confidence >= 0.4:
        return "WATCH"
    if current_state == "WATCH" and confidence >= 0.6:
        return "READY"
    if current_state == "READY" and confidence >= 0.75:
        return "ACTIVE"
    if current_state == "ACTIVE":
        return "COOLDOWN"
    if current_state == "COOLDOWN":
        return "IDLE"
    return current_state


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    allowed, reason = policy_allows_action()
    state_data = load_state()
    current_state = state_data["state"]

    confidence = 0.75 if allowed else 0.3
    next_state = decide_next_state(confidence, current_state)

    if next_state != current_state:
        transition(next_state)

    action_type = "MONITOR"
    execution_result = None

    if next_state == "ACTIVE" and allowed:
        action_type = "EXECUTE"
        execution_result = execute(
            action="EXECUTE",
            confidence=confidence,
            note=reason,
            dry_run=True
        )

        send_telegram(
            f"🚀 *DataFlow Signal*\n"
            f"State: `{next_state}`\n"
            f"Confidence: `{confidence}`\n"
            f"Note: {reason}"
        )

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": next_state,
        "action": action_type,
        "confidence": confidence,
        "note": reason,
        "execution": execution_result
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
