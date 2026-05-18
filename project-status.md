# Personal Productivity Agent Project Status

Last updated: 2026-05-17 20:52:20 GMTDT

## Current status

- Workspace: `C:\hermes\PersonalProductivity`
- Main plan: `.hermes/plans/2026-05-16_231638-ai-email-calendar-alert-agent-team.md`
- Hermes productivity profile `terminal.cwd` has been set to this workspace.
- Google Workspace OAuth is authenticated for read-only Gmail and read-only Calendar.
- Google OAuth client secret is present in this profile.
- Live Google Calendar API check succeeded.
- Gmail read-only search succeeded.
- A first manual read-only Gmail triage pass has been completed and saved to `important-email-review.md`.
- A first manual read-only daily briefing draft has been completed and saved to `daily-briefing-draft.md`.
- Calendar list returned successfully; no events were returned for today or tomorrow in the checked window.
- Himalaya/Yahoo IMAP is not installed/configured yet.
- No Hermes cron jobs are currently scheduled.

## Recommended next step

Shift from manual sender-by-sender inbox triage to building the agentic productivity system. The next milestone is to validate the controlled taxonomy, structured sender/service registry, feedback protocol, and evaluation cases before doing more live inbox review.

Immediate next milestones:

- Review `email-calendar-taxonomy.md` and confirm the enum set is acceptable.
- Review `sender-service-registry.csv` as the first structured registry replacing prose-heavy classification.
- Dry-run classifier/evaluator has been built at `scripts/triage_dry_run.py` and tested with `tests/test_triage_dry_run.py`.
- The evaluator now normalizes local Gmail/Calendar sample JSON into standard read-only item records before classification; normalized Gmail items deliberately exclude full body text.
- Current evaluator result: 5/5 evaluation cases passed; report saved to `.tmp/triage_dry_run_report.json`.
- Current local sample classification result: 3 items classified, 0 mutations; report saved to `.tmp/structured_sample_classification_report.json`.
- A tested read-only briefing renderer now exists at `scripts/briefing_renderer.py`; current local sample preview saved to `.tmp/daily_briefing_preview.txt`.
- Next: wire briefing rendering into the dry-run CLI/scheduled-agent path, then review/expand taxonomy and evaluation cases before another read-only Gmail/Calendar sample pass.
- Later configure Yahoo IMAP/Himalaya if Yahoo inbox support is still wanted.
- Later configure WhatsApp gateway delivery.
- Create cron jobs only after manual dry-run quality is acceptable.

## Preliminary setup completed

Created starter project files for rules, important senders/categories, allowlists, unwanted sender review, cleanup review, and alert formatting. These are intentionally conservative and read-only first.

## Rule updates approved and applied on 2026-05-17 19:14:15 GMTDT

- Added O2 billing sender/domain to `important-senders.md` and `allowed-senders.md`.
- Added LifeSight/WTW sender/domain to `important-senders.md` and `allowed-senders.md`.
- Added repeated noisy promotional/community/job-digest senders to `unwanted-senders.md` as report-only `candidate` entries.
- Updated `important-categories.md` with utility/mobile billing and pension/finance-account categories.
- These updates are classification/reporting rules only; no mailbox actions were taken.

## Legitimacy/applicability reporting update on 2026-05-17

- User clarified that known-applicable senders such as O2 should be handled differently from uncertain senders such as Backblaze.
- Reports should now include legitimacy/applicability evidence for uncertain senders, including official organization/domain, email authentication signals where available, and safer action guidance.
- Created `sender-legitimacy-checks.md`.
- Created `email-sender-classification-ledger.md` and machine-readable `email-sender-classification-ledger.csv`.
- Created `subscription-savings-watchlist.md`.
- Updated `email-calendar-alert-rules.md`, `whatsapp-alert-format.md`, and `daily-briefing-draft.md` to include legitimacy/applicability assessment.
- Backblaze assessment: likely legitimate and historically applicable; user used it for a prototype app but no longer needs it. User confirmed usage is free-tier, so there is no payment urgency; remaining action is optional account closure/data cleanup.


## Agentic system design pivot on 2026-05-17

- User clarified the project goal: Hermes should act as the development partner building an agentic personal productivity system, not as a one-off inbox triage assistant.
- Live Gmail/Calendar data should be used only as read-only sample/test data unless mutations are explicitly approved.
- Created `hermes-goal.md` with the recommended `/goal` wording and operating interpretation.
- Created `email-calendar-taxonomy.md` with predefined controlled classification enums.
- Created `agent-workflow.md` defining the read-only agent loop and scheduled-agent roadmap.
- Created `feedback-protocol.md` for low-friction multiple-choice user feedback.
- Created `sender-service-registry.schema.json` and `sender-service-registry.csv` as the structured machine-readable registry.
- Created `triage-evaluation-cases.jsonl` with initial test cases from O2, Backblaze, LifeSight, marketing, and calendar examples.
- Future work should prioritize the taxonomy/registry/evaluation workflow over additional manual inbox sorting.

## Safety defaults

- Read-only until explicitly approved.
- No email deletion, archive, labels, filters, unsubscribe clicks, replies, calendar edits, or todo writes by default.
- Any future cleanup must start with preview-only and exact sender matching.
- WhatsApp is the preferred final alert channel, but setup/debug can use the current Hermes chat first.

## Immediate blockers / user-provided inputs needed

None for the next design step: validate taxonomy/registry and build a dry-run evaluator before further live inbox triage.

Later inputs needed:

1. VIP senders/domains and known important service providers.
2. Preferred quiet hours/timezone if different from local defaults.
3. Yahoo IMAP app password/access details if Yahoo inbox support is still needed.
4. WhatsApp gateway route/target when ready to test phone alerts.