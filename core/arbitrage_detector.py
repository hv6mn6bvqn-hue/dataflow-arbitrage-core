from pathlib import Path
import json
from datetime import datetime

FEED_PATH = Path("docs/feed/index.json")
ARBITRAGE_PATH = Path("docs/arbitrage/index.json")


def load_feed():
    if not FEED_PATH.exists():
        return []

    data = json.loads(FEED_PATH.read_text())
    return data.get("signals", [])


def detect_arbitrage(signals):

    opportunities = []

    # структура: symbol -> source -> price
    markets = {}

    for s in signals:

        symbol = s.get("symbol")
        source = s.get("source")

        if not symbol or not source:
            continue

        price = s.get("price")

        # если price нет — пропускаем
        if price is None:
            continue

        try:
            price = float(price)
        except:
            continue

        markets.setdefault(symbol, {})
        markets[symbol][source] = price

    for symbol, sources in markets.items():

        if len(sources) < 2:
            continue

        prices = list(sources.values())

        low = min(prices)
        high = max(prices)

        spread = high - low

        if spread <= 0:
            continue

        percent = (spread / low) * 100

        # фильтр минимального спреда
        if percent < 0.5:
            continue

        opportunity = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "symbol": symbol,
            "buy_price": round(low, 4),
            "sell_price": round(high, 4),
            "spread": round(spread, 4),
            "spread_percent": round(percent, 3),
            "type": "cross_exchange_arbitrage",
            "confidence": min(percent / 5, 1.0)
        }

        opportunities.append(opportunity)

    return opportunities


def save_opportunities(data):

    ARBITRAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(data),
        "opportunities": data
    }

    ARBITRAGE_PATH.write_text(json.dumps(result, indent=2))


def main():

    print("[ARBITRAGE] scanning markets")

    signals = load_feed()

    opportunities = detect_arbitrage(signals)

    print(f"[ARBITRAGE] opportunities found: {len(opportunities)}")

    save_opportunities(opportunities)


if __name__ == "__main__":
    main()