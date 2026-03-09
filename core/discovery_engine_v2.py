import os
import importlib
import json
from core.utils.logger import log

CONNECTOR_PATH = "core/connectors/crypto"

def load_all_connectors(auto=False):
    connectors = {}
    files = [f for f in os.listdir(CONNECTOR_PATH) if f.endswith(".py") and f != "__init__.py"]
    for file in files:
        name = file.replace(".py", "")
        try:
            module = importlib.import_module(f"core.connectors.crypto.{name}")
            connectors[name] = module
            log(f"[CONNECTOR] loaded connectors.crypto.{name}")
        except Exception as e:
            log(f"[CONNECTOR] failed to load {name}: {e}")
    return connectors

def collect_signals(connectors):
    all_signals = []
    for name, conn in connectors.items():
        try:
            snapshots = conn.fetch_prices()
            log(f"[{name.upper()}] price snapshots: {len(snapshots)}")
            for s in snapshots:
                s["source"] = name
            all_signals.extend(snapshots)
        except Exception as e:
            log(f"[{name.upper()}] request error: {e}")
    return all_signals