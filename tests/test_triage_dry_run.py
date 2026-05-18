import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from triage_dry_run import (
    classify_case,
    classify_item,
    classify_records,
    evaluate_cases,
    extract_email_address,
    load_registry,
    load_cases,
    normalize_calendar_event,
    normalize_gmail_message,
    normalize_records,
)


def test_extract_email_address_handles_display_name_and_plain_address():
    assert extract_email_address("O2 <notification@billing.o2.com>") == "notification@billing.o2.com"
    assert extract_email_address("plain@example.com") == "plain@example.com"


def test_normalize_gmail_message_produces_standard_item_without_body_leakage():
    message = {
        "id": "msg-1",
        "threadId": "thread-1",
        "from": "O2 <notification@billing.o2.com>",
        "to": "user@example.com",
        "subject": "Your O2 bill is ready",
        "date": "Sat, 16 May 2026 09:10:38 +0000",
        "snippet": "Your monthly snapshot is here",
        "labels": ["UNREAD", "INBOX"],
        "body": "Full private body should not be copied into normalized dry-run items",
    }

    item = normalize_gmail_message(message)

    assert item == {
        "source_type": "gmail",
        "source_id": "msg-1",
        "thread_id": "thread-1",
        "sender": "notification@billing.o2.com",
        "sender_display": "O2 <notification@billing.o2.com>",
        "subject": "Your O2 bill is ready",
        "date": "Sat, 16 May 2026 09:10:38 +0000",
        "snippet": "Your monthly snapshot is here",
        "labels": ["UNREAD", "INBOX"],
    }


def test_normalize_calendar_event_produces_standard_item():
    event = {
        "id": "event-1",
        "summary": "Dentist appointment",
        "start": "2026-05-18T09:00:00+01:00",
        "end": "2026-05-18T09:30:00+01:00",
        "location": "High Street",
        "htmlLink": "https://calendar.google.com/event?eid=abc",
    }

    item = normalize_calendar_event(event)

    assert item == {
        "source_type": "google_calendar",
        "source_id": "event-1",
        "title": "Dentist appointment",
        "start": "2026-05-18T09:00:00+01:00",
        "end": "2026-05-18T09:30:00+01:00",
        "location": "High Street",
    }


def test_classify_item_classifies_normalized_gmail_message():
    registry = load_registry(ROOT / "sender-service-registry.csv")
    item = normalize_gmail_message({
        "id": "msg-1",
        "threadId": "thread-1",
        "from": "O2 <notification@billing.o2.com>",
        "subject": "Your O2 bill is ready",
        "date": "Sat, 16 May 2026 09:10:38 +0000",
        "snippet": "Your monthly snapshot is here",
        "labels": ["UNREAD", "INBOX"],
    })

    result = classify_item(item, registry)

    assert result["matched_registry_key"] == "notification@billing.o2.com"
    assert result["classification"]["trust_level"] == "trusted_confirmed"
    assert result["classification"]["message_category"] == "billing"
    assert result["classification"]["mutation_policy"] == "none_read_only"


def test_normalize_records_handles_gmail_list_and_calendar_list():
    gmail_records = [{"id": "msg-1", "from": "O2 <notification@billing.o2.com>", "subject": "Bill"}]
    calendar_records = [{"id": "event-1", "summary": "Meeting"}]

    gmail_items = normalize_records(gmail_records, "gmail")
    calendar_items = normalize_records(calendar_records, "google_calendar")

    assert gmail_items[0]["source_type"] == "gmail"
    assert gmail_items[0]["sender"] == "notification@billing.o2.com"
    assert calendar_items[0]["source_type"] == "google_calendar"
    assert calendar_items[0]["title"] == "Meeting"


def test_classify_records_normalizes_and_classifies_sample_records():
    registry = load_registry(ROOT / "sender-service-registry.csv")
    records = [{"id": "msg-1", "from": "O2 <notification@billing.o2.com>", "subject": "Bill"}]

    results = classify_records(records, "gmail", registry)

    assert len(results) == 1
    assert results[0]["matched_registry_key"] == "notification@billing.o2.com"
    assert results[0]["classification"]["disposition"] == "review_today"


def test_classify_case_uses_exact_sender_registry_match_for_backblaze():
    registry = load_registry(ROOT / "sender-service-registry.csv")
    case = {
        "id": "gmail-backblaze-quota-free-tier",
        "source_type": "gmail",
        "sender": "no-reply@backblaze.com",
        "subject_contains": "Storage Cap",
        "expected": {
            "trust_level": "likely_legitimate",
            "user_relationship": "historical_unused",
            "cost_status": "free_tier",
            "message_category": "quota_usage",
            "urgency": "weekly_cleanup",
            "disposition": "optional_cleanup",
            "action_policy": "optional_account_closure",
            "mutation_policy": "none_read_only",
        },
    }

    result = classify_case(case, registry)

    assert result["matched_registry_key"] == "no-reply@backblaze.com"
    assert result["actual"] == case["expected"]
    assert result["passed"] is True


def test_classify_case_falls_back_to_domain_registry_match():
    registry = load_registry(ROOT / "sender-service-registry.csv")
    case = {
        "id": "gmail-backblaze-domain-fallback",
        "source_type": "gmail",
        "sender": "alerts@backblaze.com",
        "expected": {
            "trust_level": "likely_legitimate",
            "user_relationship": "historical_unused",
            "cost_status": "free_tier",
            "message_category": "quota_usage",
            "urgency": "weekly_cleanup",
            "disposition": "optional_cleanup",
            "action_policy": "optional_account_closure",
            "mutation_policy": "none_read_only",
        },
    }

    result = classify_case(case, registry)

    assert result["matched_registry_key"] == "backblaze.com"
    assert result["actual"] == case["expected"]
    assert result["passed"] is True


def test_classify_unknown_gmail_sender_requests_user_classification_without_mutation():
    registry = load_registry(ROOT / "sender-service-registry.csv")
    case = {
        "id": "gmail-unknown-sender",
        "source_type": "gmail",
        "sender": "unknown@example.invalid",
        "expected": {
            "trust_level": "unknown",
            "user_relationship": "unknown_applicability",
            "cost_status": "unknown",
            "message_category": "unknown",
            "urgency": "daily_briefing",
            "disposition": "needs_user_classification",
            "action_policy": "ask_user",
            "mutation_policy": "none_read_only",
        },
    }

    result = classify_case(case, registry)

    assert result["matched_registry_key"] is None
    assert result["actual"] == case["expected"]
    assert result["passed"] is True


def test_evaluate_cases_reports_all_project_cases_pass():
    registry = load_registry(ROOT / "sender-service-registry.csv")
    cases = load_cases(ROOT / "triage-evaluation-cases.jsonl")

    report = evaluate_cases(cases, registry)

    assert report["total"] == 5
    assert report["passed"] == 5
    assert report["failed"] == 0
    assert all(item["passed"] for item in report["results"])
