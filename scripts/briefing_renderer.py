#!/usr/bin/env python3
"""Render read-only triage classifications into concise briefing text.

The renderer accepts already-normalized/classified items and produces a phone-safe
message format suitable for Hermes chat now and WhatsApp later. It deliberately
uses snippets/metadata only; full email bodies should not be supplied or emitted.
"""

from __future__ import annotations

from typing import Any


def _sender_label(item: dict[str, Any]) -> str:
    return str(item.get("sender_display") or item.get("sender") or "unknown sender")


def _subject_or_title(item: dict[str, Any]) -> str:
    return str(item.get("subject") or item.get("title") or item.get("source_id") or "untitled")


def _legitimacy_label(classification: dict[str, Any]) -> str:
    trust = classification.get("trust_level", "unknown")
    relationship = classification.get("user_relationship", "unknown_applicability")
    if relationship == "current_applicable" and trust == "trusted_confirmed":
        prefix = "known applicable"
    elif trust == "suspicious":
        prefix = "suspicious"
    elif relationship == "unknown_applicability":
        prefix = "applicability unknown"
    else:
        prefix = str(relationship).replace("_", " ")
    return f"{prefix}; {trust}/{relationship}"


def _question_for(result: dict[str, Any]) -> str:
    item = result.get("item", {})
    service = _sender_label(item)
    reply_key = item.get("sender") or service
    return "\n".join(
        [
            f"Classify {service}:",
            "1 current important",
            "2 current low priority",
            "3 historical free-tier",
            "4 historical paid-risk",
            "5 historical unknown cost",
            "6 noise candidate",
            "7 suspicious",
            "8 ignore/suppress",
            f"Reply with: {reply_key} <number>",
        ]
    )


def _render_email_line(result: dict[str, Any]) -> str:
    item = result.get("item", {})
    classification = result.get("classification", {})
    label = _legitimacy_label(classification)
    action = classification.get("action_policy", "report_only")
    return f"- {_sender_label(item)} — {_subject_or_title(item)} ({label}; action: {action})"


def _render_cleanup_line(result: dict[str, Any]) -> str:
    item = result.get("item", {})
    classification = result.get("classification", {})
    disposition = classification.get("disposition", "review_when_convenient")
    cost = classification.get("cost_status", "unknown")
    action = classification.get("action_policy", "report_only")
    return f"- {_sender_label(item)} — {_subject_or_title(item)} ({disposition}; {cost}; action: {action})"


def _render_calendar_line(result: dict[str, Any]) -> str:
    item = result.get("item", {})
    title = _subject_or_title(item)
    start = item.get("start") or "time not provided"
    location = item.get("location") or "no location"
    return f"- {title} — {start} — {location}"


def render_daily_briefing(classified_items: list[dict[str, Any]], title: str = "Daily briefing") -> str:
    """Render classified read-only items into the concise briefing format."""
    lines = [title, "Mode: read-only dry run; 0 mutations"]
    if not classified_items:
        lines.append("No items to report.")
        return "\n".join(lines)

    must_know: list[str] = []
    calendar: list[str] = []
    cleanup: list[str] = []
    questions: list[str] = []

    for result in classified_items:
        source_type = result.get("source_type")
        classification = result.get("classification", {})
        disposition = classification.get("disposition")
        action_policy = classification.get("action_policy")

        if action_policy == "ask_user" or disposition == "needs_user_classification":
            questions.append(_question_for(result))
        elif source_type == "google_calendar":
            calendar.append(_render_calendar_line(result))
        elif disposition in {"optional_cleanup", "noise_candidate", "review_when_convenient"}:
            cleanup.append(_render_cleanup_line(result))
        else:
            must_know.append(_render_email_line(result))

    if must_know:
        lines.append("Must know today:")
        lines.extend(must_know)
    if calendar:
        lines.append("Calendar:")
        lines.extend(calendar)
    if cleanup:
        lines.append("Cleanup/watchlist:")
        lines.extend(cleanup)
    if questions:
        lines.append("Classification questions:")
        lines.extend(questions)

    lines.append("Privacy: Full bodies omitted; use source apps for details and avoid clicking links from uncertain senders.")
    return "\n".join(lines)
