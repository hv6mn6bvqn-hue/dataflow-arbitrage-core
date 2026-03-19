# core/venue_rotation_engine.py
import json
import os

INPUT_FILE = "sources/execution_confidence.json"
OUTPUT_FILE = "sources/venue_rotation.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[VENUE_ROTATION] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    active_count = 0
    for s in signals:
        # Если confidence >= 0.7 — активируем
        s["active"] = s.get("confidence", 0) >= 0.7
        if s["active"]:
            active_count += 1

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[VENUE_ROTATION] active: {active_count}")

if __name__ == "__main__":
    print("[VENUE_ROTATION] start")
    run()