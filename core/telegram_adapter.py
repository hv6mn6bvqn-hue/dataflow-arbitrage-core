import os
import requests


def send_telegram(message: str):
    token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("[TELEGRAM] skipped — credentials not set")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("[TELEGRAM] message sent")
        return True
    except Exception as e:
        print(f"[TELEGRAM] error: {e}")
        return False
