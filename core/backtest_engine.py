import json
import os
import random

INPUT_FILE = "sources/risk_checked.json"
OUTPUT_FILE = "sources/backtest_report.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[BACKTEST] input file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def simulate(signal):

    pnl = signal.get("execution_pnl", 0)

    variation = random.uniform(-0.5, 1.5)

    result = pnl * variation

    signal["backtest_pnl"] = round(result, 8)

    if result > 0:
        signal["backtest_result"] = "WIN"
    else:
        signal["backtest_result"] = "LOSS"

    return signal


def run():

    print("[BACKTEST] engine start")

    signals = load_signals()

    result = []

    wins = 0
    losses = 0

    for signal in signals:

        tested = simulate(signal)

        if tested["backtest_result"] == "WIN":
            wins += 1
        else:
            losses += 1

        result.append(tested)

    report = {
        "total": len(result),
        "wins": wins,
        "losses": losses,
        "winrate": round(wins / len(result), 4) if result else 0,
        "signals": result
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print("[BACKTEST] total:", len(result))
    print("[BACKTEST] wins:", wins)
    print("[BACKTEST] losses:", losses)


def main():
    run()