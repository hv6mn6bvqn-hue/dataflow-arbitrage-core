import importlib
from datetime import datetime

MODULES = [

    "core.market_feed",

    "core.discovery_engine_v2",

    "core.spread_engine",

    "core.arbitrage_matrix_engine",

    "core.arbitrage_detector",

    "core.analyzer",

    "core.signal_policy",

    "core.action_engine",

    "core.exporter",

    "core.portfolio_engine",

    "core.metrics_engine",

    "core.performance_engine",
]


def run_module(module_path):

    try:

        module = importlib.import_module(module_path)

        if hasattr(module, "main"):

            print(f"[PIPELINE] running {module_path}")

            module.main()

        else:

            print(f"[PIPELINE] skipped {module_path} (no main())")

    except Exception as e:

        print(f"[PIPELINE] error in {module_path}: {e}")


def main():

    print("\n[PIPELINE] DataFlow system start")

    print(f"[PIPELINE] timestamp: {datetime.utcnow().isoformat()} \n")

    for module_path in MODULES:

        run_module(module_path)

    print("\n[PIPELINE] cycle complete\n")


if __name__ == "__main__":

    main()