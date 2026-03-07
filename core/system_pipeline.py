import importlib
from datetime import datetime

ENGINE_SEQUENCE = [
    "core.market_feed",
    "core.discovery_engine_v2",
    "core.arbitrage_detector",
    "core.analyzer",
    "core.signal_policy",
    "core.action_engine",
    "core.portfolio_engine",
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
            print(f"[PIPELINE] skipped {module_name} (no main function)")

    except Exception as e:
        print(f"[PIPELINE] error in {module_name}: {e}")


def main():

    print("\n[PIPELINE] DataFlow system start")
    print("[PIPELINE] timestamp:", datetime.utcnow().isoformat(), "\n")

    for module_name in ENGINE_SEQUENCE:
        run_module(module_name)

    print("\n[PIPELINE] cycle complete\n")


if __name__ == "__main__":
    main()