from pathlib import Path
from datetime import datetime

log_path = Path("core/logs/signal.log")
EXPORT_DIR = Path("core/exports/strong_signals")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_confidence(raw):
    return max(0.0, min(1.0, round(raw, 2)))


def classify_tier(confidence):
    if confidence >= 0.85:
        return "critical"
    if confidence >= 0.65:
        return "strong"
    if confidence >= 0.40:
        return "medium"
    return "weak"


def write_export(signal):
    ts = signal["timestamp"].replace(":", "").replace("-", "")
    fname = f"signal_{ts}.json"
    (EXPORT_DIR / fname).write_text(
        __import__("json").dumps(signal, indent=2)
    )


def read_last_entry():
    if not log_path.exists():
        return None

    entries = log_path.read_text().strip().split("---")
    if len(entries) < 2:
        return None

    return entries[-2]


def write_log(signal):
    with log_path.open("a") as f:
        for k, v in signal.items():
            f.write(f"{k}: {v}\n")
        f.write("---\n")


def main():
    last = read_last_entry()

    base_confidence = 0.1
    note = "baseline"

    if last and "activity_detected" in last:
        base_confidence = 0.55
        note = "recurrent activity"

    if last and "strong" in last:
        base_confidence = 0.75
        note = "reinforced signal"

    confidence = normalize_confidence(base_confidence)
    tier = classify_tier(confidence)

    signal = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "signal_type": "arbitrage_delta",
        "confidence": confidence,
        "tier": tier,
        "confirmed": tier in ("strong", "critical"),
        "note": note
    }

    write_log(signal)
    write_export(signal)


if __name__ == "__main__":
    main()
