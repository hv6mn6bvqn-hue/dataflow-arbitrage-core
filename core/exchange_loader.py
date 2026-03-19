# core/exchange_loader.py
import importlib
import os
import sys

CONNECTORS_DIR = os.path.join(os.path.dirname(__file__), "../crypto")

def load_connectors():
    """
    Автоматически загружает все коннекторы из папки crypto.
    Возвращает словарь: { "binance": connector_instance, ... }
    """
    connectors = {}
    sys.path.insert(0, CONNECTORS_DIR)

    for filename in os.listdir(CONNECTORS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "Connector"):
                    connectors[module_name] = module.Connector()
                    print(f"[EXCHANGE_LOADER] loaded: {module_name}")
            except Exception as e:
                print(f"[EXCHANGE_LOADER] failed to load {module_name}: {e}")

    sys.path.pop(0)
    return connectors