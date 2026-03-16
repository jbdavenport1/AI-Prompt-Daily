from __future__ import annotations
import feedparser
from datetime import datetime, timezone
from typing import List, Dict

FEEDS = [
    "https://news.google.com/rss/search?q=artificial+intelligence",
    "https://news.google.com/rss/search?q=OpenAI",
    "https://news.google.com/rss/search?q=Anthropic",
    "https://news.google.com/rss/search?q=Google+Gemini",
    "https://news.google.com/rss/search?q=AI+startup",
]

def fetch_news(limit_per_feed: int = 10) -> List[Dict]:
    items: List[Dict] = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:limit_per_feed]:
            items.append({
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", "").strip(),
                "source": "Unknown",
                "published": entry.get("published", ""),
                "fetched_at": datetime.now(timezone.utc).isoformat()
            })
    return dedupe_news(items)

def dedupe_news(items: List[Dict]) -> List[Dict]:
    seen = set()
    result = []
    for item in items:
        key = item["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result
