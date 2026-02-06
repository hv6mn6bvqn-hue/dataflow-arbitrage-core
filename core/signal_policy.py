from datetime import datetime, timedelta
from pathlib import Path

LOG_PATH = Path("core/logs/signal.log")

# === POLICY PARAMETERS (меняются стратегически) ===
MIN_CONFIDENCE = 0.75
COOLDOWN_MINUTES = 60
MAX_ACTIONS_PER_DAY = 5

# === INTERNAL STATE ===
_action_timestamps = []


def _parse_entries():
    if not LOG_PATH.exists():
        return []

    raw = LOG_PATH.read_text().split("---")
    entries = []

    for block in raw:
        block = block.strip()
        if not block:
            continue

        entry = {}
        for line in block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                entry[k.strip()] = v.strip()
        entries.append(entry)

    return entries


def policy_allows_action():
    global _action_timestamps

    now = datetime.utcnow()

    entries = _parse_entries()
    if not entries:
        return False, "no signals"

    last = entries[-1]

    confidence = float(last.get("confidence", 0))
    if confidence < MIN_CONFIDENCE:
        return False, f"confidence {confidence} below threshold"

    # cooldown
    _action_timestamps = [
        t for t in _action_timestamps
        if now - t < timedelta(days=1)
    ]

    if len(_action_timestamps) >= MAX_ACTIONS_PER_DAY:
        return False, "daily action limit reached"

    if _action_timestamps:
        if now - _action_timestamps[-1] < timedelta(minutes=COOLDOWN_MINUTES):
            return False, "cooldown active"

    _action_timestamps.append(now)
    return True, "policy approved"
