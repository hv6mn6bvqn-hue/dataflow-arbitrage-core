import os
import requests


def send_telegram(title: str, payload: dict):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[TELEGRAM] skipped — credentials not set")
        return

    # 🔒 КРИТИЧЕСКИЙ FIX M7.2
    # Убираем \n, пробелы, мусор из GitHub Secrets
    token = token.strip()
    chat_id = chat_id.strip()

    message = title + "\n"
    for k, v in payload.items():
        message += f"{k}: {v}\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=10,
    )

    response.raise_for_status()
    print("[TELEGRAM] message sent")