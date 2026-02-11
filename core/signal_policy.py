from datetime import datetime


ENGINE_VERSION = "v1.0.0"


def evaluate_signal(signal: dict) -> dict:
    """
    Единственная точка принятия решения.

    Всегда возвращает decision в стандартизированном формате.
    """

    if not signal:
        return build_decision(
            state="IDLE",
            action="SKIP",
            confidence=0.0,
            note="empty signal"
        )

    confidence = float(signal.get("confidence", 0))
    state = signal.get("state", "ACTIVE")

    # Бизнес-пороги
    if confidence >= 0.9:
        action = "EXECUTE"
        note = "high confidence threshold reached"
    elif confidence >= 0.75:
        action = "ALERT"
        note = "medium confidence alert zone"
    else:
        action = "SKIP"
        note = "confidence below execution threshold"

    return build_decision(
        state=state,
        action=action,
        confidence=confidence,
        note=note
    )


def build_decision(state: str, action: str, confidence: float, note: str) -> dict:
    return {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "state": state,
        "action": action,
        "confidence": round(confidence, 4),
        "note": note
    }