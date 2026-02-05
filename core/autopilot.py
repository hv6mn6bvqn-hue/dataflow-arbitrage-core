from pathlib import Path
import json
from datetime import datetime

EXPORT_FILE = Path("core/exports/primary_signal.json")
STATE_FILE = Path("core/state/autopilot_state.json")
LOG_PATH = Path("core/logs/signal.log")

CONF_THRESHOLD = 0.6


def load_signal():
    if not EXPORT_FILE.exists():
        return None
    return json.loads(EXPORT_FILE.read_text())


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {"actions_taken": 0}
    STATE_FILE.write_text(json.dumps(state, indent=2))
    return state


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def log_action(note):
    ts = datetime.utcnow().isoformat() + "Z"
    with LOG_PATH.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write("source: autopilot\n")
        f.write("signal_type: ACTION_TRIGGERED\n")
        f.write("confidence: 1.00\n")
        f.write("delta_detected: action\n")
        f.write(f"note: {note}\n")
        f.write("---\n")


def main():
    signal = load_signal()
    if not signal:
        return

    try:
        confidence = float(signal.get("confidence", 0))
    except ValueError:
        return

    if confidence < CONF_THRESHOLD:
        return

    state = load_state()
    state["actions_taken"] += 1

    # AUTODEЙСТВИЕ B:
    # фиксация сильного сигнала
    strong_dir = Path("core/exports/strong_signals")
    strong_dir.mkdir(parents=True, exist_ok=True)

    filename = f"signal_{state['actions_taken']}.json"
    (strong_dir / filename).write_text(json.dumps(signal, indent=2))

    log_action("strong signal accepted and stored")
    save_state(state)


if __name__ == "__main__":
    main()
