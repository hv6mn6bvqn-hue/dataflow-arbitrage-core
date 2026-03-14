import json
import os

INPUT_FILE = "sources/execution_validated.json"
OUTPUT_FILE = "sources/execution_scored.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[EXEC_SCORE] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def score(signal):

    spread = signal.get("execution_spread", 0)
    slippage = signal.get("slippage", 0.12)

    raw_score = spread - slippage

    final_score = round(raw_score, 4)

    signal["execution_score"] = final_score

    return signal


def run():

    print("[EXEC_SCORE] engine start")

    signals = load_signals()

    scored = [score(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(scored, f, indent=2)

    print(f"[EXEC_SCORE] scored: {len(scored)}")


def main():
    run()