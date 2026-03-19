import json

def run_spread_engine():
    with open("sources/discovery_signals.json") as f:
        signals = json.load(f)

    spreads = []
    exchange_pairs = [("binance", "kraken"), ("binance", "coinbase"), ("kraken", "coinbase")]

    for pair in exchange_pairs:
        ex1, ex2 = pair
        for s1 in [sig for sig in signals if sig["exchange"] == ex1]:
            for s2 in [sig for sig in signals if sig["exchange"] == ex2 and sig["symbol"] == s1["symbol"]]:
                if s1["ask"] and s2["bid"]:
                    spread = s2["bid"] - s1["ask"]
                    if spread > 0:
                        spreads.append({
                            "symbol": s1["symbol"],
                            "buy_exchange": ex1,
                            "sell_exchange": ex2,
                            "spread": spread,
                        })
    with open("sources/spread_opportunities.json", "w") as f:
        json.dump(spreads, f, indent=2)
    print(f"[SPREAD] opportunities found: {len(spreads)}")