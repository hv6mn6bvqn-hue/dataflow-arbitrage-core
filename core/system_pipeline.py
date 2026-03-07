import json
from datetime import datetime

from core.discovery_engine_v2 import main as discovery_main
from core.analyzer import analyze_market
from core.predictor import predict_market
from core.predictor_velocity import analyze_velocity
from core.confirmation import confirm_signals

from core.arbitrage_detector import main as arbitrage_main
from core.prioritizer import prioritize_signals
from core.signal_policy import evaluate_signal

from core.action_resolver import resolve_action
from core.action_engine import main as action_main
from core.execution_adapter import main as execution_main

from core.portfolio_engine import main as portfolio_main
from core.metrics_engine import main as metrics_main
from core.performance_engine import main as performance_main

from core.learner import learn_from_history
from core.state_manager import save_state


def run_stage(name, fn):

    print(f"[PIPELINE] {name}")

    try:
        return fn()

    except Exception as e:
        print(f"[PIPELINE] ERROR {name}: {e}")
        return None


def main():

    print("[SYSTEM] DataFlow FULL autonomous pipeline starting")

    # 1. Discovery
    run_stage("discovery", discovery_main)

    # 2. Market intelligence
    market_analysis = run_stage("analyzer", analyze_market)
    velocity = run_stage("velocity", analyze_velocity)

    # 3. Prediction
    predictions = run_stage("predictor", predict_market)

    # 4. Signal layer
    signals = run_stage("confirmation", confirm_signals)

    # 5. Arbitrage detection
    opportunities = run_stage("arbitrage", arbitrage_main)

    # 6. Policy + prioritization
    if signals:
        for s in signals:
            decision = evaluate_signal(s)

            s["decision"] = decision

        run_stage("prioritize", lambda: prioritize_signals(signals))

    # 7. Execution
    run_stage("action_engine", action_main)
    run_stage("execution", execution_main)

    # 8. Portfolio + metrics
    run_stage("portfolio", portfolio_main)
    run_stage("metrics", metrics_main)
    run_stage("performance", performance_main)

    # 9. Learning + memory
    run_stage("learning", learn_from_history)

    run_stage("state", save_state)

    # Save system state
    state = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "completed"
    }

    with open("docs/system_run.json", "w") as f:
        json.dump(state, f, indent=2)

    print("[SYSTEM] Pipeline completed")


if __name__ == "__main__":
    main()