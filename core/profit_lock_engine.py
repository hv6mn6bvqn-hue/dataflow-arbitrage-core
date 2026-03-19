# core/profit_lock_engine.py
import json
import os

INPUT_FILE = "sources/portfolio_state.json"
OUTPUT_FILE = "sources/profit_locked.json"

def run():
    if not os.path.exists(INPUT_FILE):
        locked = False
        print("[PROFIT_LOCK] input missing")
    else:
        with open(INPUT_FILE) as f:
            portfolio = json.load(f)
        # Простая логика: lock, если есть активные сигналы
        locked = portfolio.get("signals", 0) > 0

    with open(OUTPUT_FILE, "w") as f:
        json.dump({"locked": locked}, f)

    print(f"[PROFIT_LOCK] locked: {locked}")

if __name__ == "__main__":
    print("[PROFIT_LOCK] start")
    run()