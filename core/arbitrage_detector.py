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

    symbols = {}

    for s in signals:

        symbol = s.get("symbol")

        if not symbol:
            continue

        if symbol not in symbols:
            symbols[symbol] = []

        symbols[symbol].append(s)

    for symbol, entries in symbols.items():

        if len(entries) < 2:
            continue

        prices = []

        for e in entries:
            if "change_percent" in e:
                prices.append(e["change_percent"])

        if len(prices) < 2:
            continue

        spread = max(prices) - min(prices)

        if spread < 5:
            continue

        opportunity = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "symbol": symbol,
            "spread": round(spread, 2),
            "type": "arbitrage_opportunity",
            "confidence": min(spread / 20, 1.0)
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

    print("[ARBITRAGE] scanning signals")

    signals = load_feed()

    opportunities = detect_arbitrage(signals)

    print(f"[ARBITRAGE] opportunities found: {len(opportunities)}")

    save_opportunities(opportunities)


if __name__ == "__main__":
    main()