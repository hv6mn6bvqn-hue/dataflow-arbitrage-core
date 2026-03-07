import json
from datetime import datetime

from core.discovery_engine_v2 import main as discovery
from core.arbitrage_detector import main as arbitrage

from core.signal_policy import main as signal_policy
from core.prioritizer import main as prioritizer
from core.analyzer import main as analyzer

from core.predictor import main as predictor
from core.predictor_velocity import main as predictor_velocity
from core.confirmation import main as confirmation

from core.action_resolver import main as action_resolver
from core.action_engine import main as action_engine
from core.execution_adapter import main as execution_adapter

from core.portfolio_engine import main as portfolio_engine
from core.metrics_engine import main as metrics_engine
from core.performance_engine import main as performance_engine

from core.replay_engine import main as replay_engine
from core.learner import main as learner
from core.state_manager import main as state_manager

from core.autopilot import main as autopilot
from core.audit_logger import main as audit_logger
from core.exporter import main as exporter


def run_step(name, fn):

    print(f"[PIPELINE] starting {name}")

    try:
        fn()
        print(f"[PIPELINE] finished {name}")

    except Exception as e:
        print(f"[PIPELINE] error in {name}: {e}")


def main():

    started = datetime.utcnow().isoformat()

    print("[SYSTEM] DataFlow autonomous pipeline starting")

    # DATA DISCOVERY
    run_step("discovery", discovery)

    # MARKET ANALYSIS
    run_step("analyzer", analyzer)
    run_step("predictor", predictor)
    run_step("predictor_velocity", predictor_velocity)
    run_step("confirmation", confirmation)

    # SIGNAL GENERATION
    run_step("arbitrage_detector", arbitrage)
    run_step("prioritizer", prioritizer)
    run_step("signal_policy", signal_policy)

    # EXECUTION
    run_step("action_resolver", action_resolver)
    run_step("action_engine", action_engine)
    run_step("execution_adapter", execution_adapter)

    # PORTFOLIO
    run_step("portfolio_engine", portfolio_engine)
    run_step("metrics_engine", metrics_engine)
    run_step("performance_engine", performance_engine)

    # LEARNING
    run_step("replay_engine", replay_engine)
    run_step("learner", learner)
    run_step("state_manager", state_manager)

    # AUTONOMY
    run_step("autopilot", autopilot)
    run_step("audit_logger", audit_logger)
    run_step("exporter", exporter)

    finished = datetime.utcnow().isoformat()

    summary = {
        "started": started,
        "finished": finished,
        "status": "completed"
    }

    with open("docs/system_run.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("[SYSTEM] pipeline finished")


if __name__ == "__main__":
    main()