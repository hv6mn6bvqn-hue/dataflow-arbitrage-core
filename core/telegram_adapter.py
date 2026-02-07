import os
import json
import urllib.request


def send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[TELEGRAM] skipped — credentials not set")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                print("[TELEGRAM] failed", response.read().decode())
                return False
    except Exception as e:
        print("[TELEGRAM] error", str(e))
        return False

    print("[TELEGRAM] sent")
    return True
