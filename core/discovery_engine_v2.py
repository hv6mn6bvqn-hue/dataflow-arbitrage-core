import asyncio
import importlib
import pkgutil
from pathlib import Path
import json
from datetime import datetime


FEED_PATH = Path("docs/feed/index.json")


async def run_connector(module):

    try:

        if hasattr(module, "fetch_prices"):

            result = module.fetch_prices()

            if asyncio.iscoroutine(result):
                result = await result

            print(f"[DISCOVERY] {module.__name__} → {len(result)} prices")

            return result

        return []

    except Exception as e:

        print(f"[DISCOVERY] connector error {module.__name__}: {e}")

        return []


def load_connectors():

    connectors = []

    package = importlib.import_module("connectors.crypto")

    for _, name, _ in pkgutil.iter_modules(package.__path__):

        module_name = f"connectors.crypto.{name}"

        try:

            module = importlib.import_module(module_name)

            connectors.append(module)

            print(f"[CONNECTOR] loaded {module_name}")

        except Exception as e:

            print(f"[CONNECTOR] failed {module_name}: {e}")

    return connectors


async def discover():

    connectors = load_connectors()

    tasks = []

    for c in connectors:
        tasks.append(run_connector(c))

    results = await asyncio.gather(*tasks)

    merged = []

    for r in results:
        merged.extend(r)

    return merged


def save_feed(signals):

    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "feed_version": "v2",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(signals),
        "signals": signals
    }

    FEED_PATH.write_text(json.dumps(data, indent=2))


def main():

    print("[DISCOVERY V2] loading connectors")

    signals = asyncio.run(discover())

    print(f"[DISCOVERY V2] signals added: {len(signals)}")

    save_feed(signals)


if __name__ == "__main__":
    main()