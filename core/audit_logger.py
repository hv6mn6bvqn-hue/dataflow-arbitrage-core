from pathlib import Path
from datetime import datetime
import json

AUDIT_DIR = Path("audit")
AUDIT_DIR.mkdir(exist_ok=True)

AUDIT_PATH = AUDIT_DIR / "index.json"


def _load_audit():
    if not AUDIT_PATH.exists():
        return []
    return json.loads(AUDIT_PATH.read_text())


def _save_audit(records):
    AUDIT_PATH.write_text(json.dumps(records, indent=2))


def log_audit(entry: dict):
    """
    Append a single audit entry.
    Contract-stable audit logger.
    """

    record = {
        "logged_at": datetime.utcnow().isoformat() + "Z",
        **entry
    }

    records = _load_audit()
    records.append(record)
    _save_audit(records)

    return record