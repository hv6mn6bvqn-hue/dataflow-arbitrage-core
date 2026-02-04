from pathlib import Path
from datetime import datetime
import subprocess

log_path = Path("core/logs/signal.log")


def read_last_entry():
    if not log_path.exists():
        return None

    entries = log_path.read_text().strip().split("---")
    if len(entries) < 2:
        return None

    return entries[-2].strip()


def write_entry(signal_type, confidence, note):
    ts = datetime.utcnow().isoformat() + "Z"
    with log_path.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write("source: analyzer\n")
        f.write(f"signal_type: {signal_type}\n")
        f.write(f"confidence: {confidence}\n")
        f.write("delta_detected: true\n")
        f.write(f"note: {note}\n")
        f.write("---\n")


def main():
    last = read_last_entry()

    if last is None:
        write_entry("init", "0.10", "initial signal creation")
    elif "signal_type: none" in last:
        write_entry("activity_detected", "0.35", "state change detected")
    else:
        write_entry("stable", "0.05", "no meaningful change")

    # запускаем predictor как следующий слой
    try:
        subprocess.run(["python", "core/predictor.py"], check=False)
    except Exception:
        pass


if __name__ == "__main__":
    main()
