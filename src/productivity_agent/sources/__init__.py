"""Information source plugins."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ContentItem:
    """A single piece of content from any source."""
    title: str
    url: str
    source: str           # e.g., "rss:Coindesk", "x_search"
    published: Optional[datetime] = None
    summary: str = ""
    author: str = ""
    engagement: dict = field(default_factory=dict)  # likes, retweets, etc.
    raw: Any = None       # original data for debugging

    @property
    def source_name(self) -> str:
        """Return the human-readable source name."""
        if self.source.startswith("rss:"):
            return self.source[4:]
        if self.source.startswith("x:"):
            return f"X ({self.source[2:]})"
        return self.source


class SourceBase(ABC):
    """Abstract base class for information sources."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable source name."""
        ...

    @abstractmethod
    def fetch(self, topic: dict[str, Any], since: Optional[datetime] = None) -> list[ContentItem]:
        """Fetch new content items for a topic.

        Args:
            topic: Topic configuration dict from news-monitor.yaml.
            since: Only return items newer than this datetime.

        Returns:
            List of ContentItem objects.
        """
        ...

    def health_check(self) -> dict[str, Any]:
        """Return health status of this source. Override in subclasses."""
        return {"source": self.name, "status": "unknown"}
