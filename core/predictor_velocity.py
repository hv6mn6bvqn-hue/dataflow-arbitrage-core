from pathlib import Path
from datetime import datetime

LOG_PATH = Path("core/logs/signal.log")
WINDOW_SIZE = 6


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


def detect_velocity(entries):
    if len(entries) < WINDOW_SIZE:
        return None

    confidences = []
    for e in entries:
        try:
            confidences.append(float(e.get("confidence", 0)))
        except ValueError:
            pass

    if len(confidences) < 3:
        return None

    velocity = confidences[-1] - confidences[0]

    if velocity > 0.25:
        return {
            "signal_type": "confidence_spike",
            "confidence": round(min(confidences[-1] + 0.1, 1.0), 2),
            "note": "rapid confidence acceleration"
        }

    return None


def write_prediction(result):
    ts = datetime.utcnow().isoformat() + "Z"
    with LOG_PATH.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write("source: predictor_velocity\n")
        f.write(f"signal_type: {result['signal_type']}\n")
        f.write(f"confidence: {result['confidence']}\n")
        f.write("delta_detected: potential\n")
        f.write(f"note: {result['note']}\n")
        f.write("---\n")


def main():
    entries = read_entries()
    result = detect_velocity(entries)
    if result:
        write_prediction(result)


if __name__ == "__main__":
    main()
