import os
from datetime import datetime

from core.feed_loader import load_latest_signal
from core.signal_policy import evaluate_signal
from core.audit_logger import log_audit
from core.telegram_adapter import send_telegram


ENGINE_VERSION = "v1.0.0"


def build_message(decision: dict) -> str:
    return (
        "🚀 DataFlow EXECUTION\n\n"
        f"Version: {ENGINE_VERSION}\n"
        f"Action: {decision.get('action')}\n"
        f"Confidence: {decision.get('confidence')}\n"
        f"State: {decision.get('state')}\n"
    )


def main():
    print("[ENGINE] starting action engine")

    # 1️⃣ Загружаем последний сигнал
    signal = load_latest_signal()

    if not signal:
        print("[ENGINE] no signal found")
        return

    # 2️⃣ Оцениваем сигнал
    decision = evaluate_signal(signal)

    if not isinstance(decision, dict):
        print("[ENGINE] invalid decision format")
        return

    action = decision.get("action")
    confidence = decision.get("confidence", 0)

    if not action:
        print("[ENGINE] no action returned")
        return

    # 3️⃣ Формируем execution metadata
    execution = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "mode": "PROD",
        "result": "EXECUTED" if action == "EXECUTE" else "SKIPPED"
    }

    decision["execution"] = execution
    decision["engine_version"] = ENGINE_VERSION
    decision["logged_at"] = execution["timestamp"]

    # 4️⃣ Аудит
    log_audit(decision)

    # 5️⃣ Telegram
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[TELEGRAM] missing credentials")
        return

    token = token.strip()
    chat_id = chat_id.strip()

    message = build_message(decision)

    print("[TELEGRAM] sending request")
    send_telegram(
        token=token,
        chat_id=chat_id,
        message=message
    )
    print("[TELEGRAM] message sent")

    print("[ENGINE] completed")


if __name__ == "__main__":
    main()