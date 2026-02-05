from pathlib import Path
import json

BUFFER_PATH = Path("core/logs/confirmation_buffer.json")
REQUIRED_CONFIRMATIONS = 2


def load_buffer():
    if not BUFFER_PATH.exists():
        return []
    return json.loads(BUFFER_PATH.read_text())


def save_buffer(buffer):
    BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)
    BUFFER_PATH.write_text(json.dumps(buffer, indent=2))


def register_signal(entry):
    buffer = load_buffer()
    buffer.append(entry)

    # чистим старые, оставляем последние 3
    buffer = buffer[-3:]
    save_buffer(buffer)
    return buffer


def is_confirmed(buffer):
    strong = [
        e for e in buffer
        if e["signal_type"] == "potential_strong" and e["confidence"] >= 0.8
    ]
    return len(strong) >= REQUIRED_CONFIRMATIONS
