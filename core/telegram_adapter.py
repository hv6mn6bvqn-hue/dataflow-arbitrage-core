import os
import requests


def send_telegram(message: str):
    """
    Unified Telegram adapter.
    Reads token + chat_id from environment.
    """

    token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("[TELEGRAM] missing credentials")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("[TELEGRAM] message sent")
    except Exception as e:
        print(f"[TELEGRAM] error: {e}")