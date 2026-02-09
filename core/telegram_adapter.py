import os
import requests

TELEGRAM_API = "https://api.telegram.org"


def send_telegram(message: str, title: str | None = None):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[TELEGRAM] skipped — credentials not set")
        return

    text = message
    if title:
        text = f"{title}\n\n{message}"

    url = f"{TELEGRAM_API}/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print("[TELEGRAM] message sent")
    except Exception as e:
        print(f"[TELEGRAM] error: {e}")