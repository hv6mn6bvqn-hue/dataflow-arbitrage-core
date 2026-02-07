import os
import requests


def send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[TELEGRAM] skipped — credentials not set")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    r = requests.post(url, json=payload, timeout=10)

    if r.status_code != 200:
        print("[TELEGRAM] failed", r.text)
        return False

    print("[TELEGRAM] sent")
    return True
