from datetime import datetime

THRESHOLD_EXECUTE = 0.9
THRESHOLD_MONITOR = 0.3


def evaluate_signal(signal: dict) -> dict:
    """
    Unified signal evaluation policy.
    Returns a DECISION DICT (contract-stable).
    """

    confidence = float(signal.get("confidence", 0.0))
    note = signal.get("note", "")

    if confidence >= THRESHOLD_EXECUTE:
        return {
            "allow": True,
            "action": "EXECUTE",
            "confidence": confidence,
            "note": note or "confidence above execute threshold",
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }

    if confidence >= THRESHOLD_MONITOR:
        return {
            "allow": False,
            "action": "MONITOR",
            "confidence": confidence,
            "note": note or "confidence in monitor range",
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }

    return {
        "allow": False,
        "action": "MONITOR",
        "confidence": confidence,
        "note": note or "confidence below threshold",
        "evaluated_at": datetime.utcnow().isoformat() + "Z"
    }