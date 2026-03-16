import json
import os
from datetime import datetime

INPUT_FILE = "data/anomaly_guarded.json"
OUTPUT_FILE = "data/live_session.json"


def load_signals():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def build_session(signals):

    state = "RUN" if len(signals) > 0 else "PAUSE"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "signals": len(signals),
        "session_state": state
    }


def save_state(data):

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():

    print("[SESSION] start")

    signals = load_signals()

    state = build_session(signals)

    save_state(state)

    print(f"[SESSION] state: {state['session_state']}")


if __name__ == "__main__":
    main()