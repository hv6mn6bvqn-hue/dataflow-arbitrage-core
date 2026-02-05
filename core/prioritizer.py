from pathlib import Path
from datetime import datetime
import json

LOG_PATH = Path("core/logs/signal.log")
WEIGHTS_PATH = Path("core/state/weights.json")
WINDOW_SIZE = 8

PRIORITY_MAP = {
    "confidence_spike": 3,
    "potential_delta": 2,
    "activity_detected": 1,
    "stable": 0
}


def load_weights():
    if WEIGHTS_PATH.exists():
        return json.loads(WEIGHTS_PATH.read_text())
    return {}


def read_entries():
    if not LOG_PATH.exists():
        return []

    raw = LOG_PATH.read_text().strip().split("---")
    entries = []

    for block in raw:
        entry = {}
        for line in block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                entry[k.strip()] = v.strip()
        if entry:
            entries.append(entry)

    return entries[-WINDOW_SIZE:]


def select_top_signal(entries, weights):
    best = None
    best_score = -1

    for e in entries:
        stype = e.get("signal_type")
        base = PRIORITY_MAP.get(stype, 0)

        try:
            conf = float(e.get("confidence", 0))
        except ValueError:
            conf = 0

        source = e.get("source", "")
        weight = weights.get(source, 1.0)

        score = (base + conf) * weight

        if score > best_score:
            best_score = score
            best = e

    return best


def write_priority_signal(signal):
    ts = datetime.utcnow().isoformat() + "Z"
    with LOG_PATH.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write("source: prioritizer\n")
        f.write(f"signal_type: PRIMARY::{signal.get('signal_type')}\n")
        f.write(f"confidence: {signal.get('confidence')}\n")
        f.write("delta_detected: prioritized\n")
        f.write("note: self-learning weighted selection\n")
        f.write("---\n")


def main():
    weights = load_weights()
    entries = read_entries()
    if not entries:
        return

    top = select_top_signal(entries, weights)
    if top:
        write_priority_signal(top)


if __name__ == "__main__":
    main()
