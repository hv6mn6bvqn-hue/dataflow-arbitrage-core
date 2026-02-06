def is_actionable_signal(signal: dict) -> bool:
    """
    Central decision policy.
    Determines whether a signal is strong enough to trigger an action.
    """

    if not isinstance(signal, dict):
        return False

    signal_type = str(signal.get("type", "")).lower()
    confidence = float(signal.get("confidence", 0))

    # стратегический whitelist
    actionable_types = {
        "potential_strong",
        "action_triggered",
        "strong_signal"
    }

    if signal_type in actionable_types and confidence >= 0.7:
        return True

    return False
