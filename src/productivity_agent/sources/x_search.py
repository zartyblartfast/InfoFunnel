"""X (Twitter) search source using xAI's x_search via the Hermes x_search tool.

This source is designed to be called from within a Hermes agent context
where the x_search tool is available. For standalone use, it falls back
to direct API calls using stored OAuth credentials.
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from productivity_agent.sources import SourceBase, ContentItem


class XSearchSource(SourceBase):
    """Fetches content from X/Twitter using x_search."""

    def __init__(self, use_hermes_tool: bool = True):
        self._use_hermes = use_hermes_tool

    @property
    def name(self) -> str:
        return "x_search"

    def fetch(self, topic: dict[str, Any], since: Optional[datetime] = None) -> list[ContentItem]:
        """Run x_search queries for a topic and return content items."""
        items = []
        queries = topic.get("x_queries", [])
        allowed_handles = topic.get("x_allowed_handles", [])
        excluded_handles = topic.get("x_excluded_handles", [])

        # Build date range
        from_date = since.strftime("%Y-%m-%d") if since else ""
        to_date = datetime.now().strftime("%Y-%m-%d")

        for query in queries:
            try:
                result = self._run_search(
                    query=query,
                    allowed_handles=allowed_handles if allowed_handles else None,
                    excluded_handles=excluded_handles if excluded_handles else None,
                    from_date=from_date,
                    to_date=to_date,
                )
                if result and result.get("success"):
                    items.extend(self._parse_result(result, query))
            except Exception as e:
                items.append(ContentItem(
                    title=f"[X Search Error] {query}: {e}",
                    url="",
                    source="x_search",
                ))

        return items

    def _run_search(self, query: str, allowed_handles: Optional[list],
                    excluded_handles: Optional[list], from_date: str,
                    to_date: str) -> Optional[dict]:
        """Execute x_search. Tries Hermes tool first, then direct API."""
        if self._use_hermes:
            return self._run_via_hermes(query, allowed_handles, excluded_handles, from_date, to_date)
        return self._run_via_api(query, allowed_handles, excluded_handles, from_date, to_date)

    def _run_via_hermes(self, query: str, allowed_handles: Optional[list],
                         excluded_handles: Optional[list], from_date: str,
                         to_date: str) -> Optional[dict]:
        """Run x_search through the Hermes agent CLI."""
        # Build a minimal prompt that triggers x_search
        prompt = f'Use x_search to search X for: "{query}"'
        if allowed_handles:
            prompt += f" from accounts: {', '.join(allowed_handles)}"
        if from_date:
            prompt += f" from {from_date} to {to_date}"
        prompt += ". Return results as JSON."

        try:
            result = subprocess.run(
                ["hermes", "chat", "-q", prompt, "--toolsets", "x_search"],
                capture_output=True, text=True, timeout=120
            )
            # The output will be the agent's response, not raw JSON
            # We need to extract the search results from the text output
            return {"success": True, "answer": result.stdout.strip(), "query": query}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _run_via_api(self, query: str, allowed_handles: Optional[list],
                     excluded_handles: Optional[list], from_date: str,
                     to_date: str) -> Optional[dict]:
        """Run x_search directly via xAI API using stored OAuth credentials."""
        try:
            from tools.x_search_tool import x_search_tool
            result = x_search_tool(
                query=query,
                allowed_x_handles=allowed_handles,
                excluded_x_handles=excluded_handles,
                from_date=from_date,
                to_date=to_date,
            )
            return json.loads(result)
        except ImportError:
            return {"success": False, "error": "x_search_tool not available. Run from Hermes context or install the package."}

    def _parse_result(self, result: dict, query: str) -> list[ContentItem]:
        """Parse x_search result into ContentItem objects."""
        items = []
        answer = result.get("answer", "")
        citations = result.get("inline_citations", [])

        # Each citation is a separate content item
        for citation in citations:
            url = citation.get("url", "")
            title = citation.get("title", "")
            if url:
                items.append(ContentItem(
                    title=title or url,
                    url=url,
                    source=f"x:{query}",
                ))

        # If no citations but we have an answer, create one item from the summary
        if not items and answer:
            items.append(ContentItem(
                title=f"X discussion: {query}",
                url="",
                source=f"x:{query}",
                summary=answer[:500],
            ))

        return items

    def health_check(self) -> dict[str, Any]:
        try:
            from tools.x_search_tool import check_x_search_requirements
            available = check_x_search_requirements()
            return {"source": self.name, "status": "ok" if available else "no_credentials"}
        except ImportError:
            return {"source": self.name, "status": "hermes_only"}
