import json
import os
import random

INPUT_FILE = "sources/liquidity_checked.json"
OUTPUT_FILE = "sources/execution_ready.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[EXECUTION] liquidity file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[EXECUTION] signals loaded:", len(data))
    return data


def simulate_execution(signal):

    bid = signal.get("bid", 0)
    ask = signal.get("ask", 0)

    if bid == 0 or ask == 0:
        return None

    spread = ask - bid

    latency_ms = random.randint(20, 120)

    slippage_factor = random.uniform(0.0001, 0.0015)

    slippage = ask * slippage_factor

    executable_entry = ask + slippage
    executable_exit = bid - slippage

    pnl = executable_exit - executable_entry

    signal["latency_ms"] = latency_ms
    signal["slippage"] = round(slippage, 8)
    signal["entry_exec"] = round(executable_entry, 8)
    signal["exit_exec"] = round(executable_exit, 8)
    signal["execution_pnl"] = round(pnl, 8)

    if pnl >= 0:
        signal["execution_score"] = "PASS"
    else:
        signal["execution_score"] = "FAIL"

    return signal


def process(signals):

    result = []

    for s in signals:

        executed = simulate_execution(s)

        if executed is None:
            continue

        if executed["execution_score"] == "PASS":
            result.append(executed)

    return result


def save(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("[EXECUTION] signals saved:", len(data))


def run():

    print("[EXECUTION] execution simulator start")

    signals = load_signals()

    processed = process(signals)

    print("[EXECUTION] execution-valid signals:", len(processed))

    save(processed)


def main():
    run()