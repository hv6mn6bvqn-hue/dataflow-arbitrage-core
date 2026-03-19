# core/anomaly_guard_engine.py
import json
import os

INPUT_FILE = "sources/venue_rotation.json"
OUTPUT_FILE = "sources/anomaly_guard.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[ANOMALY_GUARD] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    approved_count = 0
    for s in signals:
        # Блокировка аномалий: например, слишком большой PnL
        s["approved"] = abs(s.get("pnl", 0)) < 5000
        if s["approved"]:
            approved_count += 1

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[ANOMALY_GUARD] approved: {approved_count}")

if __name__ == "__main__":
    print("[ANOMALY_GUARD] start")
    run()