import os
import importlib
from datetime import datetime


CONNECTOR_PATH = "connectors.crypto"


def load_connectors():

    connectors = []

    base_path = os.path.join("connectors", "crypto")

    for file in os.listdir(base_path):

        if not file.endswith(".py"):
            continue

        if file.startswith("_"):
            continue

        module_name = file.replace(".py", "")

        full_module = f"{CONNECTOR_PATH}.{module_name}"

        try:
            module = importlib.import_module(full_module)
            connectors.append(module)

            print(f"[CONNECTOR] loaded {full_module}")

        except Exception as e:

            print(f"[CONNECTOR] failed {full_module}:", e)

    return connectors


def run():

    print("[DISCOVERY V2] loading connectors")

    connectors = load_connectors()

    all_signals = []

    for connector in connectors:

        try:

            if hasattr(connector, "fetch"):
                signals = connector.fetch()
            elif hasattr(connector, "fetch_prices"):
                signals = connector.fetch_prices()
            else:
                continue

            print(f"[DISCOVERY] {connector.__name__} → {len(signals)} prices")

            all_signals.extend(signals)

        except Exception as e:

            print(f"[DISCOVERY] error {connector.__name__}:", e)

    print(f"[DISCOVERY V2] raw signals: {len(all_signals)}")

    return all_signals