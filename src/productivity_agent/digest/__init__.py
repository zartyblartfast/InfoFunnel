"""Digest generation and formatting."""

import os
from datetime import datetime
from typing import Any

from productivity_agent.sources import ContentItem
from productivity_agent.filtering import FilterEngine


class DigestGenerator:
    """Generates formatted digests from filtered content items."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.global_config = config.get("global", {})

    def generate(self, topic_results: dict[str, list[ContentItem]]) -> str:
        """Generate a full digest from topic-filtered items.

        Args:
            topic_results: Dict mapping topic name -> list of ContentItem

        Returns:
            Formatted digest string.
        """
        sections = []
        total_items = 0
        max_total = self.global_config.get("max_total_items", 10)

        for topic_name, items in topic_results.items():
            if not items:
                sections.append(self._format_empty_topic(topic_name))
                continue

            # Apply global cap
            remaining = max_total - total_items
            if remaining <= 0:
                break
            items = items[:remaining]

            total_items += len(items)
            sections.append(self._format_topic_section(topic_name, items))

        # Add footer
        sections.append(self._format_footer())

        return "\n".join(sections)

    def _format_topic_section(self, topic_name: str, items: list[ContentItem]) -> str:
        """Format a single topic's items."""
        lines = [f"### {topic_name}", ""]

        for i, item in enumerate(items, 1):
            lines.append(f"**{i}. {item.title}**")
            if item.summary:
                # Truncate summary to 2 sentences
                summary = self._truncate_summary(item.summary, max_sentences=2)
                lines.append(f"Why it matters: {summary}")
            lines.append(f"Source: {item.source_name}")
            if item.url:
                lines.append(f"Link: {item.url}")
            lines.append("")

        return "\n".join(lines)

    def _format_empty_topic(self, topic_name: str) -> str:
        return f"### {topic_name}\n\nNo significant developments since last check.\n"

    def _format_footer(self) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return (
            f"---\n"
            f"Digest generated at {now}\n"
            f"Config: config/news-monitor.yaml\n"
            f"Admin: python scripts/news-monitor-admin.py"
        )

    @staticmethod
    def _truncate_summary(text: str, max_sentences: int = 2) -> str:
        """Truncate text to N sentences."""
        sentences = text.replace("!", ".").replace("?", ".").split(".")
        kept = []
        for s in sentences:
            s = s.strip()
            if s:
                kept.append(s)
                if len(kept) >= max_sentences:
                    break
        result = ". ".join(kept)
        if not result.endswith("."):
            result += "."
        return result
