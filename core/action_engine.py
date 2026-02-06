from pathlib import Path
from datetime import datetime
import json

from core.signal_policy import is_actionable_signal

FEED_PATH = Path("feed/index.json")
ACTIONS_LOG = Path("core/logs/actions.log")

def load_feed():
    if not FEED_PATH.exists():
        return []

    data = json.loads(FEED_PATH.read_text())
    return data.get("signals", [])

def write_action(signal):
    ts = datetime.utcnow().isoformat() + "Z"

    ACTIONS_LOG.parent.mkdir(parents=True, exist_ok=True)

    with ACTIONS_LOG.open("a") as f:
        f.write(f"timestamp: {ts}\n")
        f.write(f"action: SIMULATED_EXECUTION\n")
        f.write(f"signal_type: {signal['type']}\n")
        f.write(f"confidence: {signal['confidence']}\n")
        f.write(f"source: action_engine\n")
        f.write("---\n")

def main():
    signals = load_feed()

    if not signals:
        return

    for signal in signals:
        if is_actionable_signal(signal):
            write_action(signal)

if __name__ == "__main__":
    main()
