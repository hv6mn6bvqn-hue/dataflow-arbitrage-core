import importlib
from datetime import datetime


PIPELINE_MODULES = [

    # market data
    "core.market_feed",

    # discovery
    "core.discovery_engine_v2",

    # arbitrage engines
    "core.spread_engine",
    "core.arbitrage_matrix_engine",
    "core.funding_engine",

    # decision layer
    "core.arbitrage_detector",
    "core.analyzer",
    "core.signal_policy",

    # execution
    "core.action_engine",

    # public layer
    "core.exporter",

    # portfolio
    "core.portfolio_engine",

    # analytics
    "core.metrics_engine",
    "core.performance_engine"
]


def run_module(module_name):

    try:

        module = importlib.import_module(module_name)

        if hasattr(module, "main"):
            print(f"[PIPELINE] running {module_name}")
            module.main()
        else:
            print(f"[PIPELINE] skipped {module_name} (no main())")

    except Exception as e:

        print(f"[PIPELINE] error in {module_name}: {e}")


def main():

    print("\n[PIPELINE] DataFlow system start")
    print("[PIPELINE] timestamp:", datetime.utcnow(), "\n")

    for module in PIPELINE_MODULES:
        run_module(module)

    print("\n[PIPELINE] cycle complete\n")


if __name__ == "__main__":
    main()