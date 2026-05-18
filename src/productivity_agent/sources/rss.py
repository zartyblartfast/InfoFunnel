"""RSS feed source using blogwatcher-cli."""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from productivity_agent.sources import SourceBase, ContentItem


class RSSSource(SourceBase):
    """Fetches content from RSS feeds via blogwatcher-cli."""

    def __init__(self, blogwatcher_bin: Optional[str] = None):
        self._bin = blogwatcher_bin or self._find_blogwatcher()

    @property
    def name(self) -> str:
        return "rss"

    def _find_blogwatcher(self) -> str:
        """Locate blogwatcher-cli binary."""
        # Check common locations
        candidates = [
            os.path.join(os.path.expanduser("~"), "bin", "blogwatcher-cli.exe"),
            os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes", "profiles", "productivity", "home", "bin", "blogwatcher-cli.exe"),
            "blogwatcher-cli",  # hope it's on PATH
        ]
        for c in candidates:
            if os.path.isfile(c) or (c == "blogwatcher-cli" and self._cmd_exists(c)):
                return c
        return "blogwatcher-cli"  # fallback

    def _cmd_exists(self, cmd: str) -> bool:
        try:
            subprocess.run([cmd, "--help"], capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    def fetch(self, topic: dict[str, Any], since: Optional[datetime] = None) -> list[ContentItem]:
        """Fetch unread articles from blogwatcher for the topic's RSS feeds."""
        items = []
        feed_names = topic.get("rss_feeds", [])

        for feed_name in feed_names:
            try:
                articles = self._fetch_feed(feed_name, since)
                for article in articles:
                    items.append(ContentItem(
                        title=article.get("title", ""),
                        url=article.get("url", ""),
                        source=f"rss:{feed_name}",
                        published=article.get("published"),
                        summary=article.get("summary", ""),
                    ))
            except Exception as e:
                # Log but don't crash -- other feeds may work
                items.append(ContentItem(
                    title=f"[RSS Error] {feed_name}: {e}",
                    url="",
                    source=f"rss:{feed_name}",
                ))

        return items

    def _fetch_feed(self, feed_name: str, since: Optional[datetime] = None) -> list[dict]:
        """Fetch articles from a single blogwatcher feed."""
        # Run blogwatcher-cli articles --blog "Feed Name" --all
        cmd = [self._bin, "articles", "--blog", feed_name, "--all"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            raise RuntimeError(f"blogwatcher-cli failed: {result.stderr.strip()}")

        # Parse output -- blogwatcher outputs text, not JSON
        # We need to parse the text format
        return self._parse_articles_output(result.stdout, since)

    def _parse_articles_output(self, output: str, since: Optional[datetime] = None) -> list[dict]:
        """Parse blogwatcher-cli text output into article dicts."""
        articles = []
        current = {}

        for line in output.split("\n"):
            line = line.strip()
            if not line:
                if current.get("title"):
                    articles.append(current)
                    current = {}
                continue

            # Parse lines like:
            #   [1] Article Title
            #        Blog: CoinDesk
            #        URL: https://...
            #        Published: 2026-05-18
            if line.startswith("[") and "]" in line and "Blog:" not in line and "URL:" not in line and "Published:" not in line:
                if current.get("title"):
                    articles.append(current)
                    current = {}
                title = line.split("]", 1)[1].strip()
                current["title"] = title
            elif line.startswith("URL:"):
                current["url"] = line[4:].strip()
            elif line.startswith("Published:"):
                date_str = line[10:].strip()
                try:
                    current["published"] = datetime.fromisoformat(date_str)
                except ValueError:
                    current["published"] = None
            elif line.startswith("Blog:"):
                current["blog"] = line[5:].strip()

        if current.get("title"):
            articles.append(current)

        # Filter by date if specified
        if since:
            articles = [a for a in articles if a.get("published") and a["published"] >= since]

        return articles

    def health_check(self) -> dict[str, Any]:
        try:
            result = subprocess.run([self._bin, "--help"], capture_output=True, timeout=5)
            return {"source": self.name, "status": "ok" if result.returncode == 0 else "error"}
        except Exception as e:
            return {"source": self.name, "status": "error", "error": str(e)}
