import json
import os

INPUT_FILE = "sources/exchange_executed.json"
OUTPUT_FILE = "sources/live_routed.json"


def load_data():
    if not os.path.exists(INPUT_FILE):
        print("[LIVE_ROUTER] input missing")
        return []

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    except Exception as e:
        print(f"[LIVE_ROUTER] load error: {e}")
        return []


def route(signals):
    routed = []

    for signal in signals:
        fragments = signal.get("capital_fragments", 1)
        route_type = "PRIMARY"
        if fragments >= 3:
            route_type = "MULTI_FRAGMENT"

        # добавляем execution_status и executed_fragments для downstream
        signal["route"] = route_type
        signal["execution_status"] = signal.get("execution_status", "SUCCESS" if fragments > 0 else "FAILED")
        signal["executed_fragments"] = signal.get("executed_fragments", fragments)

        routed.append(signal)

    return routed


def save(data):
    os.makedirs("sources", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[LIVE_ROUTER] routed: {len(data)}")


def main():
    print("[LIVE_ROUTER] start")
    signals = load_data()
    result = route(signals)
    save(result)


if __name__ == "__main__":
    main()