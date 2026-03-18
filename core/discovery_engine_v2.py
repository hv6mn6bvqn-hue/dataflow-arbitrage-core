import os
import importlib
import json
import time

CONNECTOR_PATH = "connectors/crypto"
OUTPUT_FILE = "sources/signals.json"


def load_all_connectors():

    connectors = {}

    if not os.path.exists(CONNECTOR_PATH):
        print("[DISCOVERY] connector path missing:", CONNECTOR_PATH)
        return connectors

    files = [
        f for f in os.listdir(CONNECTOR_PATH)
        if f.endswith(".py") and f != "__init__.py"
    ]

    print("[DISCOVERY] connector files:", len(files))

    for file in files:

        name = file.replace(".py", "")

        try:
            module = importlib.import_module(f"connectors.crypto.{name}")
            connectors[name] = module
            print(f"[CONNECTOR] loaded: {name}")

        except Exception as e:
            print(f"[CONNECTOR] failed {name}: {e}")

    return connectors


def collect_signals(connectors):

    all_signals = []

    for name, conn in connectors.items():

        try:
            snapshots = conn.fetch_prices()

            print(f"[{name.upper()}] snapshots:", len(snapshots))

            for s in snapshots:

                if "symbol" not in s or "price" not in s:
                    continue

                all_signals.append({
                    "exchange": name,
                    "symbol": s["symbol"],
                    "price": s["price"],
                    "timestamp": int(time.time())
                })

        except Exception as e:
            print(f"[{name.upper()}] request error: {e}")

    return all_signals


def save_signals(signals):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[DISCOVERY] signals saved:", len(signals))


def fallback_if_empty(signals):

    if signals:
        return signals

    print("[DISCOVERY] fallback activated")

    return [
        {
            "exchange": "binance",
            "symbol": "BTCUSDT",
            "price": 65000,
            "timestamp": int(time.time())
        },
        {
            "exchange": "okx",
            "symbol": "BTCUSDT",
            "price": 65200,
            "timestamp": int(time.time())
        }
    ]


def run():

    print("[DISCOVERY] engine start")

    connectors = load_all_connectors()

    signals = collect_signals(connectors)

    signals = fallback_if_empty(signals)

    save_signals(signals)


def main():
    run()


if __name__ == "__main__":
    main()