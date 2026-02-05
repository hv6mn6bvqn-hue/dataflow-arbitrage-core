from pathlib import Path
import json
import shutil

STRONG_SIGNALS_DIR = Path("core/exports/strong_signals")

FEED_ROOT = Path("core/exports/feed")
FEED_V1 = FEED_ROOT / "v1"
FEED_V1_STRONG = FEED_V1 / "strong_signals"

PUBLIC_ROOT = Path("docs/feed")

FEED_V1_STRONG.mkdir(parents=True, exist_ok=True)


def build_feed_v1():
    feed_index = []

    for signal_file in sorted(STRONG_SIGNALS_DIR.glob("signal_*.json")):
        signal = json.loads(signal_file.read_text())

        public_signal = {
            "version": "1.0",
            "timestamp": signal["timestamp"],
            "signal_type": signal["signal_type"],
            "confidence": signal["confidence"],
            "confirmed": signal.get("confirmed", False)
        }

        target = FEED_V1_STRONG / signal_file.name
        target.write_text(json.dumps(public_signal, indent=2))

        feed_index.append({
            "file": f"strong_signals/{signal_file.name}",
            "timestamp": signal["timestamp"],
            "confidence": signal["confidence"]
        })

    index_path = FEED_V1 / "index.json"
    index_path.write_text(json.dumps({
        "feed_version": "v1",
        "schema_version": "1.0",
        "signal_count": len(feed_index),
        "signals": feed_index[-20:]
    }, indent=2))


def build_manifest():
    manifest = {
        "latest": "v1",
        "feeds": {
            "v1": {
                "schema_version": "1.0",
                "path": "v1/",
                "guarantees": [
                    "fields will not be removed",
                    "types will not change",
                    "new fields may be added"
                ]
            }
        }
    }

    (FEED_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2))


def publish_to_docs():
    if PUBLIC_ROOT.exists():
        shutil.rmtree(PUBLIC_ROOT)

    shutil.copytree(FEED_ROOT, PUBLIC_ROOT)


def build_feed():
    build_feed_v1()
    build_manifest()
    publish_to_docs()


if __name__ == "__main__":
    build_feed()
