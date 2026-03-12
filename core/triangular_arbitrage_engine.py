import json
import os
from collections import defaultdict

INPUT_FILE = "sources/signals.json"
OUTPUT_FILE = "sources/triangular_opportunities.json"

THRESHOLD = 0.002


def load_prices():

    if not os.path.exists(INPUT_FILE):
        print("[TRI] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[TRI] signals loaded:", len(data))
    return data


def build_graph(signals):

    graph = defaultdict(dict)

    for s in signals:

        symbol = s["symbol"]
        price = s["price"]

        if "-" in symbol:
            base, quote = symbol.split("-")
        elif "/" in symbol:
            base, quote = symbol.split("/")
        else:
            continue

        graph[base][quote] = price

        if price > 0:
            graph[quote][base] = 1 / price

    return graph


def find_triangles(graph):

    opportunities = []

    assets = list(graph.keys())

    for a in assets:
        for b in graph[a]:

            if b not in graph:
                continue

            for c in graph[b]:

                if c not in graph:
                    continue

                if a not in graph[c]:
                    continue

                r1 = graph[a][b]
                r2 = graph[b][c]
                r3 = graph[c][a]

                result = r1 * r2 * r3

                profit = result - 1

                if profit > THRESHOLD:

                    opportunities.append({
                        "path": [a, b, c, a],
                        "profit": profit
                    })

    return opportunities


def save_opportunities(opps):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(opps, f, indent=2)

    print("[TRI] opportunities saved:", len(opps))


def run():

    print("[TRI] triangular arbitrage engine start")

    signals = load_prices()

    graph = build_graph(signals)

    opps = find_triangles(graph)

    print("[TRI] opportunities found:", len(opps))

    save_opportunities(opps)


def main():
    run()