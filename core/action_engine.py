# core/action_engine.py
import json
import os

INPUT_FILE = "sources/policy_decision.json"
OUTPUT_FILE = "sources/action_executed.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[ENGINE] no signals to process")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Имитируем выполнение
        s["executed"] = s["action"] == "EXECUTE"

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[ENGINE] processed: {len(signals)}")

if __name__ == "__main__":
    print("[ENGINE] starting action engine")
    run()