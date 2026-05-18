# Read-Only Agentic Workflow

Goal: define how scheduled and interactive agents should manage Gmail, Google Calendar, and later Yahoo Mail as a safe-first personal productivity system.

## Roles

- Hermes development partner: designs, implements, tests, and updates this system.
- Productivity agent: future scheduled/interactive worker that applies the workflow.
- User: confirms policies, resolves unknowns, and approves any mutation.

## Inputs

- Gmail read-only searches and message reads.
- Google Calendar read-only event lists.
- Later: Yahoo Mail read-only IMAP via Himalaya or equivalent.
- Project-local state files in `C:\hermes\PersonalProductivity`.

## State files

- `email-calendar-taxonomy.md` — controlled enum vocabulary.
- `sender-service-registry.csv` — machine-readable sender/domain/service defaults.
- `feedback-protocol.md` — how agents ask structured questions and apply answers.
- `email-calendar-alert-rules.md` — alert policy.
- `triage-evaluation-cases.jsonl` — examples with expected classification/action.
- `scripts/briefing_renderer.py` — compact read-only briefing renderer for Hermes chat now and WhatsApp later.
- `project-status.md` — project status and next safe actions.

Existing files such as `email-sender-classification-ledger.md`, `important-senders.md`, and `allowed-senders.md` are historical/scaffolding references. Prefer the structured registry for future agent behavior.

## Agent loop

1. Load taxonomy and registry.
2. Collect candidate items read-only:
   - unread/recent Gmail messages
   - upcoming Calendar events
   - later Yahoo messages
3. Normalize each item into a standard item record:
   - source_type
   - id/thread id/event id
   - sender/domain/organizer
   - subject/title
   - date/time
   - snippet/body summary
   - available evidence such as auth results or calendar metadata
4. Match sender/domain/service in registry.
5. Classify item using controlled enums:
   - trust_level
   - user_relationship
   - cost_status
   - message_category/event_category
   - urgency
   - disposition
   - action_policy
   - mutation_policy
   - confidence
6. Apply alert policy:
   - immediate alert only for configured high-signal cases
   - daily briefing for normal important items
   - weekly cleanup for low-priority/admin/noise review
   - suppress unless changed for resolved low-value items
7. Validate classification behavior with the local dry-run evaluator:
   - run `python scripts/triage_dry_run.py`
   - expected current result: all cases in `triage-evaluation-cases.jsonl` pass
   - use failures to update taxonomy, registry rows, or expected cases before using more live data
   - classify local read-only samples with `python scripts/triage_dry_run.py --gmail-json .tmp/daily_important_senders.json --calendar-json .tmp/daily_calendar_today.json --json`
   - sample classification output must remain local/read-only and must not include full Gmail body text in normalized items
8. Generate output with compact evidence:
   - what happened
   - why it matters or does not matter
   - confidence
   - suggested safe action
   - no action taken
   - render local sample classifications with `scripts/briefing_renderer.py` helpers; current preview artifact: `.tmp/daily_briefing_preview.txt`
   - output must stay phone-safe: no full private email bodies, no mutation claims, and uncertainty must be explicit
9. If classification is uncertain and useful, ask a structured feedback question.
10. Convert user feedback into registry updates and evaluation cases.
11. Never mutate external systems unless mutation_policy and explicit user approval permit it.

## Safe-first mutation rule

Disallowed by default:

- sending/replying to email
- deleting, archiving, labelling, filtering, marking read/unread
- clicking unsubscribe links
- creating/modifying/deleting calendar events
- creating/modifying/deleting todos
- cancelling accounts/subscriptions

Allowed by default:

- read-only searches
- read-only message/event inspection
- local project-file updates
- draft recommendations and proposed rules

## Scheduled jobs roadmap

Phase 1: manual dry run
- Run read-only collection manually.
- Classify with taxonomy.
- Compare against evaluation cases.
- Ask structured questions for unknowns.

Phase 2: daily briefing cron
- Run once per morning.
- Deliver to current Hermes chat first.
- No mutations.

Phase 3: urgent alert cron/poller
- Only high-confidence immediate items.
- Deliver to current Hermes chat first.
- Later WhatsApp.

Phase 4: weekly cleanup digest
- Noise candidates, historical free-tier accounts, paid-risk opportunities.
- No automated unsubscribe/filter/cancellation.

Phase 5: WhatsApp delivery
- Configure gateway delivery after output quality is acceptable.
