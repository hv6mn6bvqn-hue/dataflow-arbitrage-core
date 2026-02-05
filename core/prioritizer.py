from pathlib import Path
from datetime import datetime

LOG_PATH = Path("core/logs/signal.log")
WINDOW_SIZE = 8

PRIORITY_MAP = {
    "confidence_spike": 3,
    "potential_delta": 2,
    "activity_detected": 1,
    "stable": 0
}


def read_entries():
    if not LOG_PATH.exists():
        return []

    raw = LOG_PATH.read_text().strip().split("---")
    entries = []

    for block in raw:
        lines = block.strip().splitlines()
        entry = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                entry[k.strip()] = v.strip()
        if entry:
            entries.append(entry)

    return entries[-WINDOW_SIZE:]


def select_top_signal(entries):
    best = None
    best_score = -1

    for e in entries:
        stype = e.get("signal_type")
        score = PRIORITY_MAP.get(stype, -1)

        try:
            conf = float(e.get("confidence", 0))
        except ValueError:
            conf = 0

        total_score = score + conf

        if total_score > best_score:
            best_score = total_score
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
        f.write("note: highest priority signal selected\n")
        f.write("---\n")


def main():
    entries = read_entries()
    if not entries:
        return

    top = select_top_signal(entries)
    if top:
        write_priority_signal(top)


if __name__ == "__main__":
    main()
