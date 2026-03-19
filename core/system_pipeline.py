# core/system_pipeline.py
import json
import os
from datetime import datetime

# 1️⃣ CCXT Connector
import ccxt
import time

class CCXTConnector:
    def __init__(self):
        self.exchanges = {
            "binance": ccxt.binance(),
            "kraken": ccxt.kraken(),
            "coinbase": ccxt.coinbasepro(),
            "kucoin": ccxt.kucoin(),
        }

    def fetch_tickers(self):
        all_tickers = {}
        for name, ex in self.exchanges.items():
            try:
                data = ex.fetch_tickers()
            except Exception as e:
                print(f"[{name}] ticker error: {e}")
                data = {}
            all_tickers[name] = data
            time.sleep(0.2)
        return all_tickers

    def place_order(self, exchange, symbol, side, quantity, price=None):
        # заглушка
        print(f"[{exchange}] placing {side} {quantity} {symbol} at {price}")
        return {"id": f"{exchange}_{symbol}_{side}"}

    def check_order(self, order_id):
        # считаем, что ордер всегда filled
        return {"filled": True}

# 2️⃣ Discovery
def discovery_engine():
    conn = CCXTConnector()
    tickers = conn.fetch_tickers()
    signals = []
    for ex, data in tickers.items():
        for sym, info in data.items():
            bid = info.get("bid")
            ask = info.get("ask")
            ts = info.get("timestamp")
            if bid and ask:
                signals.append({
                    "exchange": ex,
                    "symbol": sym,
                    "bid": bid,
                    "ask": ask,
                    "timestamp": ts,
                })
    os.makedirs("sources", exist_ok=True)
    with open("sources/discovery_signals.json", "w") as f:
        json.dump(signals, f, indent=2)
    print(f"[DISCOVERY] signals saved: {len(signals)}")

# 3️⃣ Spread Engine
def spread_engine():
    path = "sources/discovery_signals.json"
    if not os.path.exists(path):
        print("[SPREAD] no discovery signals")
        return
    with open(path) as f:
        sigs = json.load(f)

    spreads = []
    exs = ["binance", "kraken", "coinbase", "kucoin"]
    for i in range(len(exs)):
        for j in range(i+1, len(exs)):
            a = exs[i]
            b = exs[j]
            for s1 in [x for x in sigs if x["exchange"] == a]:
                for s2 in [x for x in sigs if x["exchange"] == b and x["symbol"] == s1["symbol"]]:
                    spread = s2["bid"] - s1["ask"]
                    if spread > 0:
                        spreads.append({
                            "symbol": s1["symbol"],
                            "buy_exchange": a,
                            "sell_exchange": b,
                            "spread": round(spread,6)
                        })

    with open("sources/spread_opportunities.json","w") as f:
        json.dump(spreads, f, indent=2)
    print(f"[SPREAD] opportunities: {len(spreads)}")

# 4️⃣ Live Order Router
def live_order_router():
    inp = "sources/spread_opportunities.json"
    out = "sources/live_export.json"
    if not os.path.exists(inp):
        print("[LIVE_ROUTER] no spread opportunities")
        return
    with open(inp) as f:
        ops = json.load(f)

    conn = CCXTConnector()
    routed=[]
    for o in ops:
        res = conn.place_order(o["buy_exchange"], o["symbol"], "BUY", 0.001)
        o["order_id"] = res["id"]
        routed.append(o)
    with open(out,"w") as f:
        json.dump(routed, f, indent=2)
    print(f"[LIVE_ROUTER] routed: {len(routed)}")

# 5️⃣ Confirmation
def order_confirmation():
    inp="sources/live_export.json"
    out="sources/live_confirmed.json"
    if not os.path.exists(inp):
        print("[CONFIRMATION] no live export")
        return
    with open(inp) as f:
        data = json.load(f)
    conn = CCXTConnector()
    confirmed=[]
    for s in data:
        status = conn.check_order(s["order_id"])
        s["confirmed"] = status.get("filled", False)
        confirmed.append(s)
    with open(out,"w") as f:
        json.dump(confirmed,f,indent=2)
    print(f"[CONFIRMATION] confirmed: {len(confirmed)}")

# 6️⃣ Real PnL & Capital
def real_pnl():
    inp="sources/live_confirmed.json"
    if not os.path.exists(inp):
        print("[REAL_PNL] missing")
        return
    with open(inp) as f:
        data=json.load(f)
    pnl=[] 
    for s in data:
        pnl.append({"symbol":s["symbol"], "pnl":round(s["spread"]*1,6)})
    print(f"[REAL_PNL] tracked: {len(pnl)}")

# 7️⃣ Runner
def main():
    print("[PIPELINE] start", datetime.utcnow())
    discovery_engine()
    spread_engine()
    live_order_router()
    order_confirmation()
    real_pnl()
    print("[PIPELINE] complete", datetime.utcnow())

if __name__ == "__main__":
    main()