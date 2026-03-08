import importlib


CONNECTORS = [
    "connectors.kraken"
]


def load_connectors():

    modules = []

    for connector in CONNECTORS:

        try:

            module = importlib.import_module(connector)

            modules.append(module)

            print(f"[CONNECTOR] loaded {connector}")

        except Exception as e:

            print(f"[CONNECTOR] failed {connector}: {e}")

    return modules