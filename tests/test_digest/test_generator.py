"""Tests for digest generation."""

import pytest
from datetime import datetime

from productivity_agent.sources import ContentItem
from productivity_agent.digest import DigestGenerator


@pytest.fixture
def config():
    return {
        "global": {"max_total_items": 10},
        "topics": [],
    }


@pytest.fixture
def generator(config):
    return DigestGenerator(config)


class TestDigestGenerator:
    def test_empty_topics(self, generator):
        result = generator.generate({})
        assert "Digest generated at" in result

    def test_topic_with_items(self, generator):
        items = [
            ContentItem(
                title="Bitcoin ETF Approved",
                url="http://test.com/1",
                source="rss:CoinDesk",
                summary="The SEC has approved a spot Bitcoin ETF for the first time.",
            ),
        ]
        result = generator.generate({"Bitcoin": items})
        assert "Bitcoin" in result
        assert "ETF" in result
        assert "CoinDesk" in result

    def test_empty_topic_shows_no_developments(self, generator):
        result = generator.generate({"Bitcoin": []})
        assert "No significant developments" in result

    def test_global_max_items_cap(self):
        config = {"global": {"max_total_items": 3}}
        gen = DigestGenerator(config)
        items_a = [
            ContentItem(title=f"Topic A {i}", url=f"http://a.com/{i}", source="rss:test")
            for i in range(5)
        ]
        items_b = [
            ContentItem(title=f"Topic B {i}", url=f"http://b.com/{i}", source="rss:test")
            for i in range(5)
        ]
        result = gen.generate({"Topic A": items_a, "Topic B": items_b})
        # Should not exceed 3 total
        assert result.count("Topic A") + result.count("Topic B") <= 6  # headers + items
