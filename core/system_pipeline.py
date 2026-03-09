import json
import os
from datetime import datetime

from core import market_feed
from core import discovery_engine_v2
from core import spread_engine
from core import arbitrage_matrix_engine
from core import funding_engine
from core import arbitrage_detector
from core import analyzer
from core import signal_policy
from core import action_engine
from core import exporter
from core import portfolio_engine
from core import metrics_engine
from core import performance_engine


def run_pipeline():

    print("[PIPELINE] DataFlow system start")
    print("[PIPELINE] timestamp:", datetime.utcnow(), "\n")

    # MARKET FEED
    print("[PIPELINE] running core.market_feed")
    prices = market_feed.fetch_prices()

    # DISCOVERY
    print("\n[PIPELINE] running core.discovery_engine_v2")

    connectors = discovery_engine_v2.load_all_connectors()
    signals = discovery_engine_v2.collect_signals(connectors)

    os.makedirs("sources", exist_ok=True)

    with open("sources/signals.json", "w") as f:
        json.dump(signals, f)

    print("[DISCOVERY] signals saved:", len(signals))

    # SPREAD ENGINE
    print("\n[PIPELINE] running core.spread_engine")
    spread_engine.main()

    # MATRIX ENGINE
    print("\n[PIPELINE] running core.arbitrage_matrix_engine")
    arbitrage_matrix_engine.main()

    # FUNDING ENGINE
    print("\n[PIPELINE] running core.funding_engine")
    funding_engine.main()

    # ARBITRAGE DETECTOR
    print("\n[PIPELINE] running core.arbitrage_detector")
    arbitrage_detector.main()

    # ANALYZER
    print("\n[PIPELINE] running core.analyzer")
    analyzer.main()

    # SIGNAL POLICY
    print("\n[PIPELINE] running core.signal_policy")
    signal_policy.main()

    # ACTION ENGINE
    print("\n[PIPELINE] running core.action_engine")
    action_engine.main()

    # EXPORTER
    print("\n[PIPELINE] running core.exporter")
    exporter.main()

    # PORTFOLIO
    print("\n[PIPELINE] running core.portfolio_engine")
    portfolio_engine.main()

    # METRICS
    print("\n[PIPELINE] running core.metrics_engine")
    metrics_engine.main()

    # PERFORMANCE
    print("\n[PIPELINE] running core.performance_engine")
    performance_engine.main()

    print("\n[PIPELINE] cycle complete")


if __name__ == "__main__":
    run_pipeline()