from pathlib import Path
from datetime import datetime
import json

LOG_PATH = Path("core/logs/signal.log")
EXPORT_DIR = Path("core/exports/actions")
EXPORT_FILE = EXPORT_DIR / "index.json"

ACTION_CONFIDENCE_THRESHOLD = 0.8


def parse_log_entries():
    if not LOG_PATH.exists():
        return []

    raw = LOG_PATH.read_text().strip().split("---")
    entries = []

    for block in raw:
        block = block.strip()
        if not block:
            continue

        entry = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            entry[k.strip()] = v.strip()

        entries.append(entry)

    return entries


def is_actionable(entry):
    try:
        confidence = float(entry.get("confidence", 0))
    except ValueError:
        return False

    signal_type = entry.get("signal_type", "").lower()

    return confidence >= ACTION_CONFIDENCE_THRESHOLD and signal_type in {
        "potential_strong",
        "action_triggered"
    }


def build_action_feed(entries):
    actions = []

    for e in entries:
        if not is_actionable(e):
            continue

        actions.append({
            "timestamp": e.get("timestamp"),
            "type": e.get("signal_type"),
            "confidence": float(e.get("confidence", 0)),
            "source": "dataflow"
        })

    return {
        "feed_version": "v1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "action_count": len(actions),
        "actions": actions
    }


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    entries = parse_log_entries()
    feed = build_action_feed(entries)

    EXPORT_FILE.write_text(
        json.dumps(feed, indent=2)
    )

    print(f"[action_engine] exported {feed['action_count']} actions")


if __name__ == "__main__":
    main()
