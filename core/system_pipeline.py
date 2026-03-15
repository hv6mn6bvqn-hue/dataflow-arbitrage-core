import datetime

from core.market_feed import main as market_feed
from core.discovery_engine_v2 import main as discovery_engine
from core.spread_engine import main as spread_engine
from core.signal_filter_engine import main as signal_filter_engine
from core.arbitrage_matrix_engine import main as arbitrage_matrix_engine
from core.triangular_arbitrage_engine import main as triangular_arbitrage_engine
from core.funding_engine import main as funding_engine
from core.arbitrage_detector import main as arbitrage_detector
from core.fee_engine import main as fee_engine
from core.orderbook_engine import main as orderbook_engine
from core.liquidity_engine import main as liquidity_engine
from core.execution_simulator import main as execution_simulator
from core.execution_score_engine import main as execution_score_engine
from core.slippage_guard import main as slippage_guard
from core.latency_monitor import main as latency_monitor
from core.strategy_router import main as strategy_router
from core.funding_recovery_engine import main as funding_recovery_engine
from core.stat_arb_engine import main as stat_arb_engine
from core.capital_allocator import main as capital_allocator
from core.position_sizing_engine import main as position_sizing_engine
from core.drawdown_guard import main as drawdown_guard

from core.schema_normalizer import main as schema_normalizer
from core.opportunity_ranker import main as opportunity_ranker
from core.policy_v3 import main as policy_v3
from core.portfolio_intelligence_v2 import main as portfolio_intelligence_v2

from core.analyzer import main as analyzer
from core.signal_policy import main as signal_policy
from core.action_engine import main as action_engine
from core.exporter import main as exporter
from core.portfolio_engine import main as portfolio_engine
from core.metrics_engine import main as metrics_engine
from core.performance_engine import main as performance_engine


def run_step(name, func):

    print(f"\n[PIPELINE] running {name}")

    try:
        func()
    except Exception as e:
        print(f"[PIPELINE] ERROR in {name}: {e}")


def main():

    print("[PIPELINE] DataFlow system start")
    print(f"[PIPELINE] timestamp: {datetime.datetime.utcnow()}")

    pipeline = [
        ("core.market_feed", market_feed),
        ("core.discovery_engine_v2", discovery_engine),
        ("core.spread_engine", spread_engine),
        ("core.signal_filter_engine", signal_filter_engine),
        ("core.arbitrage_matrix_engine", arbitrage_matrix_engine),
        ("core.triangular_arbitrage_engine", triangular_arbitrage_engine),
        ("core.funding_engine", funding_engine),
        ("core.arbitrage_detector", arbitrage_detector),
        ("core.fee_engine", fee_engine),
        ("core.orderbook_engine", orderbook_engine),
        ("core.liquidity_engine", liquidity_engine),
        ("core.execution_simulator", execution_simulator),
        ("core.execution_score_engine", execution_score_engine),
        ("core.slippage_guard", slippage_guard),
        ("core.latency_monitor", latency_monitor),
        ("core.strategy_router", strategy_router),
        ("core.funding_recovery_engine", funding_recovery_engine),
        ("core.stat_arb_engine", stat_arb_engine),
        ("core.capital_allocator", capital_allocator),
        ("core.position_sizing_engine", position_sizing_engine),
        ("core.drawdown_guard", drawdown_guard),

        ("core.schema_normalizer", schema_normalizer),
        ("core.opportunity_ranker", opportunity_ranker),
        ("core.policy_v3", policy_v3),
        ("core.portfolio_intelligence_v2", portfolio_intelligence_v2),

        ("core.analyzer", analyzer),
        ("core.signal_policy", signal_policy),
        ("core.action_engine", action_engine),
        ("core.exporter", exporter),
        ("core.portfolio_engine", portfolio_engine),
        ("core.metrics_engine", metrics_engine),
        ("core.performance_engine", performance_engine),
    ]

    for name, func in pipeline:
        run_step(name, func)

    print("\n[PIPELINE] cycle complete")


if __name__ == "__main__":
    main()