# core/spread_engine.py
import json

def run():
    try:
        with open("sources/discovery_signals.json") as f:
            signals = json.load(f)
    except Exception:
        signals = []

    opportunities = []
    for s in signals:
        # простая фильтрация и генерация пар
        if "price" in s:
            opportunities.append(s)

    with open("sources/spread_opportunities.json", "w") as f:
        json.dump(opportunities, f)

    print(f"[SPREAD] loaded: {len(signals)}")
    print(f"[SPREAD] opportunities: {len(opportunities)}")
    print(f"[SPREAD] saved: {len(opportunities)}")

if __name__ == "__main__":
    print("[SPREAD] engine start")
    run()