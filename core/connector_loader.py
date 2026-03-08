import importlib

# пути к нашим коннекторам
CONNECTORS = [
    "connectors.crypto.kraken",
    "connectors.crypto.binance",
    "connectors.crypto.coinbase"
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