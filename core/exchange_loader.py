# core/exchange_loader.py
import os
import importlib.util

CONNECTORS_DIR = "crypto"
CONNECTORS = {}

def load_connectors():
    global CONNECTORS
    CONNECTORS = {}

    for file in os.listdir(CONNECTORS_DIR):
        if file.endswith(".py") and file != "__init__.py":
            name = file[:-3]  # убираем .py
            path = os.path.join(CONNECTORS_DIR, file)

            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            CONNECTORS[name] = module

    print(f"[EXCHANGE_LOADER] loaded exchanges: {list(CONNECTORS.keys())}")
    return CONNECTORS

if __name__ == "__main__":
    load_connectors()