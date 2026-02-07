from datetime import datetime, timedelta
from core.analyzer import read_last_entry
from core.state_manager import load_state, save_state


CONFIDENCE_THRESHOLD = 0.7
COOLDOWN_MINUTES = 60  # бизнес-решение: не чаще 1 раза в час


def _utcnow():
    return datetime.utcnow()


def policy_allows_action():
    """
    Returns:
    {
        "allow": bool,
        "confidence": float,
        "reason": str
    }
    """

    last = read_last_entry()
    if not last:
        return {
            "allow": False,
            "confidence": 0.0,
            "reason": "no signals available"
        }

    # parse confidence
    try:
        confidence = float(
            last.split("confidence:")[1].splitlines()[0].strip()
        )
    except Exception:
        confidence = 0.0

    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "allow": False,
            "confidence": confidence,
            "reason": f"confidence {confidence} below threshold"
        }

    # cooldown check
    state = load_state()
    last_exec_ts = state.get("last_exec_at")

    if last_exec_ts:
        last_exec_dt = datetime.fromisoformat(last_exec_ts.replace("Z", ""))
        if _utcnow() - last_exec_dt < timedelta(minutes=COOLDOWN_MINUTES):
            return {
                "allow": False,
                "confidence": confidence,
                "reason": "cooldown active"
            }

    # allow + persist exec timestamp
    state["last_exec_at"] = _utcnow().isoformat() + "Z"
    save_state(state)

    return {
        "allow": True,
        "confidence": confidence,
        "reason": "threshold passed and cooldown cleared"
    }
