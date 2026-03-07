import json
from datetime import datetime

import importlib


ENGINE_SEQUENCE = [
    "core.discovery_engine_v2",
    "core.arbitrage_detector",
    "core.signal_policy",
    "core.action_engine",
    "core.portfolio_engine",
    "core.metrics_engine",
    "core.performance_engine",
]


def run_module(module_name):

    print(f"[PIPELINE] running {module_name}")

    try:
        module = importlib.import_module(module_name)

        if hasattr(module, "main"):
            module.main()
        else:
            print(f"[PIPELINE] {module_name} has no main()")

    except Exception as e:
        print(f"[PIPELINE] ERROR {module_name}: {e}")


def main():

    print("[SYSTEM] DataFlow FULL pipeline starting")

    for engine in ENGINE_SEQUENCE:
        run_module(engine)

    state = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "completed"
    }

    with open("docs/system_run.json", "w") as f:
        json.dump(state, f, indent=2)

    print("[SYSTEM] Pipeline finished")


if __name__ == "__main__":
    main()