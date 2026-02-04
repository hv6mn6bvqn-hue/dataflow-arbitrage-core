from pathlib import Path
from datetime import datetime

LOG_PATH = Path("core/logs/signal.log")
WINDOW_SIZE = 5  # сколько последних записей анализируем
STABLE_THRESHOLD = 3  # сколько стабильных подряд считаем «застоем»

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


def detect_potential_delta(entries):
    if len(entries) < WINDOW_SIZE:
        return None

    stable_count = 0
    avg_confidence = 0.0

    for e in entries:
        if e.get("signal_type") == "stable":
            stable_count += 1
        try:
            avg_confidence += float(e.get("confidence", 0))
        except ValueError:
            pass

    avg_confidence /= len(entries)

    if stable_count >= STABLE_THRESHOLD and avg_confidence > 0.03:
        return {
            "signal_type": "potential_delta",
            "confidence": round(avg_confidence + 0.15, 2),
            "note": "prolonged stability with confidence drift"
        }

    return None


def write_prediction(result):
    ts = datetime.utcnow().isoformat() + "Z"
    with LOG_PATH.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write("source: predictor\n")
        f.write(f"signal_type: {result['signal_type']}\n")
        f.write(f"confidence: {result['confidence']}\n")
        f.write("delta_detected: potential\n")
        f.write(f"note: {result['note']}\n")
        f.write("---\n")


def main():
    entries = read_entries()
    result = detect_potential_delta(entries)
    if result:
        write_prediction(result)


if __name__ == "__main__":
    main()
