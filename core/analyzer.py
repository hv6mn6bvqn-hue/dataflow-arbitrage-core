from pathlib import Path
from datetime import datetime

# Подключаем источники (если доступны)
try:
    from sources.web_signal import generate_signal as web_signal
    WEB_AVAILABLE = True
except Exception:
    WEB_AVAILABLE = False

try:
    from sources.github_signal import generate_signal as github_signal
    GITHUB_AVAILABLE = True
except Exception:
    GITHUB_AVAILABLE = False


log_path = Path("core/logs/signal.log")


def read_last_entry():
    if not log_path.exists():
        return None

    entries = log_path.read_text().strip().split("---")
    if len(entries) < 2:
        return None

    return entries[-2].strip()


def write_entry(signal_type, confidence, note, source):
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
    # 1️⃣ Web Signal — приоритет №1
    if WEB_AVAILABLE:
        signal = web_signal()
        write_entry(
            signal_type=signal.get("signal_type", "web_unknown"),
            confidence=signal.get("confidence", "0.20"),
            note=signal.get("note", ""),
            source="web_signal"
        )
        return

    # 2️⃣ GitHub Signal — приоритет №2
    if GITHUB_AVAILABLE:
        signal = github_signal()
        write_entry(
            signal_type=signal.get("signal_type", "github_unknown"),
            confidence=signal.get("confidence", "0.15"),
            note=signal.get("note", ""),
            source="github_signal"
        )
        return

    # 3️⃣ Fallback — ядро
    last = read_last_entry()

    if last is None:
        write_entry("init", "0.10", "initial signal creation", "analyzer")
        return

    if "signal_type: none" in last:
        write_entry("activity_detected", "0.35", "state change detected", "analyzer")
    else:
        write_entry("stable", "0.05", "no meaningful change", "analyzer")


if __name__ == "__main__":
    main()
