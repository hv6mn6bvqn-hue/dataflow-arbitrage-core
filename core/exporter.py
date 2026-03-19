# core/exporter.py
import json
import os
import shutil

INPUT_FILE = "sources/action_executed.json"
OUTPUT_FILE = "sources/live_export.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print("[EXPORTER] input missing")
        signals = []
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    # Экспортируем для live routing
    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[EXPORTER] exported: {len(signals)} signals")

if __name__ == "__main__":
    print("[EXPORTER] start")
    run()