from core.connectors import ccxt_connector
import json

def run_discovery():
    connector = ccxt_connector.Connector()
    market_data = connector.fetch_tickers()

    signals = []
    for exchange_name, tickers in market_data.items():
        for symbol, ticker in tickers.items():
            signal = {
                "exchange": exchange_name,
                "symbol": symbol,
                "bid": ticker.get("bid"),
                "ask": ticker.get("ask"),
                "timestamp": ticker.get("timestamp"),
            }
            signals.append(signal)

    with open("sources/discovery_signals.json", "w") as f:
        json.dump(signals, f, indent=2)
    print(f"[DISCOVERY] signals saved: {len(signals)}")