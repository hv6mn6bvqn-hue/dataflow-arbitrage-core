# core/execution_policy_bridge.py
import json
import os

INPUT_FILE = "sources/live_session.json"
OUTPUT_FILE = "sources/policy_bridge.json"

def run():
    if not os.path.exists(INPUT_FILE):
        state = "PAUSE"
        print("[EXEC_POLICY_BRIDGE] input missing")
    else:
        with open(INPUT_FILE) as f:
            session = json.load(f)
        state = session.get("state", "PAUSE")

    # Если сессия активна, разрешаем мост политики
    bridged = state == "RUN"

    with open(OUTPUT_FILE, "w") as f:
        json.dump({"bridged": bridged}, f)

    print(f"[EXEC_POLICY_BRIDGE] bridged: {bridged}")

if __name__ == "__main__":
    print("[EXEC_POLICY_BRIDGE] start")
    run()