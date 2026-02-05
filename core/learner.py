from pathlib import Path
import json

LOG_PATH = Path("core/logs/signal.log")
WEIGHTS_PATH = Path("core/state/weights.json")

DEFAULT_WEIGHTS = {
    "predictor": 1.0,
    "predictor_velocity": 1.0
}


def load_weights():
    if WEIGHTS_PATH.exists():
        return json.loads(WEIGHTS_PATH.read_text())
    WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    WEIGHTS_PATH.write_text(json.dumps(DEFAULT_WEIGHTS, indent=2))
    return DEFAULT_WEIGHTS.copy()


def save_weights(weights):
    WEIGHTS_PATH.write_text(json.dumps(weights, indent=2))


def read_recent_blocks():
    if not LOG_PATH.exists():
        return []

    blocks = LOG_PATH.read_text().strip().split("---")
    parsed = []

    for block in blocks:
        entry = {}
        for line in block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                entry[k.strip()] = v.strip()
        if entry:
            parsed.append(entry)

    return parsed[-10:]


def evaluate_signal(blocks):
    primary = None
    aftermath = None

    for b in reversed(blocks):
        if b.get("source") == "prioritizer" and not primary:
            primary = b
        elif primary and b.get("source") == "analyzer":
            aftermath = b
            break

    if not primary or not aftermath:
        return None

    try:
        p_conf = float(primary.get("confidence", 0))
        a_conf = float(aftermath.get("confidence", 0))
    except ValueError:
        return None

    return a_conf - p_conf


def main():
    weights = load_weights()
    blocks = read_recent_blocks()
    delta = evaluate_signal(blocks)

    if delta is None:
        return

    if delta > 0:
        weights["predictor"] += 0.05
        weights["predictor_velocity"] += 0.05
    else:
        weights["predictor"] = max(0.1, weights["predictor"] - 0.05)
        weights["predictor_velocity"] = max(0.1, weights["predictor_velocity"] - 0.05)

    save_weights(weights)


if __name__ == "__main__":
    main()
