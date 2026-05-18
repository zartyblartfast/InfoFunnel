"""Tests for content filtering engine."""

import pytest
from datetime import datetime, timedelta

from productivity_agent.sources import ContentItem
from productivity_agent.filtering import FilterEngine


@pytest.fixture
def bitcoin_topic():
    return {
        "name": "Bitcoin",
        "max_items": 5,
        "keywords_include": ["bitcoin", "btc", "etf", "sec", "regulation"],
        "keywords_exclude": ["shitcoin", "memecoin", "scam"],
        "importance_rules": "Focus on regulatory and institutional news.",
    }


@pytest.fixture
def engine(bitcoin_topic):
    return FilterEngine(bitcoin_topic)


class TestKeywordFilters:
    def test_include_keyword_match(self, engine):
        items = [
            ContentItem(title="Bitcoin ETF approved by SEC", url="http://test.com/1", source="rss:test"),
            ContentItem(title="Dogecoin price surges", url="http://test.com/2", source="rss:test"),
        ]
        result = engine.filter_items(items)
        assert len(result) == 1
        assert "Bitcoin" in result[0].title

    def test_exclude_keyword_rejects(self, engine):
        items = [
            ContentItem(title="New shitcoin launched on Bitcoin", url="http://test.com/1", source="rss:test"),
        ]
        result = engine.filter_items(items)
        assert len(result) == 0

    def test_no_include_keywords_allows_all(self):
        topic = {"name": "Test", "keywords_include": [], "keywords_exclude": []}
        engine = FilterEngine(topic)
        items = [
            ContentItem(title="Anything goes", url="http://test.com/1", source="rss:test"),
        ]
        result = engine.filter_items(items)
        assert len(result) == 1


class TestDeduplication:
    def test_duplicate_urls_removed(self, engine):
        items = [
            ContentItem(title="Bitcoin news", url="http://test.com/1", source="rss:test"),
            ContentItem(title="Bitcoin news duplicate", url="http://test.com/1", source="x:test"),
        ]
        result = engine.filter_items(items)
        assert len(result) == 1

    def test_duplicate_titles_removed(self, engine):
        items = [
            ContentItem(title="Bitcoin ETF approved", url="http://test.com/1", source="rss:test"),
            ContentItem(title="Bitcoin ETF approved", url="http://test.com/2", source="x:test"),
        ]
        result = engine.filter_items(items)
        assert len(result) == 1


class TestRanking:
    def test_high_engagement_ranked_higher(self, engine):
        items = [
            ContentItem(title="Bitcoin news low", url="http://test.com/1", source="rss:test",
                       engagement={"likes": 10}),
            ContentItem(title="Bitcoin news high", url="http://test.com/2", source="rss:test",
                       engagement={"likes": 2000}),
        ]
        result = engine.filter_items(items)
        assert "high" in result[0].title.lower()

    def test_max_items_cap(self, engine):
        items = [
            ContentItem(title=f"Bitcoin news {i}", url=f"http://test.com/{i}", source="rss:test")
            for i in range(20)
        ]
        result = engine.filter_items(items)
        assert len(result) <= 5  # max_items from fixture
