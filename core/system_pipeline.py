import datetime

from core import market_feed
from core import discovery_engine_v2
from core import spread_engine
from core import signal_filter_engine
from core import arbitrage_matrix_engine
from core import triangular_arbitrage_engine
from core import funding_engine
from core import arbitrage_detector
from core import fee_engine
from core import liquidity_engine
from core import analyzer
from core import signal_policy
from core import action_engine
from core import exporter
from core import portfolio_engine
from core import metrics_engine
from core import performance_engine


def run_pipeline():

    print("[PIPELINE] DataFlow system start")
    print("[PIPELINE] timestamp:", datetime.datetime.utcnow())

    print("\n[PIPELINE] running core.market_feed")
    market_feed.main()

    print("\n[PIPELINE] running core.discovery_engine_v2")
    discovery_engine_v2.main()

    print("\n[PIPELINE] running core.spread_engine")
    spread_engine.main()

    print("\n[PIPELINE] running core.signal_filter_engine")
    signal_filter_engine.main()

    print("\n[PIPELINE] running core.arbitrage_matrix_engine")
    arbitrage_matrix_engine.main()

    print("\n[PIPELINE] running core.triangular_arbitrage_engine")
    triangular_arbitrage_engine.main()

    print("\n[PIPELINE] running core.funding_engine")
    funding_engine.main()

    print("\n[PIPELINE] running core.arbitrage_detector")
    arbitrage_detector.main()

    print("\n[PIPELINE] running core.fee_engine")
    fee_engine.main()

    print("\n[PIPELINE] running core.liquidity_engine")
    liquidity_engine.main()

    print("\n[PIPELINE] running core.analyzer")
    analyzer.main()

    print("\n[PIPELINE] running core.signal_policy")
    signal_policy.main()

    print("\n[PIPELINE] running core.action_engine")
    action_engine.main()

    print("\n[PIPELINE] running core.exporter")
    exporter.main()

    print("\n[PIPELINE] running core.portfolio_engine")
    portfolio_engine.main()

    print("\n[PIPELINE] running core.metrics_engine")
    metrics_engine.main()

    print("\n[PIPELINE] running core.performance_engine")
    performance_engine.main()

    print("\n[PIPELINE] cycle complete")


if __name__ == "__main__":
    run_pipeline()