import os
import importlib.util

CONNECTORS_DIR = os.path.join(os.path.dirname(__file__), "../connectors/crypto")

def load_connectors():
    connectors = {}
    if not os.path.exists(CONNECTORS_DIR):
        raise FileNotFoundError(f"Connectors folder not found: {CONNECTORS_DIR}")

    for filename in os.listdir(CONNECTORS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(CONNECTORS_DIR, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "Connector"):
                connectors[module_name] = module.Connector()
            else:
                print(f"[exchange_loader] {module_name} has no Connector class")
    return connectors