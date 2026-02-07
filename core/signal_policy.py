from core.analyzer import read_last_entry


CONFIDENCE_THRESHOLD = 0.7


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

    if "confidence:" in last:
        try:
            confidence = float(
                last.split("confidence:")[1].splitlines()[0].strip()
            )
        except Exception:
            confidence = 0.0
    else:
        confidence = 0.0

    if confidence >= CONFIDENCE_THRESHOLD:
        return {
            "allow": True,
            "confidence": confidence,
            "reason": f"confidence {confidence} >= threshold"
        }

    return {
        "allow": False,
        "confidence": confidence,
        "reason": f"confidence {confidence} below threshold"
    }
