import importlib
import pkgutil


def load_connectors():

    connectors = []

    packages = [
        "connectors.crypto",
        "connectors.ecommerce",
        "connectors.betting"
    ]

    for package in packages:

        try:
            module = importlib.import_module(package)
        except Exception:
            continue

        for _, name, _ in pkgutil.iter_modules(module.__path__):

            module_name = f"{package}.{name}"

            try:
                mod = importlib.import_module(module_name)

                if hasattr(mod, "fetch_signals"):
                    connectors.append(mod)
                    print(f"[CONNECTOR] loaded {module_name}")

            except Exception as e:
                print(f"[CONNECTOR] failed {module_name}: {e}")

    return connectors