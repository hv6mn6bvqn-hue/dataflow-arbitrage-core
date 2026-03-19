# core/live_capital_controller.py
import json
import os

INPUT_FILE = "sources/pnl_tracked.json"

CAPITAL_FILE = "sources/live_capital.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[LIVE_CAPITAL] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    equity = 10000  # стартовая капитализация
    for s in signals:
        equity += s.get("pnl", 0)

    with open(CAPITAL_FILE, "w") as f:
        json.dump({"equity": equity}, f)

    print(f"[LIVE_CAPITAL] equity: {equity}")

if __name__ == "__main__":
    print("[LIVE_CAPITAL] start")
    run()