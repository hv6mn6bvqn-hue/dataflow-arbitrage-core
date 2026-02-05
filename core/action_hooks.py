from pathlib import Path
import json
from datetime import datetime

ACTIONS_DIR = Path("core/exports/actions")

ACTIONS_DIR.mkdir(parents=True, exist_ok=True)


def emit_action(signal):
    action = {
        "action_type": "STRONG_SIGNAL_CONFIRMED",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "signal": signal,
        "status": "pending",
        "recommended_mode": "manual_review"
    }

    fname = f"action_{action['timestamp'].replace(':', '-')}.json"
    path = ACTIONS_DIR / fname

    with path.open("w") as f:
        json.dump(action, f, indent=2)

    return path
