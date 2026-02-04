import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

STATE_FILE = Path("sources/.web_state")


def fetch_rss(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read()


def get_latest_item_id(rss_bytes):
    root = ET.fromstring(rss_bytes)
    channel = root.find("channel")
    if channel is None:
        return None

    item = channel.find("item")
    if item is None:
        return None

    guid = item.findtext("guid")
    link = item.findtext("link")
    title = item.findtext("title")

    return guid or link or title


def load_last_state():
    if not STATE_FILE.exists():
        return None
    return STATE_FILE.read_text().strip()


def save_state(value):
    STATE_FILE.write_text(value)


def generate_signal():
    RSS_URL = "https://news.ycombinator.com/rss"

    try:
        rss = fetch_rss(RSS_URL)
        latest_id = get_latest_item_id(rss)

        if latest_id is None:
            return {
                "signal_type": "web_error",
                "confidence": "0.05",
                "note": "unable to parse rss"
            }

        last_id = load_last_state()

        if last_id != latest_id:
            save_state(latest_id)
            return {
                "signal_type": "web_activity",
                "confidence": "0.45",
                "note": "new public item detected"
            }

        return {
            "signal_type": "web_stable",
            "confidence": "0.10",
            "note": "no change in public feed"
        }

    except Exception as e:
        return {
            "signal_type": "web_exception",
            "confidence": "0.01",
            "note": str(e)
        }
