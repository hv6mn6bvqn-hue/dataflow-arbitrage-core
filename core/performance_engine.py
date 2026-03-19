# core/performance_engine.py
import json
import os

INPUT_FILE = "sources/portfolio_state.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print("[PERFORMANCE] no portfolio data")
        return
    with open(INPUT_FILE) as f:
        portfolio = json.load(f)
    # Обновляем performance placeholder
    print(f"[PERFORMANCE] updated: state={portfolio.get('state','IDLE')} equity={portfolio.get('equity',0)}")

if __name__ == "__main__":
    print("[PERFORMANCE] start")
    run()