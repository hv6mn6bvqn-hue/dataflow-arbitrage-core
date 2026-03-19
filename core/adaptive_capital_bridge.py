# core/adaptive_capital_bridge.py
import json
import os

INPUT_FILE = "sources/live_capital.json"
OUTPUT_FILE = "sources/capital_bridge.json"

def run():
    if not os.path.exists(INPUT_FILE):
        equity = 10000
    else:
        with open(INPUT_FILE) as f:
            data = json.load(f)
            equity = data.get("equity", 10000)

    # Для модели: консенсус = equity
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"consensus": equity}, f)

    print(f"[CAPITAL_BRIDGE] consensus: {equity}")

if __name__ == "__main__":
    print("[CAPITAL_BRIDGE] start")
    run()