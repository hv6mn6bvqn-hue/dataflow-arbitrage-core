# core/exchange_sandbox_guard.py
import json
import os

INPUT_FILE = "sources/policy_bridge.json"
OUTPUT_FILE = "sources/sandbox_guard.json"

def run():
    if not os.path.exists(INPUT_FILE):
        allow_execution = False
        print("[SANDBOX_GUARD] input missing")
    else:
        with open(INPUT_FILE) as f:
            bridge = json.load(f)
        allow_execution = bridge.get("bridged", False)

    with open(OUTPUT_FILE, "w") as f:
        json.dump({"guarded": not allow_execution}, f)

    print(f"[SANDBOX_GUARD] guarded: {not allow_execution}")

if __name__ == "__main__":
    print("[SANDBOX_GUARD] start")
    run()