from datetime import datetime, timedelta
from core.analyzer import read_last_entry
from core.state_manager import load_state, save_state


CONFIDENCE_THRESHOLD = 0.7
COOLDOWN_MINUTES = 60
DECAY_HALF_LIFE_MINUTES = 120  # через 2 часа доверие падает в 2 раза


def _utcnow():
    return datetime.utcnow()


def _apply_decay(confidence: float, age_minutes: float) -> float:
    if age_minutes <= 0:
        return confidence
    decay_factor = 0.5 ** (age_minutes / DECAY_HALF_LIFE_MINUTES)
    return round(confidence * decay_factor, 4)


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
        raw_confidence = float(
            last.split("confidence:")[1].splitlines()[0].strip()
        )
    except Exception:
        raw_confidence = 0.0

    # parse timestamp
    try:
        ts_line = [l for l in last.splitlines() if l.startswith("timestamp:")][0]
        ts = datetime.fromisoformat(ts_line.split("timestamp:")[1].strip().replace("Z", ""))
        age_minutes = (_utcnow() - ts).total_seconds() / 60
    except Exception:
        age_minutes = 0.0

    effective_confidence = _apply_decay(raw_confidence, age_minutes)

    if effective_confidence < CONFIDENCE_THRESHOLD:
        return {
            "allow": False,
            "confidence": effective_confidence,
            "reason": f"confidence {effective_confidence} below threshold after decay"
        }

    # cooldown check
    state = load_state()
    last_exec_ts = state.get("last_exec_at")

    if last_exec_ts:
        last_exec_dt = datetime.fromisoformat(last_exec_ts.replace("Z", ""))
        if _utcnow() - last_exec_dt < timedelta(minutes=COOLDOWN_MINUTES):
            return {
                "allow": False,
                "confidence": effective_confidence,
                "reason": "cooldown active"
            }

    # allow + persist exec timestamp
    state["last_exec_at"] = _utcnow().isoformat() + "Z"
    save_state(state)

    return {
        "allow": True,
        "confidence": effective_confidence,
        "reason": "threshold passed with decay applied"
    }
