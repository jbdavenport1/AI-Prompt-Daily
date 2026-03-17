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


def clean_title(title: str) -> str:
    title = title.strip()

    if " - " in title:
        title = title.split(" - ")[0].strip()

    return title


def score_headline(title: str) -> int:
    score = 0
    lowered = title.lower()

    strong_terms = [
        "openai",
        "anthropic",
        "google",
        "gemini",
        "microsoft",
        "meta",
        "nvidia",
        "ai",
        "artificial intelligence",
        "model",
        "agent",
        "startup",
        "funding",
        "launch",
    ]

    weak_terms = [
        "stock",
        "buy for",
        "price prediction",
        "motley fool",
    ]

    for term in strong_terms:
        if term in lowered:
            score += 2

    for term in weak_terms:
        if term in lowered:
            score -= 2

    if len(title) <= 100:
        score += 1

    return score


def fetch_news(limit_per_feed: int = 10, max_results: int = 5) -> List[Dict]:
    items: List[Dict] = []

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit_per_feed]:
            title = entry.get("title", "").strip()
            clean = clean_title(title)

            items.append({
                "title": clean,
                "url": entry.get("link", "").strip(),
                "source": "Unknown",
                "published": entry.get("published", ""),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "score": score_headline(clean),
            })

    deduped = dedupe_news(items)
    ranked = sorted(deduped, key=lambda x: x.get("score", 0), reverse=True)

    for item in ranked:
        item.pop("score", None)

    return ranked[:max_results]


def dedupe_news(items: List[Dict]) -> List[Dict]:
    seen = set()
    result = []

    for item in items:
        key = item["title"].lower().strip()

        if key and key not in seen:
            seen.add(key)
            result.append(item)

    return result
