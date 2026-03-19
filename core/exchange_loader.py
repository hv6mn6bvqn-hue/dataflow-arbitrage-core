import os
import importlib.util

# Путь к папке с коннекторами
CONNECTORS_DIR = os.path.join(os.path.dirname(__file__), "../crypto")

def load_connectors():
    connectors = {}
    if not os.path.exists(CONNECTORS_DIR):
        print(f"[EXCHANGE_LOADER] crypto folder not found: {CONNECTORS_DIR}")
        return connectors

    for filename in os.listdir(CONNECTORS_DIR):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        module_name = filename[:-3]  # без .py
        file_path = os.path.join(CONNECTORS_DIR, filename)
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Проверка на класс Connector
            if hasattr(module, "Connector"):
                connectors[module_name] = module.Connector()
                print(f"[EXCHANGE_LOADER] loaded: {module_name}")
            else:
                print(f"[EXCHANGE_LOADER] skipped (no Connector class): {module_name}")
        except Exception as e:
            print(f"[EXCHANGE_LOADER] failed to load {module_name}: {e}")

    return connectors

# Тестовый запуск
if __name__ == "__main__":
    conns = load_connectors()
    print(f"Connectors loaded: {list(conns.keys())}")