from pathlib import Path
from datetime import datetime
import json

AUDIT_PATH = Path("docs/audit/actions_history.json")


def log_action(payload: dict):
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if AUDIT_PATH.exists():
        history = json.loads(AUDIT_PATH.read_text())
    else:
        history = []

    entry = {
        "logged_at": datetime.utcnow().isoformat() + "Z",
        **payload
    }

    history.append(entry)

    AUDIT_PATH.write_text(json.dumps(history, indent=2))
