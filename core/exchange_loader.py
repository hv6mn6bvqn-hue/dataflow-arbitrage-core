# core/exchange_loader.py
import os
import importlib.util

# путь к папке crypto внутри connectors
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONNECTORS_DIR = os.path.join(PROJECT_ROOT, "connectors", "crypto")

def load_connectors():
    connectors = {}
    if not os.path.exists(CONNECTORS_DIR):
        print(f"[EXCHANGE_LOADER] directory not found: {CONNECTORS_DIR}")
        return connectors

    for filename in os.listdir(CONNECTORS_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            filepath = os.path.join(CONNECTORS_DIR, filename)
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            connectors[module_name] = module.Connector()  # все коннекторы должны иметь класс Connector
    return connectors