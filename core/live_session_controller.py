# core/live_session_controller.py
import json
import os

INPUT_FILE = "sources/anomaly_guard.json"
OUTPUT_FILE = "sources/live_session.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        state = "PAUSE"
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)
        # Сессия активна, если хотя бы один сигнал approved
        state = "RUN" if any(s.get("approved", False) for s in signals) else "PAUSE"

    with open(OUTPUT_FILE, "w") as f:
        json.dump({"state": state}, f)

    print(f"[SESSION] state: {state}")

if __name__ == "__main__":
    print("[SESSION] start")
    run()