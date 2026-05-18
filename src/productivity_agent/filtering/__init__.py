"""Content filtering and ranking engine."""

import re
from datetime import datetime
from typing import Any

from productivity_agent.sources import ContentItem


class FilterEngine:
    """Filters and ranks content items based on topic rules."""

    def __init__(self, topic: dict[str, Any]):
        self.topic = topic
        self._include_patterns = self._compile_keywords(topic.get("keywords_include", []))
        self._exclude_patterns = self._compile_keywords(topic.get("keywords_exclude", []))

    def filter_items(self, items: list[ContentItem]) -> list[ContentItem]:
        """Apply all filters to a list of content items."""
        results = []
        seen_urls = set()
        seen_titles = set()

        for item in items:
            if item.title.startswith("[") and "Error" in item.title:
                continue
            url_key = item.url.lower().rstrip("/") if item.url else ""
            title_key = item.title.lower().strip()[:80]
            if url_key and url_key in seen_urls:
                continue
            if title_key in seen_titles:
                continue
            if url_key:
                seen_urls.add(url_key)
            seen_titles.add(title_key)
            if not self._passes_keyword_filters(item):
                continue
            results.append(item)

        results = self._rank_items(results)
        max_items = self.topic.get("max_items", 5)
        return results[:max_items]

    def _passes_keyword_filters(self, item: ContentItem) -> bool:
        text = f"{item.title} {item.summary}".lower()
        if self._include_patterns:
            if not any(p.search(text) for p in self._include_patterns):
                return False
        if self._exclude_patterns:
            if any(p.search(text) for p in self._exclude_patterns):
                return False
        return True

    def _rank_items(self, items: list[ContentItem]) -> list[ContentItem]:
        scored = [(self._score_item(item), item) for item in items]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored]

    def _score_item(self, item: ContentItem) -> float:
        score = 0.0
        text = f"{item.title} {item.summary}".lower()
        likes = item.engagement.get("likes", 0)
        retweets = item.engagement.get("retweets", 0)
        if likes > 1000:
            score += 3.0
        elif likes > 500:
            score += 2.0
        elif likes > 100:
            score += 1.0
        if retweets > 500:
            score += 2.0
        elif retweets > 100:
            score += 1.0
        high_signal_sources = ["coindesk", "bitcoinmagazine", "theblock", "glassnode"]
        if any(s in item.source.lower() for s in high_signal_sources):
            score += 2.0
        if item.published:
            age_hours = (datetime.now() - item.published).total_seconds() / 3600
            if age_hours < 2:
                score += 2.0
            elif age_hours < 8:
                score += 1.0
            elif age_hours > 48:
                score -= 1.0
        important_words = ["sec", "etf", "regulation", "hack", "exploit", "adoption",
                          "institutional", "upgrade", "breaking", "urgent"]
        for word in important_words:
            if word in text:
                score += 1.5
                break
        return score

    @staticmethod
    def _compile_keywords(keywords: list[str]) -> list[re.Pattern]:
        patterns = []
        for kw in keywords:
            kw = kw.strip().lower()
            if kw:
                if len(kw) <= 4:
                    patterns.append(re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE))
                else:
                    patterns.append(re.compile(re.escape(kw), re.IGNORECASE))
        return patterns
