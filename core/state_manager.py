from pathlib import Path
from datetime import datetime, timedelta
import json

STATE_PATH = Path("core/state.json")

DEFAULT_STATE = {
    "state": "IDLE",
    "last_transition": None
}


def load_state():
    if not STATE_PATH.exists():
        return DEFAULT_STATE.copy()

    return json.loads(STATE_PATH.read_text())


def save_state(state_data):
    STATE_PATH.write_text(json.dumps(state_data, indent=2))


def transition(new_state):
    state = load_state()
    state["state"] = new_state
    state["last_transition"] = datetime.utcnow().isoformat() + "Z"
    save_state(state)
    return state
