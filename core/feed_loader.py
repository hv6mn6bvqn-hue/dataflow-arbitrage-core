from pathlib import Path
import json

FEED_PATH = Path("docs/feed/index.json")


def load_feed():
    """
    Load full feed (for backtest / replay).
    Returns list of signals.
    """
    if not FEED_PATH.exists():
        return []

    data = json.loads(FEED_PATH.read_text())
    return data.get("signals", [])


def load_latest_signal():
    """
    Load latest signal only (for action engine).
    """
    signals = load_feed()
    if not signals:
        return None
    return signals[-1]