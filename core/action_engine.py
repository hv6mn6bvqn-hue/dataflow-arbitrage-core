from datetime import datetime
from pathlib import Path
import json

from core.state_manager import transition, load_state
from core.execution_adapter import execute
from core.telegram_adapter import send_telegram

OUTPUT_PATH = Path("docs/actions/index.json")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # FORCE ACTIVE — TEST ONLY
    transition("ACTIVE")

    confidence = 0.99
    reason = "forced test signal"

    execution_result = execute(
        action="EXECUTE",
        confidence=confidence,
        note=reason,
        dry_run=True
    )

    send_telegram(
        f"🚀 *DataFlow Test Signal*\n"
        f"State: `ACTIVE`\n"
        f"Confidence: `{confidence}`\n"
        f"Note: {reason}"
    )

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": "ACTIVE",
        "action": "EXECUTE",
        "confidence": confidence,
        "note": reason,
        "execution": execution_result
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
