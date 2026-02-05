from pathlib import Path
from datetime import datetime
import json

LOG_PATH = Path("core/logs/signal.log")
EXPORT_PATH = Path("core/exports")
EXPORT_FILE = EXPORT_PATH / "primary_signal.json"


def read_last_primary():
    if not LOG_PATH.exists():
        return None

    blocks = LOG_PATH.read_text().strip().split("---")
    for block in reversed(blocks):
        lines = block.strip().splitlines()
        entry = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                entry[k.strip()] = v.strip()
        if entry.get("source") == "prioritizer":
            return entry

    return None


def export_signal(signal):
    EXPORT_PATH.mkdir(parents=True, exist_ok=True)

    payload = {
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "signal_type": signal.get("signal_type"),
        "confidence": signal.get("confidence"),
        "note": signal.get("note"),
        "status": "active"
    }

    EXPORT_FILE.write_text(json.dumps(payload, indent=2))


def main():
    primary = read_last_primary()
    if primary:
        export_signal(primary)


if __name__ == "__main__":
    main()
