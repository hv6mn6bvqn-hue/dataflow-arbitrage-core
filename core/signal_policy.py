from datetime import datetime

CONFIDENCE_THRESHOLD_EXECUTE = 0.8
CONFIDENCE_THRESHOLD_MONITOR = 0.3


def evaluate_signal(signal: dict) -> dict:
    """
    Explainable decision engine.
    Returns structured decision with reasons.
    """

    confidence = float(signal.get("confidence", 0))
    signal_type = signal.get("type", "unknown")

    rules_triggered = []
    decision = "IGNORE"

    # Rule 1: High confidence → EXECUTE
    if confidence >= CONFIDENCE_THRESHOLD_EXECUTE:
        decision = "EXECUTE"
        rules_triggered.append(
            f"confidence >= {CONFIDENCE_THRESHOLD_EXECUTE}"
        )

    # Rule 2: Medium confidence → MONITOR
    elif confidence >= CONFIDENCE_THRESHOLD_MONITOR:
        decision = "MONITOR"
        rules_triggered.append(
            f"{CONFIDENCE_THRESHOLD_MONITOR} <= confidence < {CONFIDENCE_THRESHOLD_EXECUTE}"
        )

    # Rule 3: Low confidence → IGNORE
    else:
        decision = "IGNORE"
        rules_triggered.append(
            f"confidence < {CONFIDENCE_THRESHOLD_MONITOR}"
        )

    explanation = (
        f"Decision '{decision}' because "
        f"confidence={confidence} and signal_type='{signal_type}'. "
        f"Rules: {', '.join(rules_triggered)}"
    )

    return {
        "decision": decision,
        "confidence": confidence,
        "signal_type": signal_type,
        "rules_triggered": rules_triggered,
        "explanation": explanation,
        "evaluated_at": datetime.utcnow().isoformat() + "Z",
    }