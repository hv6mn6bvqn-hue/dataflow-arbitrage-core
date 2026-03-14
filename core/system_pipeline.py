from datetime import datetime
import importlib


PIPELINE_MODULES = [
    "core.market_feed",
    "core.discovery_engine_v2",
    "core.spread_engine",
    "core.signal_filter_engine",
    "core.arbitrage_matrix_engine",
    "core.triangular_arbitrage_engine",
    "core.funding_engine",
    "core.arbitrage_detector",
    "core.fee_engine",
    "core.orderbook_engine",
    "core.liquidity_engine",
    "core.execution_simulator",
    "core.execution_score_engine",
    "core.slippage_guard",
    "core.latency_monitor",
    "core.strategy_router",
    "core.funding_recovery_engine",
    "core.stat_arb_engine",
    "core.capital_allocator",
    "core.position_sizing_engine",
    "core.drawdown_guard",
    "core.analyzer",
    "core.signal_policy",
    "core.action_engine",
    "core.exporter",
    "core.portfolio_engine",
    "core.metrics_engine",
    "core.performance_engine"
]


def run_module(module_name):

    print(f"\n[PIPELINE] running {module_name}")

    module = importlib.import_module(module_name)

    if hasattr(module, "main"):
        module.main()

    else:
        print(f"[PIPELINE] skipped {module_name} (no main)")


def main():

    print("[PIPELINE] DataFlow system start")
    print(f"[PIPELINE] timestamp: {datetime.utcnow()}")

    for module_name in PIPELINE_MODULES:
        run_module(module_name)

    print("\n[PIPELINE] cycle complete")


if __name__ == "__main__":
    main()