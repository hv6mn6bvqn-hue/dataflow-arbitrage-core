from pathlib import Path
from datetime import datetime
import json
import uuid

EVENTS_PATH = Path("core/events/events.jsonl")
EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def append_event(event_type: str, payload: dict):
    event = {
        "id": str(uuid.uuid4()),
        "type": event_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": payload
    }

    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return event