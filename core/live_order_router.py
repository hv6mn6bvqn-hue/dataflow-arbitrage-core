from core.exchange_loader import load_connectors
import json
import os

INPUT_FILE = "sources/live_export.json"
OUTPUT_FILE = "sources/live_routed.json"

def run():
    connectors = load_connectors()

    if not os.path.exists(INPUT_FILE):
        print("[LIVE_ROUTER] input file missing")
        signals = []
    else:
        with open(INPUT_FILE, "r") as f:
            signals = json.load(f)

    routed_signals = []
    for s in signals:
        ex_name = s.get("exchange")
        connector = connectors.get(ex_name)
        if not connector:
            print(f"[LIVE_ROUTER] unknown exchange {ex_name}")
            s["routed"] = False
            s["error"] = "unknown exchange"
            routed_signals.append(s)
            continue

        try:
            # place_order должен быть определён в каждом Connector
            result = connector.place_order(
                symbol=s["symbol"],
                side=s["side"],
                quantity=s["quantity"],
                price=s.get("price")
            )
            s["routed"] = True
            s["order_id"] = result.get("id", None)
        except Exception as e:
            s["routed"] = False
            s["error"] = str(e)

        routed_signals.append(s)

    # Сохраняем результат
    with open(OUTPUT_FILE, "w") as f:
        json.dump(routed_signals, f)

    print(f"[LIVE_ROUTER] routed: {len(routed_signals)}")

if __name__ == "__main__":
    run()