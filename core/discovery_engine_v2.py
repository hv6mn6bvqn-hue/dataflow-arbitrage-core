import os
import importlib
import json

CONNECTOR_PATH = "connectors/crypto"
OUTPUT_FILE = "sources/discovery_signals.json"


def load_all_connectors():

    connectors = []

    if not os.path.exists(CONNECTOR_PATH):
        print("[DISCOVERY] connector path not found:", CONNECTOR_PATH)
        return connectors

    files = [
        f for f in os.listdir(CONNECTOR_PATH)
        if f.endswith(".py") and not f.startswith("_")
    ]

    for f in files:

        module_name = f.replace(".py", "")
        module_path = f"connectors.crypto.{module_name}"

        try:

            module = importlib.import_module(module_path)
            connectors.append(module)

            print("[CONNECTOR] loaded", module_path)

        except Exception as e:

            print("[CONNECTOR] failed:", module_path, e)

    return connectors


def collect_prices():

    connectors = load_all_connectors()
    signals = []

    for c in connectors:

        try:

            data = c.fetch()

            if data:
                signals.extend(data)
                print(f"[{c.__name__.split('.')[-1].upper()}] price snapshots:", len(data))

        except Exception as e:

            print("[DISCOVERY] connector error:", c.__name__, e)

    return signals


def save_signals(signals):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print("[DISCOVERY] signals saved:", len(signals))


def run():

    signals = collect_prices()
    save_signals(signals)


def main():
    run()