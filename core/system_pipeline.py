import os
import json
from datetime import datetime
from core import market_feed, discovery_engine_v2, spread_engine, arbitrage_matrix_engine, funding_engine
from core import arbitrage_detector, analyzer, signal_policy, action_engine, exporter, portfolio_engine, metrics_engine, performance_engine
from core.utils.logger import log

def run_pipeline():
    log("[PIPELINE] DataFlow system start")
    log(f"[PIPELINE] timestamp: {datetime.utcnow()}")

    # 1️⃣ Market feed
    prices = market_feed.fetch_prices()
    log(f"[MARKET_FEED] stored {len(prices)} prices")

    # 2️⃣ Discovery Engine
    connectors = discovery_engine_v2.load_all_connectors(auto=True)
    raw_signals = discovery_engine_v2.collect_signals(connectors)
    log(f"[DISCOVERY V2] raw signals: {len(raw_signals)}")

    # Сохраняем сигналы для всех downstream модулей
    os.makedirs("sources", exist_ok=True)
    with open("sources/signals.json", "w") as f:
        json.dump(raw_signals, f)
    log(f"[DISCOVERY] signals saved: {len(raw_signals)}")

    # 3️⃣ Spread Engine
    spread_opps = spread_engine.generate_opportunities(raw_signals)
    spread_engine.save_opportunities(spread_opps)
    log(f"[SPREAD] opportunities saved: {len(spread_opps)}")

    # 4️⃣ Arbitrage Matrix
    matrix_opps = arbitrage_matrix_engine.generate_matrix(raw_signals)
    arbitrage_matrix_engine.save_opportunities(matrix_opps)
    log(f"[MATRIX] opportunities saved: {len(matrix_opps)}")

    # 5️⃣ Funding Engine
    funding_data = funding_engine.collect_rates(connectors)
    if not funding_data:
        log("[FUNDING] no data, using fallback rates")
    else:
        log(f"[FUNDING] collected: {len(funding_data)}")

    # 6️⃣ Arbitrage Detector
    all_opps = spread_opps + matrix_opps
    detected = arbitrage_detector.scan(all_opps, funding_data)
    log(f"[ARBITRAGE] opportunities saved: {len(detected)}")

    # 7️⃣ Analyzer
    market_strength = analyzer.evaluate_market_strength(prices)
    log(f"[ANALYZER] market strength {market_strength}")

    # 8️⃣ Signal Policy
    decisions = signal_policy.evaluate(detected, market_strength)
    log(f"[POLICY] {len(decisions)} decisions saved")

    # 9️⃣ Action Engine
    action_engine.execute(decisions)
    log("[ENGINE] completed")

    # 🔟 Exporter
    exporter.publish(decisions)
    log(f"[EXPORTER] public feed updated: {len(decisions)} signals")

    # 1️⃣1️⃣ Portfolio Engine
    portfolio_engine.update(decisions)
    log("[PORTFOLIO] completed")

    # 1️⃣2️⃣ Metrics & Performance
    metrics_engine.publish()
    performance_engine.update()
    log("[PIPELINE] cycle complete\n")

if __name__ == "__main__":
    run_pipeline()