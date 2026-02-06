import json
from pathlib import Path
from datetime import datetime, timedelta

LOG_PATH = Path("core/logs/signal.log")
FEED_DIR = Path("feed")
FEED_DIR.mkdir(parents=True, exist_ok=True)

FEED_FILE = FEED_DIR / "index.json"

TTL_MINUTES = {
    "low": 15,
    "medium": 60,
    "high": 180
}

def parse_log_entries():
    if not LOG_PATH.exists():
        return []

    raw = LOG_PATH.read_text().strip().split("---")
    entries = []

    for block in raw:
        lines = [l.strip() for l in block.strip().splitlines() if ":" in l]
        if not lines:
            continue

        data = {}
        for line in lines:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()

        entries.append(data)

    return entries


def rank_signal(confidence: float) -> str:
    if confidence >= 0.7:
        return "high"
    if confidence >= 0.35:
        return "medium"
    return "low"


def build_feed():
    now = datetime.utcnow()
    signals = []

    entries = parse_log_entries()

    for i, e in enumerate(entries):
        try:
            confidence = float(e.get("confidence", 0))
        except ValueError:
            continue

        rank = rank_signal(confidence)

        # ❗️Фильтр: low не публикуем
        if rank == "low":
            continue

        ttl = TTL_MINUTES[rank]
        expires_at = now + timedelta(minutes=ttl)

        signal = {
            "signal_id": f"df-{now.strftime('%Y%m%d')}-{i+1:03d}",
            "type": e.get("signal_type", "unknown"),
            "confidence": confidence,
            "rank": rank,
            "expires_at": expires_at.isoformat() + "Z"
        }

        signals.append(signal)

    feed = {
        "feed_version": "v1",
        "generated_at": now.isoformat() + "Z",
        "signal_count": len(signals),
        "signals": signals
    }

    FEED_FILE.write_text(json.dumps(feed, indent=2))


if __name__ == "__main__":
    build_feed()
