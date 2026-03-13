from datetime import datetime

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
from core.position_sizing_engine import main as position_sizing_engine
from core.drawdown_guard import main as drawdown_guard
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
        print(f"[PIPELINE] {name} failed: {e}")


def main():

    print("[PIPELINE] DataFlow system start")
    print("[PIPELINE] timestamp:", datetime.utcnow())

    run_step("core.market_feed", market_feed)
    run_step("core.discovery_engine_v2", discovery_engine)
    run_step("core.spread_engine", spread_engine)
    run_step("core.signal_filter_engine", signal_filter_engine)
    run_step("core.arbitrage_matrix_engine", arbitrage_matrix_engine)
    run_step("core.triangular_arbitrage_engine", triangular_arbitrage_engine)
    run_step("core.funding_engine", funding_engine)
    run_step("core.arbitrage_detector", arbitrage_detector)
    run_step("core.fee_engine", fee_engine)
    run_step("core.orderbook_engine", orderbook_engine)
    run_step("core.liquidity_engine", liquidity_engine)
    run_step("core.execution_simulator", execution_simulator)
    run_step("core.position_sizing_engine", position_sizing_engine)
    run_step("core.drawdown_guard", drawdown_guard)
    run_step("core.analyzer", analyzer)
    run_step("core.signal_policy", signal_policy)
    run_step("core.action_engine", action_engine)
    run_step("core.exporter", exporter)
    run_step("core.portfolio_engine", portfolio_engine)
    run_step("core.metrics_engine", metrics_engine)
    run_step("core.performance_engine", performance_engine)

    print("\n[PIPELINE] cycle complete")


if __name__ == "__main__":
    main()