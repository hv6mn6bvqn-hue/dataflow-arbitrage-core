import os
import importlib
import json
import time
from core.utils.logger import log

CONNECTOR_PATH = "core/connectors/crypto"
SIGNALS_FILE = "sources/signals.json"


def load_all_connectors():

    connectors = {}

    files = [
        f for f in os.listdir(CONNECTOR_PATH)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for file in files:

        name = file.replace(".py", "")

        try:

            module = importlib.import_module(f"core.connectors.crypto.{name}")
            connectors[name] = module

            log(f"[CONNECTOR] loaded {name}")

        except Exception as e:

            log(f"[CONNECTOR] failed {name}: {e}")

    return connectors


def collect_signals(connectors):

    all_signals = []

    for name, conn in connectors.items():

        try:

            snapshots = conn.fetch_prices()

            log(f"[{name.upper()}] snapshots: {len(snapshots)}")

            for s in snapshots:

                signal = {
                    "exchange": name,
                    "symbol": s["symbol"],
                    "price": s["price"],
                    "timestamp": int(time.time())
                }

                all_signals.append(signal)

        except Exception as e:

            log(f"[{name.upper()}] request error: {e}")

    return all_signals


def save_signals(signals):

    os.makedirs("sources", exist_ok=True)

    with open(SIGNALS_FILE, "w") as f:

        json.dump(signals, f, indent=2)


def run():

    log("[DISCOVERY] starting")

    connectors = load_all_connectors()

    log(f"[DISCOVERY] connectors: {len(connectors)}")

    signals = collect_signals(connectors)

    log(f"[DISCOVERY] signals collected: {len(signals)}")

    save_signals(signals)

    log("[DISCOVERY] signals.json updated")