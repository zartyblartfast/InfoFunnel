#!/usr/bin/env python3
"""Dry-run evaluator for the personal productivity triage taxonomy.

This script is intentionally read-only. It loads local project files only:
- sender-service-registry.csv
- triage-evaluation-cases.jsonl

It does not connect to Gmail, Calendar, Yahoo, or any external service.
"""

from __future__ import annotations

import argparse
import csv
import json
from email.utils import parseaddr
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

UNKNOWN_GMAIL_CLASSIFICATION = {
    "trust_level": "unknown",
    "user_relationship": "unknown_applicability",
    "cost_status": "unknown",
    "message_category": "unknown",
    "urgency": "daily_briefing",
    "disposition": "needs_user_classification",
    "action_policy": "ask_user",
    "mutation_policy": "none_read_only",
}

GENERIC_CALENDAR_CLASSIFICATION = {
    "event_category": "meeting",
    "urgency": "daily_briefing",
    "disposition": "review_today",
    "action_policy": "report_only",
    "mutation_policy": "none_read_only",
}


def load_registry(path: Path) -> list[dict[str, str]]:
    """Load sender/service registry rows from CSV."""
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_cases(path: Path) -> list[dict[str, Any]]:
    """Load JSONL evaluation cases."""
    cases: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(json.loads(line))
    return cases


def load_json_records(path: Path) -> list[dict[str, Any]]:
    """Load records from a JSON file containing either one object or a list."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    raise ValueError(f"Expected JSON object or list in {path}")


def extract_email_address(value: str) -> str:
    """Extract and lowercase an email address from a display-name header."""
    _display_name, address = parseaddr(value or "")
    return (address or value or "").strip().lower()


def normalize_gmail_message(message: dict[str, Any]) -> dict[str, Any]:
    """Convert a Gmail API/search result into the standard dry-run item shape.

    Full message bodies are deliberately excluded to keep dry-run artifacts compact
    and to avoid unnecessary private body-text retention.
    """
    sender_display = str(message.get("from", ""))
    return {
        "source_type": "gmail",
        "source_id": message.get("id", ""),
        "thread_id": message.get("threadId", ""),
        "sender": extract_email_address(sender_display),
        "sender_display": sender_display,
        "subject": message.get("subject", ""),
        "date": message.get("date", ""),
        "snippet": message.get("snippet", ""),
        "labels": list(message.get("labels", [])),
    }


def normalize_calendar_event(event: dict[str, Any]) -> dict[str, Any]:
    """Convert a Google Calendar event into the standard dry-run item shape."""
    return {
        "source_type": "google_calendar",
        "source_id": event.get("id", ""),
        "title": event.get("summary", ""),
        "start": event.get("start", ""),
        "end": event.get("end", ""),
        "location": event.get("location", ""),
    }


def normalize_records(records: list[dict[str, Any]], source_type: str) -> list[dict[str, Any]]:
    """Normalize a list of records from a supported read-only source."""
    if source_type == "gmail":
        return [normalize_gmail_message(record) for record in records]
    if source_type == "google_calendar":
        return [normalize_calendar_event(record) for record in records]
    raise ValueError(f"Unsupported source_type: {source_type}")


def _sender_domain(sender: str) -> str | None:
    if "@" not in sender:
        return None
    return sender.rsplit("@", 1)[1].lower()


def _match_registry(case: dict[str, Any], registry: list[dict[str, str]]) -> dict[str, str] | None:
    sender = extract_email_address(str(case.get("sender", "")))
    if not sender:
        return None

    for row in registry:
        if row.get("match_type") == "exact_sender" and row.get("sender_or_domain", "").lower() == sender:
            return row

    domain = _sender_domain(sender)
    if not domain:
        return None

    for row in registry:
        if row.get("match_type") == "domain" and row.get("sender_or_domain", "").lower() == domain:
            return row

    return None


def _classification_from_registry(row: dict[str, str]) -> dict[str, str]:
    return {
        "trust_level": row["trust_level"],
        "user_relationship": row["user_relationship"],
        "cost_status": row["cost_status"],
        "message_category": row["default_message_category"],
        "urgency": row["default_urgency"],
        "disposition": row["default_disposition"],
        "action_policy": row["action_policy"],
        "mutation_policy": row["mutation_policy"],
    }


def _default_classification(case: dict[str, Any]) -> dict[str, str]:
    if case.get("source_type") == "google_calendar":
        return dict(GENERIC_CALENDAR_CLASSIFICATION)
    return dict(UNKNOWN_GMAIL_CLASSIFICATION)


def classify_item(item: dict[str, Any], registry: list[dict[str, str]]) -> dict[str, Any]:
    """Classify one normalized item without requiring an expected outcome."""
    row = _match_registry(item, registry)
    classification = _classification_from_registry(row) if row else _default_classification(item)
    return {
        "source_type": item.get("source_type"),
        "source_id": item.get("source_id"),
        "matched_registry_key": row.get("sender_or_domain") if row else None,
        "classification": classification,
        "item": item,
    }


def classify_records(records: list[dict[str, Any]], source_type: str, registry: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Normalize and classify records from one read-only source."""
    return [classify_item(item, registry) for item in normalize_records(records, source_type)]


def classify_case(case: dict[str, Any], registry: list[dict[str, str]]) -> dict[str, Any]:
    """Classify one evaluation case using registry defaults and safe fallbacks."""
    row = _match_registry(case, registry)
    actual = _classification_from_registry(row) if row else _default_classification(case)

    expected = case.get("expected", {})
    comparable_actual = {key: actual.get(key) for key in expected}
    mismatches = {
        key: {"expected": value, "actual": comparable_actual.get(key)}
        for key, value in expected.items()
        if comparable_actual.get(key) != value
    }

    return {
        "id": case.get("id"),
        "matched_registry_key": row.get("sender_or_domain") if row else None,
        "actual": comparable_actual,
        "expected": expected,
        "passed": not mismatches,
        "mismatches": mismatches,
    }


def evaluate_cases(cases: list[dict[str, Any]], registry: list[dict[str, str]]) -> dict[str, Any]:
    """Evaluate all cases and return a summary report."""
    results = [classify_case(case, registry) for case in cases]
    passed = sum(1 for item in results if item["passed"])
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run read-only triage evaluation cases or classify local sample records.")
    parser.add_argument("--registry", type=Path, default=PROJECT_ROOT / "sender-service-registry.csv")
    parser.add_argument("--cases", type=Path, default=PROJECT_ROOT / "triage-evaluation-cases.jsonl")
    parser.add_argument("--gmail-json", action="append", type=Path, default=[], help="Local Gmail JSON sample file to normalize/classify")
    parser.add_argument("--calendar-json", action="append", type=Path, default=[], help="Local Calendar JSON sample file to normalize/classify")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    sample_results: list[dict[str, Any]] = []
    for path in args.gmail_json:
        sample_results.extend(classify_records(load_json_records(path), "gmail", registry))
    for path in args.calendar_json:
        sample_results.extend(classify_records(load_json_records(path), "google_calendar", registry))

    if sample_results:
        report = {"total": len(sample_results), "results": sample_results}
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(f"sample dry-run: {report['total']} classified, 0 mutations")
            for item in sample_results:
                classification = item["classification"]
                display = item["item"].get("subject") or item["item"].get("title") or item["source_id"]
                print(
                    f"{item['source_type']} {item['source_id']}: "
                    f"{classification.get('urgency')} / {classification.get('disposition')} / "
                    f"{classification.get('action_policy')} :: {display}"
                )
        return 0

    report = evaluate_cases(load_cases(args.cases), registry)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"triage dry-run: {report['passed']}/{report['total']} passed, {report['failed']} failed")
        for item in report["results"]:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item['id']}")
            if not item["passed"]:
                print(json.dumps(item["mismatches"], indent=2, ensure_ascii=False))
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
