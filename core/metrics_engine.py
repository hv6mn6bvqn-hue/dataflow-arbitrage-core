# core/metrics_engine.py
import json
import os

INPUT_FILE = "sources/portfolio_state.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print("[METRICS] no portfolio data")
        return
    with open(INPUT_FILE) as f:
        portfolio = json.load(f)
    # Публикуем метрики
    print(f"[METRICS] published: equity={portfolio.get('equity',0)} signals={portfolio.get('signals',0)}")

if __name__ == "__main__":
    print("[METRICS] start")
    run()
