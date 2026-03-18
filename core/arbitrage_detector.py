import json
import os

INPUT_FILE = "sources/matrix_opportunities.json"
OUTPUT_FILE = "sources/arbitrage_opportunities.json"


def load_matrix():

    if not os.path.exists(INPUT_FILE):
        print("[ARBITRAGE] matrix file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[ARBITRAGE] matrix loaded:", len(data))
    return data


def filter_opportunities(matrix):

    return [m for m in matrix if m.get("spread", 0) > 0.003]


def save_opportunities(opps):

    with open(OUTPUT_FILE, "w") as f:
        json.dump(opps, f, indent=2)

    print("[ARBITRAGE] opportunities saved:", len(opps))


def run():

    print("[ARBITRAGE] loading matrix opportunities")

    matrix = load_matrix()

    opportunities = filter_opportunities(matrix)

    print("[ARBITRAGE] opportunities found:", len(opportunities))

    save_opportunities(opportunities)


def main():
    run()


if __name__ == "__main__":
    main()