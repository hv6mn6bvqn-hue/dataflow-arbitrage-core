import os
import importlib
import json
import time

from core.utils.symbol_normalizer import normalize_symbol


CONNECTOR_PATH = "connectors/crypto"
SIGNALS_FILE = "sources/signals.json"


def load_all_connectors():

    connectors = {}

    if not os.path.exists(CONNECTOR_PATH):
        print("[DISCOVERY] connector path missing:", CONNECTOR_PATH)
        return connectors

    files = [
        f for f in os.listdir(CONNECTOR_PATH)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for file in files:

        name = file.replace(".py", "")

        try:

            module = importlib.import_module(f"connectors.crypto.{name}")

            if hasattr(module, "fetch_prices"):
                connectors[name] = module
                print(f"[CONNECTOR] loaded connectors.crypto.{name}")
            else:
                print(f"[CONNECTOR] skipped {name} (no fetch_prices)")

        except Exception as e:
            print(f"[CONNECTOR] failed {name}:", e)

    return connectors


def normalize_snapshot(snapshot):

    try:

        symbol = snapshot.get("symbol")

        if not symbol:
            return None

        normalized = normalize_symbol(symbol)

        return {
            "symbol": normalized,
            "price": float(snapshot["price"])
        }

    except Exception:
        return None


def collect_signals(connectors):

    all_signals = []

    for name, conn in connectors.items():

        try:

            snapshots = conn.fetch_prices()

            if not snapshots:
                print(f"[{name.upper()}] no data")
                continue

            print(f"[{name.upper()}] price snapshots:", len(snapshots))

            for s in snapshots:

                normalized = normalize_snapshot(s)

                if not normalized:
                    continue

                signal = {
                    "exchange": name,
                    "symbol": normalized["symbol"],
                    "price": normalized["price"],
                    "timestamp": int(time.time())
                }

                all_signals.append(signal)

        except Exception as e:
            print(f"[{name.upper()}] request error:", e)

    return all_signals


def save_signals(signals):

    os.makedirs("sources", exist_ok=True)

    with open(SIGNALS_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[DISCOVERY] signals saved:", len(signals))


def run():

    print("[DISCOVERY] starting")

    connectors = load_all_connectors()

    print("[DISCOVERY] connectors loaded:", len(connectors))

    signals = collect_signals(connectors)

    print("[DISCOVERY] signals collected:", len(signals))

    save_signals(signals)