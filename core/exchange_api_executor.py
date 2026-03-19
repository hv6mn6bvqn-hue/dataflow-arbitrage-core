# core/exchange_api_executor.py
import json
import os

INPUT_FILE = "sources/allocated_signals.json"
OUTPUT_FILE = "sources/executed_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[API_EXECUTOR] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    executed = []
    for s in signals:
        # Симуляция успешного исполнения для live
        s["executed"] = True
        s["fill_price"] = s.get("price", 0)
        executed.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(executed, f)

    print(f"[API_EXECUTOR] executed: {len(executed)}")

if __name__ == "__main__":
    print("[API_EXECUTOR] start")
    run()