import subprocess
from datetime import datetime

PIPELINE = [
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
    "core.schema_normalizer",
    "core.opportunity_ranker",
    "core.policy_v3",
    "core.portfolio_intelligence_v2",
    "core.exchange_trust_engine",
    "core.signal_repeatability_engine",
    "core.venue_quality_engine",
    "core.signal_decay_engine",
    "core.execution_memory",
    "core.fill_probability_engine",
    "core.partial_fill_guard",
    "core.failed_execution_recovery",
    "core.capital_fragmentation_engine",
    "core.exchange_api_executor",
    "core.live_order_router",
    "core.order_confirmation_engine",
    "core.real_pnl_tracker",
    "core.live_capital_controller",
    "core.adaptive_capital_bridge",
    "core.pnl_consensus_engine",
    "core.execution_confidence_engine",
    "core.execution_policy_bridge",
    "core.real_pnl_reconciliation",
    "core.exchange_sandbox_guard",
    "core.venue_rotation_engine",
    "core.anomaly_guard_engine",
    "core.live_session_controller",
    "core.arbitrage_heatmap_engine",
    "core.analyzer",
    "core.signal_policy",
    "core.action_engine",
    "core.exporter",
    "core.portfolio_engine",
    "core.profit_lock_engine",
    "core.metrics_engine",
    "core.performance_engine"
]


def run_module(module):
    print(f"\n[PIPELINE] running {module}")
    subprocess.run(["python", "-m", module], check=True)


def main():
    print("[PIPELINE] DataFlow system start")
    print(f"[PIPELINE] timestamp: {datetime.utcnow()}")

    for module in PIPELINE:
        run_module(module)

    print("\n[PIPELINE] cycle complete")


if __name__ == "__main__":
    main()