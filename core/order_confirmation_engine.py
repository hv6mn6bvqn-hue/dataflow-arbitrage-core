import json
import os

INPUT_FILE = "sources/live_routed.json"
OUTPUT_FILE = "sources/order_confirmed.json"


def load_data():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[CONFIRMATION] input missing: {INPUT_FILE}")
        return []


def confirm(signals):
    confirmed = []

    for signal in signals:
        # проверка успешной исполнения
        status = signal.get("execution_status", "PENDING")
        fragments = signal.get("executed_fragments", 0)

        if status == "SUCCESS" and fragments > 0:
            signal["confirmation"] = "CONFIRMED"
            confirmed.append(signal)
        else:
            signal["confirmation"] = "FAILED"

    return confirmed


def save(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    print("[CONFIRMATION] start")

    signals = load_data()

    if not signals:
        print("[CONFIRMATION] no signals to confirm")
        return

    result = confirm(signals)

    save(result)

    print(f"[CONFIRMATION] confirmed: {len(result)} / {len(signals)} signals")


if __name__ == "__main__":
    main()