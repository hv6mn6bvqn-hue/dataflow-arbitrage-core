from pathlib import Path
from datetime import datetime

# Попытка подключить внешний источник
try:
    from sources.github_signal import generate_signal
    GITHUB_SIGNAL_AVAILABLE = True
except Exception:
    GITHUB_SIGNAL_AVAILABLE = False


log_path = Path("core/logs/signal.log")


def read_last_entry():
    if not log_path.exists():
        return None

    entries = log_path.read_text().strip().split("---")
    if len(entries) < 2:
        return None

    return entries[-2].strip()


def write_entry(signal_type, confidence, note, source="analyzer"):
    ts = datetime.utcnow().isoformat() + "Z"
    with log_path.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write(f"source: {source}\n")
        f.write(f"signal_type: {signal_type}\n")
        f.write(f"confidence: {confidence}\n")
        f.write("delta_detected: true\n")
        f.write(f"note: {note}\n")
        f.write("---\n")


def main():
    last = read_last_entry()

    # 1️⃣ Если доступен GitHub-источник — используем его
    if GITHUB_SIGNAL_AVAILABLE:
        signal = generate_signal()
        write_entry(
            signal_type=signal.get("signal_type", "external"),
            confidence=signal.get("confidence", "0.20"),
            note=signal.get("note", "github signal"),
            source="github_signal"
        )
        return

    # 2️⃣ Fallback — старая логика (как у тебя было)
    if last is None:
        write_entry("init", "0.10", "initial signal creation")
        return

    if "signal_type: none" in last:
        write_entry("activity_detected", "0.35", "state change detected")
    else:
        write_entry("stable", "0.05", "no meaningful change")


if __name__ == "__main__":
    main()
