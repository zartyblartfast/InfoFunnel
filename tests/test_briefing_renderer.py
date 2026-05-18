import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from briefing_renderer import render_daily_briefing


def test_render_daily_briefing_groups_actionable_email_calendar_cleanup_and_questions():
    classified_items = [
        {
            "source_type": "gmail",
            "source_id": "msg-o2",
            "matched_registry_key": "notification@billing.o2.com",
            "classification": {
                "trust_level": "trusted_confirmed",
                "user_relationship": "current_applicable",
                "cost_status": "paid_active",
                "message_category": "billing",
                "urgency": "daily_briefing",
                "disposition": "review_today",
                "action_policy": "manual_check",
                "mutation_policy": "none_read_only",
            },
            "item": {
                "source_type": "gmail",
                "source_id": "msg-o2",
                "sender": "notification@billing.o2.com",
                "sender_display": "O2 <notification@billing.o2.com>",
                "subject": "Your O2 bill is ready",
                "date": "Sat, 16 May 2026 09:10:38 +0000",
                "snippet": "Your monthly snapshot is here",
            },
        },
        {
            "source_type": "gmail",
            "source_id": "msg-backblaze",
            "matched_registry_key": "no-reply@backblaze.com",
            "classification": {
                "trust_level": "likely_legitimate",
                "user_relationship": "historical_unused",
                "cost_status": "free_tier",
                "message_category": "quota_usage",
                "urgency": "weekly_cleanup",
                "disposition": "optional_cleanup",
                "action_policy": "optional_account_closure",
                "mutation_policy": "none_read_only",
            },
            "item": {
                "source_type": "gmail",
                "source_id": "msg-backblaze",
                "sender": "no-reply@backblaze.com",
                "sender_display": "Backblaze <no-reply@backblaze.com>",
                "subject": "Backblaze Daily Storage Cap reached 100%.",
                "date": "Sat, 16 May 2026 07:00:00 +0000",
                "snippet": "Storage cap reached.",
            },
        },
        {
            "source_type": "gmail",
            "source_id": "msg-unknown",
            "matched_registry_key": None,
            "classification": {
                "trust_level": "unknown",
                "user_relationship": "unknown_applicability",
                "cost_status": "unknown",
                "message_category": "unknown",
                "urgency": "daily_briefing",
                "disposition": "needs_user_classification",
                "action_policy": "ask_user",
                "mutation_policy": "none_read_only",
            },
            "item": {
                "source_type": "gmail",
                "source_id": "msg-unknown",
                "sender": "alerts@example.invalid",
                "sender_display": "Example Alerts <alerts@example.invalid>",
                "subject": "Account notice",
                "date": "Sat, 16 May 2026 08:00:00 +0000",
                "snippet": "Please review your account.",
            },
        },
        {
            "source_type": "google_calendar",
            "source_id": "event-1",
            "matched_registry_key": None,
            "classification": {
                "event_category": "meeting",
                "urgency": "daily_briefing",
                "disposition": "review_today",
                "action_policy": "report_only",
                "mutation_policy": "none_read_only",
            },
            "item": {
                "source_type": "google_calendar",
                "source_id": "event-1",
                "title": "Dentist appointment",
                "start": "2026-05-18T09:00:00+01:00",
                "end": "2026-05-18T09:30:00+01:00",
                "location": "High Street",
            },
        },
    ]

    text = render_daily_briefing(classified_items, title="Daily briefing dry-run")

    assert text.startswith("Daily briefing dry-run\nMode: read-only dry run; 0 mutations")
    assert "Must know today:" in text
    assert "O2 <notification@billing.o2.com> — Your O2 bill is ready" in text
    assert "known applicable; trusted_confirmed/current_applicable; action: manual_check" in text
    assert "Calendar:" in text
    assert "Dentist appointment — 2026-05-18T09:00:00+01:00 — High Street" in text
    assert "Cleanup/watchlist:" in text
    assert "Backblaze <no-reply@backblaze.com> — Backblaze Daily Storage Cap reached 100%." in text
    assert "optional_cleanup; free_tier; action: optional_account_closure" in text
    assert "Classification questions:" in text
    assert "Classify Example Alerts <alerts@example.invalid>" in text
    assert "Reply with: alerts@example.invalid <number>" in text
    assert "Full bodies omitted" in text


def test_render_daily_briefing_uses_empty_state_message_when_no_items():
    text = render_daily_briefing([], title="Daily briefing dry-run")

    assert text == "Daily briefing dry-run\nMode: read-only dry run; 0 mutations\nNo items to report."
