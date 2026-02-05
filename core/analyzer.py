from pathlib import Path
from datetime import datetime
import json

from predictor import run as run_predictor
from confirmation import register_signal, is_confirmed
from action_hooks import emit_action

log_path = Path("core/logs/signal.log")
export_dir = Path("core/exports/strong_signals")

export_dir.mkdir(parents=True, exist_ok=True)


def write_log(entry):
    with log_path.open("a") as f:
        f.write(f"timestamp: {entry['timestamp']}\n")
        f.write(f"source: {entry['source']}\n")
        f.write(f"signal_type: {entry['signal_type']}\n")
        f.write(f"confidence: {entry['confidence']}\n")
        f.write("delta_detected: true\n")
        f.write(f"note: {entry['note']}\n")
        f.write("---\n")


def export_signal(entry):
    fname = f"signal_{entry['timestamp'].replace(':', '-')}.json"
    path = export_dir / fname
    with path.open("w") as f:
        json.dump(entry, f, indent=2)


def main():
    entry = run_predictor()
    write_log(entry)

    buffer = register_signal(entry)

    if is_confirmed(buffer):
        confirmed_signal = {
            **entry,
            "confirmed": True,
            "confirmation_window": len(buffer)
        }

        export_signal(confirmed_signal)
        emit_action(confirmed_signal)


if __name__ == "__main__":
    main()
