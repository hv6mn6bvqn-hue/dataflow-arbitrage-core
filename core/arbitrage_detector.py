import json
from pathlib import Path
from datetime import datetime

FEED_PATH = Path("docs/feed/index.json")
EXPORT_DIR = Path("exports")

EXPORT_DIR.mkdir(exist_ok=True)

MIN_SPREAD_PERCENT = 0.5


def load_feed():

    if not FEED_PATH.exists():
        return []

    data = json.loads(FEED_PATH.read_text())

    return data.get("signals", [])


def group_by_symbol(signals):

    markets = {}

    for s in signals:

        symbol = s.get("symbol")

        if not symbol:
            continue

        markets.setdefault(symbol, []).append(s)

    return markets


def detect_arbitrage(markets):

    opportunities = []

    for symbol, entries in markets.items():

        if len(entries) < 2:
            continue

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):

                a = entries[i]
                b = entries[j]

                source_a = a.get("source")
                source_b = b.get("source")

                if source_a == source_b:
                    continue

                price_a = a.get("price") or a.get("ask") or a.get("bid")
                price_b = b.get("price") or b.get("ask") or b.get("bid")

                if not price_a or not price_b:
                    continue

                price_a = float(price_a)
                price_b = float(price_b)

                low_price = min(price_a, price_b)
                high_price = max(price_a, price_b)

                spread = high_price - low_price
                spread_percent = (spread / low_price) * 100

                if spread_percent < MIN_SPREAD_PERCENT:
                    continue

                buy_exchange = source_a if price_a < price_b else source_b
                sell_exchange = source_b if price_a < price_b else source_a

                opportunities.append({
                    "type": "signal",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "symbol": symbol,
                    "buy_from": buy_exchange,
                    "sell_to": sell_exchange,
                    "spread_percent": spread_percent,
                    "buy_price": low_price,
                    "sell_price": high_price
                })

    return opportunities


def export(opportunities):

    for i, signal in enumerate(opportunities):

        file = EXPORT_DIR / f"arb_signal_{i}.json"

        file.write_text(json.dumps(signal, indent=2))


def main():

    print("[ARBITRAGE] scanning markets")

    signals = load_feed()

    markets = group_by_symbol(signals)

    opportunities = detect_arbitrage(markets)

    print(f"[ARBITRAGE] opportunities found: {len(opportunities)}")

    if opportunities:
        export(opportunities)


if __name__ == "__main__":
    main()