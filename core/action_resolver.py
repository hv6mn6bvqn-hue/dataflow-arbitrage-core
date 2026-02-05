from pathlib import Path
import json
from datetime import datetime

ACTIONS_DIR = Path("core/exports/actions")
RESOLVED_DIR = Path("core/exports/actions_resolved")

ACTIONS_DIR.mkdir(parents=True, exist_ok=True)
RESOLVED_DIR.mkdir(parents=True, exist_ok=True)


def resolve_actions(auto_approve=False):
    """
    Обрабатывает pending actions.
    По умолчанию — manual review.
    """

    for action_file in ACTIONS_DIR.glob("action_*.json"):
        action = json.loads(action_file.read_text())

        if action.get("status") != "pending":
            continue

        if auto_approve:
            action["status"] = "approved"
            action["resolved_at"] = datetime.utcnow().isoformat() + "Z"
            action["resolution_note"] = "auto-approved by resolver"
        else:
            action["status"] = "rejected"
            action["resolved_at"] = datetime.utcnow().isoformat() + "Z"
            action["resolution_note"] = "manual review required"

        # сохраняем в resolved
        target = RESOLVED_DIR / action_file.name
        target.write_text(json.dumps(action, indent=2))

        # удаляем исходный
        action_file.unlink()
