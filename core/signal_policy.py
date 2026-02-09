# core/signal_policy.py

THRESHOLD_EXECUTE = 0.9
THRESHOLD_ALERT = 0.7


def evaluate_signal(signal: dict) -> dict:
    confidence = float(signal.get("confidence", 0))

    if confidence >= THRESHOLD_EXECUTE:
        return {
            "allow": True,
            "action": "EXECUTE",
            "confidence": confidence,
            "note": "confidence above EXECUTE threshold",
            "dry_run": False
        }

    if confidence >= THRESHOLD_ALERT:
        return {
            "allow": True,
            "action": "ALERT",
            "confidence": confidence,
            "note": "confidence above ALERT threshold",
            "dry_run": True
        }

    return {
        "allow": False,
        "action": "MONITOR",
        "confidence": confidence,
        "note": "confidence below thresholds",
        "dry_run": True
    }