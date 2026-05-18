# AI Email, Calendar, and Todo Alert Agent Team Setup Plan

> **For Hermes:** This is a planning-only setup document. Do not implement until the user confirms the remaining setup choices and approves any account credentials, gateway configuration, cron jobs, or mail-modifying actions.

**Goal:** Set up an AI agent team that monitors important email and calendar events, sends timely alerts, and optionally maintains a todo list.

**Architecture:** Use Hermes Agent as the orchestrator with scheduled cron jobs for periodic scanning, Google Workspace OAuth for Gmail/Calendar access, and Hermes gateway delivery to WhatsApp as the preferred alert channel. Start with a conservative read-only workflow that summarizes and alerts; add todo extraction only after the alerting rules are reliable.

**Tech Stack:** Hermes Agent, Hermes cron jobs, Google Workspace skill/API scripts, Gmail API, Google Calendar API, optional Hermes todo/session memory, Hermes gateway with WhatsApp delivery preferred, and Telegram as a fallback/comparison option if WhatsApp proves unreliable or too constrained.

---

## Workspace

Use this workspace as the home for the personal productivity project:

- `C:\hermes\PersonalProductivity`
- MSYS/bash path: `/c/hermes/PersonalProductivity`

Plan files should live under:

- `C:\hermes\PersonalProductivity\.hermes\plans\`

This plan is saved at:

- `C:\hermes\PersonalProductivity\.hermes\plans\2026-05-16_231638-ai-email-calendar-alert-agent-team.md`

---

## Current Context / Assumptions

- The user wants proactive alerts for important emails and calendar events.
- The user has two main email accounts: one Gmail account and one Yahoo account.
- Gmail forwarding to Yahoo has now been turned off by the user. This should simplify the design by reducing duplicate messages, duplicate alerts, and forwarded-header ambiguity.
- Email/calendar provider for calendar is still assumed to be Google Workspace/Gmail because Hermes has a dedicated Google Workspace skill that supports Gmail and Calendar.
- Yahoo mail access should be handled separately, likely through IMAP using Himalaya or another mail client/API path.
- A major additional requirement is spam/unwanted-email management: identify repeat unwanted senders, attempt unsubscribe when safe, then delete/block/filter if unsubscribe fails.
- Another required feature is bulk cleanup: once unwanted senders are identified by `From` address, there may be large numbers of existing messages to remove. Cleanup must be conservative and reversible where possible so wanted emails are not accidentally removed.
- Important-email detection should combine explicit important-sender/source lists with smart classification. Examples of usually important sources include banks, appointments, HMRC/tax authority, government, legal, medical, insurance, utilities, travel, payments, security alerts, and account access messages. The system must also detect important messages that are not yet on the explicit list.
- WhatsApp is the user's preferred destination for alerts, daily updates, calendar reminders, and similar notifications. Telegram should only be recommended instead if testing shows WhatsApp is materially harder to set up, less reliable, more constrained, or unsuitable for the desired alert behavior.
- Gmail-native productivity features such as Priority Inbox, Multiple Inboxes, labels, categories, filters, stars, and importance markers may be useful. The project should evaluate whether to use these Gmail features directly, mirror Hermes classifications into Gmail labels, or keep Hermes classification separate at first.
- Google Workspace setup is not currently complete in this environment: `google_token.json` and `google_client_secret.json` are missing.
- The first version should be read-only: scan, classify, summarize, and alert. It should not send replies, create/delete calendar events, or modify emails without explicit user approval.
- Todo support should start as suggested tasks in alerts, not automatic persistent task mutation, until the user approves the workflow.
- Delivery channel preference is now chosen: use WhatsApp via Hermes gateway for alerts, daily updates, calendar reminders, and similar notifications. Use the current Hermes chat/origin only for early setup tests if WhatsApp is not ready yet. Keep Telegram as the main fallback candidate if WhatsApp integration is impractical.

## Decisions Already Made

- **Primary email/calendar path:** Gmail + Google Calendar through Google Workspace OAuth.
- **Secondary inbox:** Yahoo remains a separate email account, probably through IMAP/Himalaya.
- **Forwarding:** Gmail-to-Yahoo forwarding is off. Treat Gmail and Yahoo as separate inboxes; retain only light duplicate protection for old forwarded messages or rare overlap.
- **Primary notification channel:** WhatsApp via Hermes gateway.
- **Telegram:** Keep as a fallback only if WhatsApp proves unreliable, too constrained, or much harder to maintain.
- **Likely hosting location:** Prefer the VPS for the always-on production agent/gateway/cron scheduler after proving the workflow locally. Keep the laptop for setup, testing, plan editing, debugging, and any tasks that require local files or browser interaction.
- **Safety posture:** Start read-only. No email modification, deletion, unsubscribe, labels, filters, calendar edits, todo writes, or message sending except approved WhatsApp alert delivery.
- **Important-message strategy:** Use explicit rules plus smart classification so banks, HMRC/tax, appointments, medical/legal/insurance/utilities/travel/payment/security/account-access messages can be detected even if the sender is not yet listed.
- **Unwanted mail strategy:** Start with reports and previews. Unsubscribe/filter/block/delete only after explicit approval and evidence.

---

## Proposed Approach

Build this as a small multi-agent system made of scheduled Hermes jobs:

1. **Email triage agent**
   - Runs every 10-30 minutes during waking hours.
   - Searches Gmail and Yahoo for recent unread or high-signal messages.
   - Classifies messages as urgent, important, FYI, or ignorable using both explicit important-source lists and smart inference.
   - Sends an alert only for urgent/important items.

2. **Spam and unwanted sender agent**
   - Tracks repeat unwanted senders across Gmail and Yahoo.
   - Builds a reviewable sender list with status: candidate, unsubscribe attempted, unsubscribe failed, blocked/filtered, deleted, allowed.
   - Attempts unsubscribe only when it appears safe and legitimate.
   - If unsubscribe fails, recommends or applies filters/blocking/deletion according to user-approved rules.

3. **Bulk unwanted-email cleanup agent**
   - Finds existing messages from user-approved unwanted `From` addresses.
   - Produces a preview count and sample subjects before any removal.
   - Uses staged cleanup: label/move to quarantine or trash first, then permanent deletion only after a waiting period and explicit approval.
   - Protects wanted messages using allowlists, date ranges, folder restrictions, and sampling.

4. **Calendar sentinel agent**
   - Runs every 5-15 minutes.
   - Looks ahead at the next few hours and next day.
   - Alerts for upcoming meetings, conflicts, travel/location changes, and events needing preparation.

5. **Messaging delivery and channel monitor agent**
   - WhatsApp delivery is in scope for the first usable alerting version, because the user wants alerts, daily updates, and calendar reminders there.
   - Checks whether Hermes gateway can deliver outbound notifications to WhatsApp reliably.
   - Separately investigates whether WhatsApp/SMS message ingestion is feasible and safe; inbound message monitoring can remain a later phase if needed.
   - Applies the same important-message logic to non-email channels, especially official contacts, appointment messages, verification/security alerts, and urgent family/work messages.
   - Starts read-only and privacy-preserving; no auto-replies or message sending without explicit approval.

6. **Daily briefing agent**
   - Runs each morning.
   - Summarizes today’s calendar, important unread email, optional important WhatsApp/SMS messages, spam cleanup candidates, and suggested todos.

7. **Todo extraction agent**
   - Optional second phase.
   - Extracts action items from important emails and meetings.
   - Initially reports suggested todos for approval.
   - Later can write to a chosen todo system if desired.

8. **Rules/config layer**
   - Keep importance criteria explicit and easy to edit.
   - Examples: VIP senders, domains, banks, HMRC/tax authority, appointments, government, medical, legal, insurance, utilities, travel, security alerts, deadlines, calendar titles, ignored newsletters, blocked senders, safe unsubscribe rules, quiet hours.

9. **Gmail workflow integration layer**
   - Optional phase for using Gmail's built-in organization features.
   - Evaluates Priority Inbox, Multiple Inboxes, labels, filters, stars, categories, and Gmail's importance markers.
   - Starts by reading these signals, then optionally writes labels/filters only after approval.

10. **Deployment / hosting layer**
   - Local laptop is best for early setup, OAuth/browser steps, plan iteration, and debugging.
   - VPS is likely best for production because it can run Hermes gateway and cron continuously without depending on the laptop being awake, online, or unlocked.
   - Production should use one authoritative Hermes instance for scheduled jobs to avoid duplicate alerts.
   - Secrets/tokens must be managed carefully on the VPS because it will hold Gmail/Yahoo/WhatsApp credentials or OAuth tokens.

---

## Step-by-Step Plan

### Phase 1: Confirm Remaining Scope and Safety Rules

**Objective:** Confirm the unresolved setup details before touching credentials, gateway configuration, cron schedules, or any account-modifying actions.

**Remaining decisions needed:**
- Confirm Gmail/Google Workspace is the authoritative email/calendar provider for the first build.
- Yahoo access method: Yahoo IMAP app password, Yahoo web/API route if available, or manual export/forwarding during early testing.
- Confirm Gmail forwarding to Yahoo remains disabled before production automation starts, to avoid duplicate detection and alerts.
- Alert destination: WhatsApp via Hermes gateway is preferred. Current Hermes chat/origin may be used only for setup/debug tests; Telegram is the fallback/comparison option if WhatsApp proves impractical.
- Alert frequency: real-time-ish, hourly, morning/evening digest, or mixed.
- Quiet hours and timezone.
- Importance rules: VIP senders, work domains, family contacts, keywords, calendar event types.
- Important-source rules: banks, HMRC/tax authority, government services, appointments, medical, legal, insurance, utilities, travel, account/security alerts, payments, renewals, deadlines, and other personal high-value categories.
- Whether smart important-email selection should alert immediately, appear in daily briefing only, or ask for review when confidence is medium.
- Whether WhatsApp should be outbound-only at first for alerts/daily updates/calendar reminders, or also used later for inbound read-only message monitoring.
- Which phone/messaging channels are in scope: WhatsApp personal, WhatsApp Business, Android SMS, iPhone/iMessage/SMS, carrier SMS, or a third-party SMS service.
- Whether Gmail-native features should be used: Priority Inbox, Multiple Inboxes, labels, filters, stars, categories, and importance markers.
- Whether Hermes should only read Gmail's existing signals or eventually write labels/create filters to make Gmail itself more organized.
- Whether the assistant may mark emails read, add labels, create todos, or remain read-only.
- What actions are allowed for unwanted mail: unsubscribe only, move to spam, delete, create filters, block senders, or only suggest actions.
- What bulk cleanup actions are allowed for already-existing unwanted mail: report only, move to quarantine folder/label, move to trash, or permanently delete after review.

**Recommended default:**
- Gmail + Google Calendar.
- Yahoo email via IMAP/Himalaya as a second email account.
- Treat Gmail and Yahoo as separate inboxes now that Gmail-to-Yahoo forwarding is disabled; keep only lightweight deduplication as a safety net for old forwarded messages and any overlap during the transition.
- WhatsApp delivery first once Hermes gateway is configured; current Hermes chat/origin only for early setup/debug tests.
- Read-only operation.
- Email scan every 15 minutes.
- Maintain `important-senders.md` and `important-categories.md`, but allow smart classification to surface important messages not yet listed.
- Smart important-email matches should include a confidence level and reason before becoming immediate alerts.
- WhatsApp notification delivery is part of the baseline user experience. WhatsApp/SMS inbound message monitoring is still a later feasibility phase, because setup may depend on the user's phone platform and available gateway adapters.
- Gmail-native feature integration is also a later phase: first inspect/read Gmail labels/categories/importance markers, then optionally create a Hermes label scheme and filters after approval.
- Spam/unwanted sender report daily at first, not immediate deletion.
- Bulk cleanup starts in preview-only mode, then quarantine/trash mode, with permanent deletion disabled until explicitly approved.
- Calendar scan every 10 minutes.
- Morning briefing at 08:00 local time.
- No automatic email/calendar/todo mutations.

---

### Phase 2: Set Up Google Workspace OAuth

**Objective:** Authorize Hermes to read Gmail and Calendar.

**Relevant Hermes skill:** `google-workspace`

**Files likely involved:**
- `~/.hermes/google_client_secret.json`
- `~/.hermes/google_token.json`
- `~/.hermes/google_oauth_pending.json` temporary during setup
- `~/.hermes/google_oauth_last_url.txt` temporary/helper file

**Setup steps:**
1. Ask which services are needed. For this use case, use `email,calendar` only.
2. Ask whether the Google account uses Advanced Protection.
3. Create/select a Google Cloud project.
4. Enable these APIs:
   - Gmail API
   - Google Calendar API
5. Create an OAuth 2.0 Desktop App client.
6. Download the OAuth JSON file.
7. Run the Google Workspace setup script with the downloaded client secret.
8. Generate the auth URL for `email,calendar` scopes.
9. User authorizes in browser and pastes back the redirected localhost URL/code.
10. Exchange the code and verify authentication.

**Verification:**
- `setup.py --check` should report authenticated.
- A Gmail search command should return JSON, even if empty.
- A Calendar list command should return JSON, even if empty.

**Risk:** Google OAuth setup is the highest-friction step. If the user only wanted email and no calendar, the `himalaya` IMAP workflow may be simpler, but for email + calendar the Google Workspace OAuth path is the right default.

---

### Phase 2B: Set Up Yahoo Mail Access and Lightweight Deduplication Policy

**Objective:** Add Yahoo as a first-class inbox while avoiding duplicate alerts from historical Gmail-forwarded messages or any rare overlap.

**Relevant Hermes skill:** `himalaya`

**Recommended access path:**
- Use Yahoo IMAP with an app password if Yahoo account security requires it.
- Configure Himalaya with two accounts if both Gmail and Yahoo are accessed through IMAP, or use Google Workspace for Gmail and Himalaya only for Yahoo.

**Files likely involved:**
- `~/.config/himalaya/config.toml`
- System keyring/pass entry for Yahoo app password, if used
- Optional project note: `C:\hermes\PersonalProductivity\email-accounts.md`

**Setup steps:**
1. Record that Gmail-to-Yahoo forwarding is now disabled.
2. Set up Yahoo IMAP access through Himalaya.
3. Verify Yahoo folder list and inbox listing.
4. Confirm delete/spam/block/filter capabilities available through Yahoo IMAP or Yahoo web settings, but keep all write/destructive actions disabled initially.
5. Keep a lightweight duplicate check for old forwarded Gmail messages that already exist in Yahoo.

**Deduplication rule:**
- Prefer the original Gmail message when the same message appears in both Gmail and Yahoo due to historical forwarding or overlap.
- Use message IDs, subject/date/from similarity, and forwarding headers where available.
- Never alert twice for the same underlying message.

**Verification:**
- Yahoo inbox listing returns structured output.
- Any historical forwarded Gmail message is recognized as duplicate or forwarded.
- A Yahoo-native message is preserved as its own candidate.

---

### Phase 3: Define Alert Rules

**Objective:** Avoid noisy or creepy alerts by making importance criteria explicit.

**Suggested file:**
- `C:\hermes\PersonalProductivity\email-calendar-alert-rules.md`

**Initial rules template:**

```markdown
# Email and Calendar Alert Rules

## VIP senders
- boss@example.com
- client-domain.com

## Important message signals
- Directly addressed to me
- From VIP sender/domain/contact
- From known important source list: banks, HMRC/tax authority, government, medical, legal, insurance, utilities, travel, school/appointments, payment processors, account/security systems
- Smart inferred important category even when sender/contact is not yet listed
- Contains deadline, urgent, action required, invoice, contract, outage, incident, interview, travel, meeting change
- Contains tax, pension, mortgage, credit card, bank account, payment failed, refund, renewal, appointment, prescription, results, fine, penalty, verification, security alert, login, password reset
- Has an attachment from a VIP or important source
- Is a reply in an active thread I recently participated in
- For WhatsApp/SMS: official appointment reminders, bank/security/payment messages, government/tax messages, verification codes, urgent family/work messages, and messages from approved important contacts

## Smart importance scoring
- High confidence: known important sender/source, or strong category evidence such as bank/HMRC/medical/security/deadline/account access.
- Medium confidence: possibly important category or unfamiliar sender with high-signal wording; include in briefing or ask for review.
- Low confidence: promotional or generic message with weak signals; do not interrupt.
- Always include reason and confidence in alerts.
- When the system finds a genuinely important sender not on the list, propose adding it to `important-senders.md`.
- When the system finds a new important category/pattern, propose adding it to `important-categories.md`.

## Suppress / low priority
- Newsletters
- Promotions
- Automated notifications unless they contain failure, outage, payment, security, or deadline terms

## Calendar alert rules
- Alert 30 minutes before meetings by default
- Alert earlier for meetings with location/travel
- Alert for conflicts or overlapping events
- Alert for calendar changes/cancellations
- Include preparation notes if event title/description indicates review, interview, demo, presentation, or deadline

## Quiet hours
- Default: 22:00-07:00 local time
- Exceptions: urgent/security/travel/family/VIP only

## Unwanted sender handling
- Maintain an allowlist for legitimate senders that must never be deleted or blocked.
- Maintain a candidate spam/unwanted sender list with evidence: sender, domain, subject examples, count, last seen, account, folder.
- Try unsubscribe only when the link appears legitimate and low-risk.
- Do not click suspicious unsubscribe links from obvious scams/phishing.
- If unsubscribe does not stop messages after a waiting period, recommend blocking/filtering/deleting.
- Prefer provider-side filters over ad hoc deletion so the rule remains durable.
- Never auto-delete messages from uncertain senders without user approval during the first phase.
- Bulk cleanup must never operate on a domain-wide match until exact sender-address cleanup has been tested.
- Before removing old messages, produce a preview with total count, folders affected, oldest/newest dates, and representative subject samples.
- Prefer reversible actions first: Gmail label/quarantine or move to trash; Yahoo move to a cleanup/quarantine folder or trash if available.
- Permanent deletion requires a separate explicit approval after review.
```

**Verification:**
- User confirms the rules are acceptable.
- Jobs reference the same rules in their prompts.

---

### Phase 4: Create the Email Triage Cron Job

**Objective:** Periodically scan recent email and alert only when something is worth interrupting the user.

**Hermes feature:** `cronjob` / `hermes cron create`

**Suggested schedule:**
- Every 15 minutes during work hours, or every 30 minutes all day with quiet-hour suppression.

**Self-contained job prompt outline:**

```text
You are the user's email triage agent.

Use Google Workspace/Gmail read-only access and Yahoo read-only access.
Look for recent unread or newly arrived messages since the last scan, focusing on the last 30-60 minutes.
Classify each candidate as urgent, important, FYI, or ignore using both explicit lists and smart inference.
Explicit lists include important senders/domains and important categories such as banks, HMRC/tax authority, government, appointments, medical, legal, insurance, utilities, travel, payments, renewals, and account/security alerts.
Smart inference should catch important messages from senders not yet listed when the content/category strongly suggests financial, tax, legal, medical, appointment, security, account access, deadline, or payment relevance.
Alert immediately for high-confidence urgent/important messages.
For medium-confidence messages, include in the daily briefing or ask the user whether this sender/category should be added to the important list.
Do not alert for generic promotions that merely mention important-sounding words unless the sender/context supports it.
Alert only for urgent or important messages.
Do not send email, modify labels, mark read, archive, delete, or reply.
Include account, sender, subject, received time, importance confidence, why it matters, and recommended next action.
If a not-yet-listed sender/category is important, propose adding it to important-senders.md or important-categories.md.
If nothing important is found, stay silent or return a short 'nothing important' depending on delivery preference.
Apply the user's alert rules and quiet hours.
```

**Likely Gmail queries:**
- `newer_than:1h is:unread`
- `newer_than:1d is:unread -category:promotions -category:social`
- VIP/domain-specific queries once rules are known.
- Important source/category queries such as bank, HMRC, tax, appointment, renewal, payment, security alert, login, verification, mortgage, insurance, utility, travel.

**Suggested files:**
- `C:\hermes\PersonalProductivity\important-senders.md`
- `C:\hermes\PersonalProductivity\important-categories.md`
- `C:\hermes\PersonalProductivity\important-email-review.md`
- `C:\hermes\PersonalProductivity\important-contacts.md`
- `C:\hermes\PersonalProductivity\messaging-integration-notes.md`

**Important sender/category list format:**

```markdown
# Important Senders

| sender_or_domain | category | confidence | action | notes |
|---|---|---|---|---|
| alerts.mybank.example | bank | high | immediate alert | account/security/payment messages |
| hmrc.gov.uk | tax authority | high | immediate alert | UK tax messages |

# Important Categories

| category | signals | default_action | notes |
|---|---|---|---|
| bank/security | login, verification, suspicious activity, card, account, payment | immediate alert | suppress obvious marketing |
| appointments | appointment, booking, reminder, cancellation, reschedule | immediate alert | include date/time if found |
| tax/HMRC | HMRC, tax, self assessment, payment, notice, code | immediate alert | verify sender carefully |
```

**Smart selection rules:**
- Explicit important sender/domain beats general classification, unless the message is clearly marketing.
- Important category + credible sender/context should be high confidence.
- Important wording from a random promotional sender should not automatically alert.
- Medium-confidence messages should be batched for review and list-building.
- The system should learn from user feedback by proposing additions to important lists, not silently changing behavior at first.

**Validation:**
- Run once manually.
- Confirm it does not over-alert.
- Confirm it includes enough context without dumping full private email content unnecessarily.
- Confirm it never performs write actions.
- Confirm obvious important messages from known sources are classified high confidence.
- Confirm important-looking marketing/promotional messages are not over-classified.
- Confirm at least some not-yet-listed important senders/categories are surfaced as review suggestions rather than missed.
- Confirm every alert includes importance confidence and reason.

---

### Phase 4B: Create the Spam and Unwanted Sender Management Workflow

**Objective:** Reduce recurring unwanted email safely, without accidentally interacting with scams or deleting wanted mail.

**Suggested schedule:**
- Daily report for the first 1-2 weeks.
- After rules are trusted, optionally run automated provider-side filter checks weekly.

**Suggested files:**
- `C:\hermes\PersonalProductivity\unwanted-senders.md`
- `C:\hermes\PersonalProductivity\allowed-senders.md`
- `C:\hermes\PersonalProductivity\spam-actions-log.md`

**Sender list schema:**

```markdown
# Unwanted Senders

| sender | domain | account | status | evidence | first_seen | last_seen | count | action | notes |
|---|---|---|---|---|---|---|---:|---|---|
| offers@example.com | example.com | yahoo | candidate | 5 promos in 7 days | 2026-05-01 | 2026-05-16 | 5 | review | possible unsubscribe |
```

**Statuses:**
- `candidate` — suspected unwanted sender, needs review.
- `unsubscribe-safe` — unsubscribe appears legitimate and can be attempted with approval.
- `unsubscribe-attempted` — unsubscribe was attempted; monitor for recurrence.
- `unsubscribe-failed` — messages continued after waiting period.
- `filter-recommended` — create provider-side rule/filter/block.
- `blocked-or-filtered` — provider-side rule is active.
- `delete-recommended` — safe to delete future messages matching exact criteria.
- `allowed` — sender/domain should not be treated as spam.

**Self-contained job prompt outline:**

```text
You are the user's unwanted-email management agent.

Scan Gmail and Yahoo for repeated unwanted senders, newsletters, promotions, and spam-like messages.
Build or update a sender list with evidence: sender, domain, account, subject examples, count, first seen, last seen, and recommended action.
Do not click unsubscribe links from suspicious/phishing messages.
For legitimate commercial/newsletter messages, recommend unsubscribe first.
If unsubscribe was already attempted and messages continue after the waiting period, recommend provider-side filtering/blocking or deletion.
Do not delete, block, filter, mark spam, or click unsubscribe unless the user has explicitly approved that category of action.
Protect allowed/VIP senders from deletion or blocking.
```

**Safe unsubscribe policy:**
- Prefer standards-based `List-Unsubscribe` headers when available.
- Prefer unsubscribe links from known legitimate senders over arbitrary links in suspicious messages.
- Do not unsubscribe from obvious scams, phishing, extortion, malware, or random spoofed senders; blocking/filtering is safer.
- Log every unsubscribe attempt and monitor whether messages continue.

**Escalation policy:**
1. Candidate identified.
2. User approves sender/domain as unwanted.
3. If legitimate sender: attempt unsubscribe.
4. Monitor for 7-14 days.
5. If still sending: create filter/block/delete rule.
6. If scam/phishing: skip unsubscribe; recommend spam/block/filter immediately.

**Validation:**
- Manual dry run produces a review list without modifying mail.
- Known legitimate senders are not included if allowlisted.
- Repeated unwanted senders are grouped by domain/sender.
- Confirm old Gmail-forwarded-to-Yahoo messages are not double-counted if encountered.
- No unsubscribe/block/delete action happens without approval.

---

### Phase 4C: Create the Bulk Cleanup Workflow for Existing Unwanted Mail

**Objective:** Safely remove large volumes of already-existing unwanted emails from approved `From` addresses without deleting wanted mail.

**Default mode:** Preview-only.

**Cleanup principle:** Exact sender first, reversible action first, permanent deletion last.

**Suggested files:**
- `C:\hermes\PersonalProductivity\cleanup-candidates.md`
- `C:\hermes\PersonalProductivity\cleanup-approvals.md`
- `C:\hermes\PersonalProductivity\cleanup-actions-log.md`

**Bulk cleanup stages:**

1. **Identify exact sender address**
   - Use the full normalized `From` email address, not only display name.
   - Avoid broad domain matching unless separately approved.
   - Treat lookalike domains and spoofed names as separate senders.

2. **Preview matching messages**
   - Count messages by account and folder/label.
   - Show oldest/newest dates.
   - Show 10-25 representative subject lines and snippets.
   - Show whether messages include replies, attachments, starred/flagged states, or user-sent thread participation.

3. **Safety exclusions**
   - Exclude starred/flagged/important messages by default.
   - Exclude messages in Sent, Drafts, Archive-only business folders, or custom protected folders unless approved.
   - Exclude threads where the user replied, unless approved.
   - Exclude messages with attachments until sampled and approved.
   - Exclude senders/domains listed in `allowed-senders.md`.

4. **User approval checkpoint**
   - Present exact sender, count, folders, samples, exclusions, and proposed action.
   - Require explicit approval per sender or per batch.

5. **Quarantine/trash first**
   - Gmail: prefer applying a label such as `Hermes/UnwantedCleanup` and/or moving to Trash after approval.
   - Yahoo: prefer moving to a cleanup/quarantine folder or Trash if supported through IMAP.
   - Keep an action log with message IDs where available.

6. **Monitor and undo window**
   - Wait 7-30 days before permanent deletion.
   - Provide a recovery path from label/quarantine/trash.
   - Only permanently delete after a second explicit approval.

**Self-contained job prompt outline:**

```text
You are the user's bulk unwanted-email cleanup agent.

Use only user-approved unwanted sender addresses from unwanted-senders.md or cleanup-approvals.md.
For each exact From address, find existing matching messages in Gmail and Yahoo.
Do not use broad domain matching unless the user explicitly approved the domain.
Produce a cleanup preview: account, folder/label, count, oldest/newest date, sample subjects, and safety exclusions.
Exclude starred/flagged/important messages, user-replied threads, messages with attachments, protected folders, and allowlisted senders by default.
Do not delete, trash, move, label, or permanently remove anything unless the user explicitly approved the exact action.
Prefer quarantine/label/trash before permanent deletion.
Log every approved action with sender, query, count, date, account, folder, and message IDs if available.
```

**Validation:**
- Preview mode returns counts and samples without modifying mail.
- The same sender in Gmail and Yahoo is reported separately by account.
- Historical Gmail-forwarded-to-Yahoo duplicates are not double-counted if encountered.
- Safety exclusions reduce the candidate count and are shown to the user.
- A test cleanup uses a tiny approved sample before any large batch.
- Recovery from quarantine/trash is verified before enabling larger cleanup.

---

### Phase 5: Create the Calendar Sentinel Cron Job

**Objective:** Alert the user about upcoming events, changes, conflicts, and prep needs.

**Suggested schedule:**
- Every 10 minutes for next-2-hour alerts.
- Optional daily lookahead once in the evening for tomorrow.

**Self-contained job prompt outline:**

```text
You are the user's calendar sentinel.

Use Google Calendar read-only access.
Check events starting in the next 2 hours and events changed recently.
Alert for upcoming meetings, conflicts, cancellations, location/video-link changes, and prep-heavy events.
For each alert, include title, start time, location/link if present, attendees if useful, and suggested preparation.
Do not create, delete, edit, accept, or decline calendar events.
Apply quiet hours, but allow urgent/travel/conflict alerts.
```

**Validation:**
- Run once manually.
- Confirm timezone handling is correct.
- Confirm recurring events are not repeatedly alerted every run unless a new threshold is crossed.
- Confirm conflicts are detected correctly.

---

### Phase 5B: Configure WhatsApp Delivery, Then Investigate WhatsApp/SMS Inbound Monitoring

**Objective:** Use WhatsApp as the preferred destination for alerts, daily updates, and calendar reminders; separately determine whether official/important inbound WhatsApp and SMS messages can be included safely and reliably.

**Status:** WhatsApp outbound delivery is a baseline requirement for the first useful alerting version. Inbound WhatsApp/SMS monitoring remains a later feasibility phase.

**Why WhatsApp first:**
- The user explicitly prefers WhatsApp for alerts, daily updates, calendar reminders, and similar notifications.
- WhatsApp is likely to be noticed faster than email or a terminal chat.
- Hermes gateway supports WhatsApp as a platform, so it is a reasonable first-class target.

**When Telegram might be better:**
- Telegram bot setup is often simpler and more automation-friendly than WhatsApp personal-account integration.
- Telegram tends to be easier for bot-style commands, test notifications, group/channel routing, and low-friction debugging.
- WhatsApp may have stricter platform/account constraints depending on the adapter, account type, and whether this is personal WhatsApp or WhatsApp Business/API.
- Therefore Telegram should be kept as the fallback if WhatsApp setup is unreliable, restricted, slow to approve, or unsuitable for recurring automated alerts.

**Outbound alert delivery requirements:**
- Send urgent/important email alerts to WhatsApp.
- Send calendar reminders to WhatsApp.
- Send daily briefing/update to WhatsApp.
- Respect quiet hours and escalation exceptions.
- Avoid duplicate WhatsApp notifications for the same email/event/message.
- Include concise context and a recommended action; avoid long unreadable blocks.

**Potential integration paths:**
- Hermes gateway supports WhatsApp, Telegram, SMS, and other platforms, but setup depends on the available adapter, credentials, and phone/account constraints.
- WhatsApp personal accounts may be harder to integrate reliably than WhatsApp Business/API-style integrations.
- SMS integration depends heavily on phone platform:
  - Android may allow SMS forwarding/automation through companion apps or gateway integrations.
  - iPhone SMS/iMessage is usually more restrictive; BlueBubbles/iMessage-style routes may help for iMessage but not always carrier SMS.
  - Third-party SMS services are better for owned numbers, but may not read personal phone inboxes.

**Recommended first step:**
- Configure/test outbound WhatsApp notification delivery first.
- Send a small manual test alert, a sample daily briefing, and a sample calendar reminder to WhatsApp before enabling cron jobs.
- Treat inbound WhatsApp/SMS message monitoring as read-only message ingestion or manual export/forwarding until the integration path is proven.
- Start with a small `important-contacts.md` list for official contacts and key people.
- Do not auto-reply or send WhatsApp/SMS messages without explicit approval.

**Smart selection for WhatsApp/SMS:**
- High confidence: appointment reminders, bank/security/payment notices, government/tax notices, verification/account access messages, urgent messages from known important contacts.
- Medium confidence: unknown contact with official-sounding content; include in review/briefing.
- Low confidence: generic promotional broadcast or unknown sender without action/deadline/security content.

**Suggested files:**
- `C:\hermes\PersonalProductivity\important-contacts.md`
- `C:\hermes\PersonalProductivity\messaging-integration-notes.md`
- `C:\hermes\PersonalProductivity\whatsapp-alert-format.md`
- `C:\hermes\PersonalProductivity\important-message-review.md`

**Validation:**
- Confirm a test Hermes gateway notification arrives in WhatsApp.
- Confirm a sample daily briefing is readable in WhatsApp.
- Confirm a sample calendar reminder arrives at the right time and is not duplicated.
- Confirm Telegram is only needed as a fallback if WhatsApp is unreliable or impractical.
- Confirm the selected integration can read messages without breaking WhatsApp/SMS account terms or reliability.
- Confirm private message content is only processed with user consent.
- Confirm high-confidence messages are surfaced with contact, channel, timestamp, reason, and recommended next action.
- Confirm no messages are sent automatically.

---

### Phase 5C: Evaluate Gmail Native Workflow Features

**Objective:** Decide how to incorporate Gmail's built-in productivity features without overcomplicating or prematurely modifying the mailbox.

**Status:** Later phase after baseline Gmail access and read-only triage work.

**Useful Gmail features to evaluate:**
- **Priority Inbox:** Gmail's own importance model may provide useful signal for the Hermes triage agent.
- **Multiple Inboxes:** Could provide user-visible panes such as Important, Awaiting Reply, Appointments, Finance/Tax, and Cleanup Candidates.
- **Labels:** Could mirror Hermes classifications, e.g. `Hermes/Important`, `Hermes/Review`, `Hermes/Finance`, `Hermes/Appointments`, `Hermes/UnwantedCandidate`, `Hermes/CleanupQuarantine`.
- **Filters:** Could automatically label or route known important/unwanted senders after rules are trusted.
- **Stars / importance markers:** Could be read as user feedback; optionally applied later only with approval.
- **Categories:** Gmail's Promotions/Social/Updates/Forums/Primary categories can help suppress noise and find official updates.

**Recommended approach:**
1. Read existing Gmail labels, categories, stars, and importance markers.
2. Compare Gmail's Priority Inbox/importance signals against Hermes smart classification.
3. Keep Hermes classification separate initially; do not change Gmail UI or labels during early tests.
4. If useful, design a small Gmail label scheme under a `Hermes/` prefix.
5. Add labels only after explicit approval.
6. Create filters only after labels have proven useful and false positives are low.
7. Keep Gmail Multiple Inboxes as a user-facing optional UI setup, not a required automation dependency.

**Possible label scheme:**
```text
Hermes/Important
Hermes/Review
Hermes/FinanceTax
Hermes/Appointments
Hermes/Security
Hermes/Travel
Hermes/TodoCandidate
Hermes/UnwantedCandidate
Hermes/CleanupQuarantine
```

**Gmail search examples that may support Multiple Inboxes:**
- `label:Hermes/Important newer_than:30d`
- `label:Hermes/Review`
- `label:Hermes/FinanceTax newer_than:90d`
- `label:Hermes/Appointments newer_than:30d`
- `label:Hermes/UnwantedCandidate`
- `label:Hermes/CleanupQuarantine`

**Validation:**
- Gmail's native importance/categorization is compared with Hermes classification on a sample set.
- Labels are only proposed, not created, in the first pass.
- If labels are created later, they use a clear `Hermes/` prefix and can be removed cleanly.
- Filters are not created until label behavior is verified.
- Multiple Inboxes setup remains optional and user-controlled.

---

### Phase 6: Create the Daily Briefing Job

**Objective:** Provide a compact morning plan combining calendar, important email, and suggested todos.

**Suggested schedule:**
- Every day at 08:00 local time.

**Self-contained job prompt outline:**

```text
You are the user's daily briefing agent.

Summarize today's calendar, important unread emails, optional important WhatsApp/SMS messages if integration is enabled, deadlines, and suggested todos.
Group output into:
1. Must know today
2. Calendar timeline
3. Important email needing action
4. Important WhatsApp/SMS messages needing action, if available
5. Suggested todos
6. Watchlist / waiting-on
Do not modify email, calendar, messaging, or todo systems.
Keep the briefing concise and actionable.
```

**Validation:**
- Run once manually before enabling recurrence.
- Confirm the briefing format works well in WhatsApp.
- Confirm suggested todos are useful and not hallucinated.

---

### Phase 7: Add Todo Workflow, Initially Read-Only/Suggested

**Objective:** Identify action items without risking unwanted task-list changes.

**Options:**
1. Keep todos as suggested items in alerts and daily briefings.
2. Use Hermes session todo only for the current session.
3. Integrate with an external todo system later, such as Google Tasks, Todoist, Notion, Linear, Obsidian, or a markdown file.

**Recommended first version:**
- Suggested todos only.
- User can approve adding them later.

**Suggested todo extraction criteria:**
- Explicit asks: “Can you…”, “Please…”, “Need you to…”
- Deadlines: “by Friday”, “before the meeting”, “due today”
- Calendar prep: “review deck”, “prepare agenda”, “bring…”
- Follow-ups: “waiting on X”, “reply to Y”

**Validation:**
- Compare extracted todos against a few real emails/events.
- Check false positives.
- Only then decide whether to persist todos automatically.

---

### Phase 8: Configure WhatsApp Delivery Channel

**Objective:** Make alerts land where the user will notice them.

**Default:** WhatsApp via Hermes gateway.

**Temporary setup/debug fallback:** Current Hermes conversation/origin delivery.

**Fallback/comparison option:**
- Telegram via Hermes gateway, but only if WhatsApp proves materially worse for setup, reliability, recurring notifications, or bot-style interaction.

**Other later options:**
- Discord DM/channel via Hermes gateway.
- Slack DM/channel via Hermes gateway.
- Email delivery.
- SMS if configured.

**Hermes commands likely involved if gateway delivery is desired:**
- `hermes gateway setup`
- `hermes gateway run`
- `hermes gateway install`
- `hermes gateway start`
- `/sethome` from the target chat/channel, if supported by the platform.

**Validation:**
- Send a test cron notification to WhatsApp.
- Confirm delivery appears in WhatsApp.
- Confirm daily briefing and calendar reminder formatting are readable on a phone screen.
- Confirm notifications are not duplicated across channels unless explicitly desired.

---

### Phase 9: Decide Production Hosting Location

**Objective:** Choose where the always-on Hermes gateway and scheduled productivity agents should run.

**Recommended direction:**
- Prove the workflow locally first.
- Move production cron jobs and WhatsApp gateway delivery to the VPS once authentication and alert formatting work.
- Keep the laptop as the operator/development machine for editing rules, reviewing logs, and making approved changes.

**Why VPS is probably better for production:**
- Always-on availability for calendar reminders, email scans, and daily briefings.
- Does not depend on the laptop being powered on, awake, connected, or not rebooting.
- Better fit for Hermes gateway service mode and scheduled cron jobs.
- Cleaner separation between personal laptop use and background automation.

**Why local laptop is still useful:**
- Easier for browser-based OAuth setup and interactive debugging.
- Lower initial friction while designing prompts and rules.
- Useful for inspecting or editing project files in `C:\hermes\PersonalProductivity`.
- Avoids copying credentials to the VPS until the workflow is proven.

**Important deployment rules:**
- Do not run the same cron jobs on both laptop and VPS in production, or alerts may duplicate.
- Pick one authoritative scheduler. If production moves to the VPS, disable/pause local cron jobs.
- Store credentials/tokens only on the machine that needs them.
- Lock down VPS access, file permissions, updates, backups, and logs because it will process private email/calendar data.
- Keep project rules/config in a portable workspace that can be copied or synced deliberately between laptop and VPS.

**Validation before cutover:**
- VPS `hermes doctor` is clean.
- VPS gateway can start/restart as a service.
- VPS can send a test WhatsApp notification.
- VPS can run a manual Gmail/Calendar read-only check.
- VPS cron scheduler can run one dry-run job without duplicate local alerts.
- Local cron jobs are paused or absent before enabling VPS production schedules.

---

## Additional Opportunities / Capabilities Not Yet Raised

These are not required for the first version, but they are worth considering during planning so the architecture does not accidentally block them later.

### 1. Waiting-on and follow-up tracking

**Capability:** Detect messages where the user is waiting for someone else, or where someone is waiting for the user.

**Examples:**
- "I will send this by Friday" from another person becomes a waiting-on item.
- "Can you send me..." becomes a reply/action candidate.
- No response after N days becomes a gentle follow-up reminder.

**Why useful:** This turns the system from an alert bot into a lightweight executive assistant.

**Recommended phase:** After read-only email triage works.

**Suggested file:**
- `C:\hermes\PersonalProductivity\waiting-on.md`

### 2. Deadline and renewal tracker

**Capability:** Extract due dates, renewal dates, cancellation windows, payment dates, insurance renewals, tax deadlines, subscription changes, appointment dates, and travel dates from emails/calendar events.

**Why useful:** Important emails often matter because of a date. Tracking dates separately can prevent missed renewals, penalties, and forgotten admin tasks.

**Recommended phase:** After daily briefing and todo suggestions are reliable.

**Suggested file:**
- `C:\hermes\PersonalProductivity\deadline-tracker.md`

### 3. Bill, payment, refund, and finance watchlist

**Capability:** Identify bills, invoices, payment failures, card expiry notices, refunds, chargebacks, bank/security alerts, suspicious activity, and unusual financial admin emails.

**Why useful:** These are high-impact categories where missing a message can be costly.

**Safety note:** Start with alerts only. Do not connect bank APIs, make payments, or click payment links.

**Suggested file:**
- `C:\hermes\PersonalProductivity\finance-watchlist.md`

### 4. Document and attachment intelligence

**Capability:** Detect and summarize important attachments such as PDFs, invoices, booking confirmations, letters, medical documents, statements, tickets, contracts, and forms.

**Why useful:** Some important information is inside attachments rather than the email body.

**Safety note:** Attachment processing should be read-only and should avoid executing or trusting active content. For scans/PDFs, use OCR/document extraction only when approved.

**Suggested file:**
- `C:\hermes\PersonalProductivity\document-review.md`

### 5. Appointment and travel preparation assistant

**Capability:** For upcoming appointments/trips/meetings, collect related emails, attachments, addresses, links, booking references, travel time, and prep notes into a concise reminder.

**Examples:**
- Appointment tomorrow: include location, booking reference, documents to bring, and travel buffer.
- Flight/train/hotel: include departure time, check-in status, reference, and disruption watch.

**Recommended phase:** After calendar sentinel is reliable.

### 6. Contact and organization intelligence

**Capability:** Build a private contact/org map from email/calendar history: important people, companies, service providers, recurring appointment sources, account managers, and domains.

**Why useful:** Helps classify unknown messages correctly and reduces manual rule maintenance.

**Safety note:** Keep this local/project-private and reviewable. Do not upload broad contact lists unnecessarily.

**Suggested files:**
- `C:\hermes\PersonalProductivity\important-contacts.md`
- `C:\hermes\PersonalProductivity\organization-map.md`

### 7. Digest tiers and notification modes

**Capability:** Support multiple alert modes instead of one all-or-nothing notification policy.

**Possible tiers:**
- Immediate interruption: urgent/security/calendar/travel/VIP.
- Same-day digest: important but non-urgent.
- Weekly review: newsletters, account statements, cleanup candidates.
- Silent log: low-confidence or already-handled items.

**Why useful:** Prevents notification fatigue while preserving visibility.

### 8. Feedback loop / personal learning

**Capability:** Let the user correct classifications: "this is important", "never alert me about this", "this sender is safe", "add to cleanup", "only include in daily digest".

**Why useful:** The system will improve quickly if feedback updates explicit project files rather than relying only on model judgment.

**Suggested files:**
- `C:\hermes\PersonalProductivity\classification-feedback.md`
- Updates to `important-senders.md`, `important-categories.md`, `allowed-senders.md`, and `unwanted-senders.md` after approval.

### 9. Alert action buttons / command shortcuts

**Capability:** If the delivery channel supports it, alerts could include quick reply commands such as:
- `snooze 2h`
- `add to important`
- `mark as unwanted candidate`
- `include in daily briefing only`
- `create todo draft`
- `stop alerts from this sender`

**Why useful:** Makes the system easier to tune from WhatsApp/Telegram without opening the workspace.

**Safety note:** Destructive commands still require confirmation and logging.

### 10. Personal knowledge base / reference memory

**Capability:** Save durable reference notes from important admin emails, such as account numbers, policy renewal dates, provider contact details, recurring appointment instructions, and household/vendor information.

**Why useful:** The assistant can answer "when does this renew?", "who do I contact?", or "what was the reference number?" without searching the inbox every time.

**Safety note:** Avoid storing secrets, passwords, full financial details, or unnecessary sensitive medical/legal content.

**Suggested file:**
- `C:\hermes\PersonalProductivity\personal-admin-reference.md`

### 11. Weekly review and cleanup briefing

**Capability:** A weekly review that summarizes:
- unresolved important emails
- waiting-on items
- upcoming deadlines/renewals
- unused cleanup candidates
- medium-confidence classification decisions needing user feedback
- noisy senders that may need rules

**Why useful:** Daily alerts handle urgency; weekly review handles maintenance and gradual improvement.

### 12. Failure monitoring and health checks

**Capability:** Alert if the automation itself stops working.

**Examples:**
- Gmail OAuth token expired.
- Yahoo IMAP auth failed.
- WhatsApp delivery failed.
- VPS cron did not run.
- Gateway is down.
- Duplicate scheduler detected on laptop and VPS.

**Why useful:** A silent personal assistant failure is worse than an obvious one.

**Suggested file:**
- `C:\hermes\PersonalProductivity\agent-health-log.md`

### 13. Privacy, retention, and audit policy

**Capability:** Decide what summaries/logs are kept, for how long, and where.

**Why useful:** The project will process private email/calendar/message data. A simple retention policy avoids accumulating unnecessary sensitive logs.

**Suggested file:**
- `C:\hermes\PersonalProductivity\privacy-retention-policy.md`

### 14. Vacation / away mode

**Capability:** Temporarily alter alert thresholds and daily briefing behavior when travelling, on holiday, sick, or intentionally offline.

**Examples:**
- More travel/calendar alerts while travelling.
- Fewer work alerts during holiday.
- Escalate only family/security/banking.

**Recommended phase:** Later, after baseline alerting works.

### 15. Cross-channel duplicate and escalation policy

**Capability:** If the same event appears through email, calendar, WhatsApp/SMS, and possibly app notifications, merge it into one coherent alert.

**Example:** A medical appointment may appear as email confirmation, calendar event, SMS reminder, and WhatsApp message. The assistant should avoid four separate alerts.

**Why useful:** This becomes important if inbound WhatsApp/SMS monitoring is added later.

### Recommended additions to the roadmap

Add these as optional later phases, not first-build requirements:

1. Waiting-on/follow-up tracker.
2. Deadline/renewal tracker.
3. Finance/admin watchlist.
4. Attachment/document intelligence.
5. Weekly review briefing.
6. Health-check/failure-monitoring job.
7. Privacy/retention policy.
8. Feedback loop and command shortcuts.

The highest-value additions are likely **waiting-on tracking**, **deadline/renewal tracking**, **weekly review**, and **health checks**, because they provide major practical value without requiring risky write actions.

---

## Files Likely to Change or Be Created

Because this is a setup/configuration project, most changes are Hermes config/state rather than application code.

**Project workspace:**
- `C:\hermes\PersonalProductivity\`

**Plan file:**
- `C:\hermes\PersonalProductivity\.hermes\plans\2026-05-16_231638-ai-email-calendar-alert-agent-team.md`

**Optional project rules/config file:**
- `C:\hermes\PersonalProductivity\email-calendar-alert-rules.md`
- `C:\hermes\PersonalProductivity\email-accounts.md`
- `C:\hermes\PersonalProductivity\important-senders.md`
- `C:\hermes\PersonalProductivity\important-categories.md`
- `C:\hermes\PersonalProductivity\important-email-review.md`
- `C:\hermes\PersonalProductivity\important-contacts.md`
- `C:\hermes\PersonalProductivity\messaging-integration-notes.md`
- `C:\hermes\PersonalProductivity\whatsapp-alert-format.md`
- `C:\hermes\PersonalProductivity\important-message-review.md`
- `C:\hermes\PersonalProductivity\gmail-workflow-notes.md`
- `C:\hermes\PersonalProductivity\gmail-label-plan.md`
- `C:\hermes\PersonalProductivity\allowed-senders.md`
- `C:\hermes\PersonalProductivity\unwanted-senders.md`
- `C:\hermes\PersonalProductivity\spam-actions-log.md`
- `C:\hermes\PersonalProductivity\cleanup-candidates.md`
- `C:\hermes\PersonalProductivity\cleanup-approvals.md`
- `C:\hermes\PersonalProductivity\cleanup-actions-log.md`
- `C:\hermes\PersonalProductivity\waiting-on.md`
- `C:\hermes\PersonalProductivity\deadline-tracker.md`
- `C:\hermes\PersonalProductivity\finance-watchlist.md`
- `C:\hermes\PersonalProductivity\document-review.md`
- `C:\hermes\PersonalProductivity\organization-map.md`
- `C:\hermes\PersonalProductivity\classification-feedback.md`
- `C:\hermes\PersonalProductivity\personal-admin-reference.md`
- `C:\hermes\PersonalProductivity\agent-health-log.md`
- `C:\hermes\PersonalProductivity\privacy-retention-policy.md`

**Google Workspace auth files:**
- `~/.hermes/google_client_secret.json`
- `~/.hermes/google_token.json`
- `~/.hermes/google_oauth_pending.json` temporary
- `~/.hermes/google_oauth_last_url.txt` temporary/helper

**Hermes config/gateway files, if using messaging delivery:**
- `~/.hermes/config.yaml`
- `~/.hermes/.env`
- `~/.hermes/logs/gateway.log`

**Cron scheduler state:**
- Managed internally by Hermes cron; inspect with `hermes cron list`.

**Optional future todo storage:**
- A markdown todo file in `C:\hermes\PersonalProductivity\`
- Obsidian note
- Notion database
- Google Tasks integration
- Another selected system

---

## Tests / Validation Checklist

### Authentication
- Google Workspace setup reports authenticated.
- Gmail search returns valid JSON.
- Calendar list returns valid JSON.

### Email triage
- Manual run finds recent unread mail from Gmail and Yahoo.
- Important messages are surfaced.
- Known important senders/categories such as banks, appointments, HMRC/tax authority, government, medical, insurance, utilities, travel, security, and payments are recognized.
- Smart selection surfaces high-confidence important messages from senders not yet on `important-senders.md`.
- Medium-confidence important candidates go to review/briefing instead of interrupting immediately.
- Important-looking promotional messages are suppressed unless sender/context supports importance.
- Newsletters/promotions are suppressed.
- Historical Gmail-forwarded-to-Yahoo messages are deduplicated if encountered.
- No email is sent, modified, archived, deleted, marked read, or labeled.
- Alert includes account, sender, subject, timestamp, confidence, reason, and recommended next action.

### Spam and unwanted sender workflow
- Manual dry run produces `unwanted-senders.md` candidates without modifying mail.
- Candidate list includes evidence, counts, account, and recommended action.
- Allowlisted/VIP senders are excluded.
- Suspicious/phishing messages are not unsubscribed from.
- Legitimate newsletter/commercial senders are recommended for unsubscribe first.
- Failed unsubscribe cases escalate to filter/block/delete recommendations only after the waiting period.
- No unsubscribe, block, filter, spam marking, or delete action happens without explicit approval.

### Bulk unwanted-email cleanup
- Preview mode reports exact sender, account, folder/label, count, oldest/newest dates, sample subjects, and exclusions.
- Preview mode makes no email changes.
- Cleanup uses exact `From` address matching by default, not display name or broad domain matching.
- Allowlisted, starred/flagged/important, attachment-bearing, protected-folder, and user-replied threads are excluded by default.
- A small sample cleanup is tested before any large batch.
- First cleanup action is reversible: label/quarantine or trash, not permanent deletion.
- Permanent deletion requires a separate approval after the recovery window.
- Cleanup action log records sender, query, counts, account/folder, date, and message IDs where available.

### Calendar sentinel
- Manual run finds upcoming events.
- Timezone is correct.
- Alerts are not repeated every run for the same event unless appropriate.
- Conflicts and imminent meetings are detected.
- No calendar events are created, edited, accepted, declined, or deleted.

### Daily briefing
- Includes today’s calendar and important email.
- Includes important WhatsApp/SMS messages only if a safe integration or manual import path has been enabled.
- Is delivered to WhatsApp once WhatsApp gateway delivery is configured.
- Suggested todos are traceable to email/calendar/message evidence.
- Output is concise and actionable.

### WhatsApp delivery and WhatsApp/SMS integration investigation
- Confirms outbound WhatsApp delivery works for alerts, daily updates, and calendar reminders.
- Documents WhatsApp alert formatting in `whatsapp-alert-format.md`.
- Documents feasible inbound WhatsApp/SMS integration options in `messaging-integration-notes.md`.
- Identifies whether user has Android, iPhone, WhatsApp personal, WhatsApp Business, or another route.
- Confirms read-only ingestion is possible before any automation is proposed.
- Confirms no WhatsApp/SMS messages are sent automatically.
- Applies the same confidence/reason approach used for important email.

### Gmail native workflow evaluation
- Documents current Gmail labels, categories, importance markers, stars, and Priority Inbox behavior in `gmail-workflow-notes.md`.
- Compares Gmail-native importance with Hermes smart classification.
- Produces a proposed `Hermes/` label scheme in `gmail-label-plan.md` before any labels are created.
- Confirms Multiple Inboxes can be supported by Gmail searches/labels without becoming a hard dependency.
- Does not create labels, filters, stars, or importance markers without explicit approval.

### Delivery
- Test alert arrives in WhatsApp.
- Test daily briefing arrives in WhatsApp and is readable on a phone screen.
- Test calendar reminder arrives in WhatsApp at the right time.
- Telegram fallback is documented only if WhatsApp setup/reliability is insufficient.
- Quiet hours behave as expected.
- Cron jobs can be listed, paused, resumed, and run manually.

---

## Risks, Tradeoffs, and Open Questions

### Risks
- **OAuth setup friction:** Google Cloud OAuth setup takes a few minutes and can fail if APIs/test users are not configured correctly.
- **Privacy:** Email and calendar content will be processed by the configured LLM provider. The user should confirm they are comfortable with this.
- **Notification noise:** Overly broad criteria could make alerts annoying.
- **Missed alerts:** Overly strict criteria could hide important items.
- **State tracking:** Repeated alerts require a reliable method to remember what has already been notified.
- **Timezone mistakes:** Calendar alerts must use the correct local timezone and offsets.
- **Todo hallucination:** Action items should be grounded in specific email/calendar evidence.

### Tradeoffs
- **Cron polling vs push notifications:** Cron is simpler and robust; push/webhooks would be faster but more complex.
- **Read-only first vs automation:** Read-only is safer; write actions save time but require stronger confirmation and audit trails.
- **Single combined job vs multiple agents:** Separate jobs are easier to tune and debug; a single job is simpler to manage but can become messy.
- **WhatsApp vs Telegram:** WhatsApp matches the user's preferred daily communication channel; Telegram may be easier for bots and debugging. Use WhatsApp first unless integration testing shows Telegram is materially more reliable or maintainable.
- **Current chat delivery vs gateway:** Current chat is simplest for setup tests; WhatsApp gateway delivery is more useful for real-time personal notifications.

### Open questions for the user
1. Confirm Gmail/Google Calendar as the first-build provider and scope.
2. For Yahoo, should access be through IMAP/Himalaya with an app password?
3. Confirm Gmail-to-Yahoo forwarding remains disabled for production use.
4. Which WhatsApp route should be used: personal WhatsApp through Hermes gateway, WhatsApp Business/API-style integration, or another WhatsApp-compatible adapter?
5. What timezone and quiet hours should be used?
6. Who are VIP senders/domains?
7. Which important senders/domains are already known, such as banks, HMRC, medical providers, utilities, insurers, travel providers, appointment systems, payment processors, and government services?
8. Which important categories should trigger immediate alerts versus daily briefing only?
9. What confidence threshold should interrupt immediately: high only, or high plus selected medium-confidence categories?
10. Which keywords should always trigger attention?
11. What senders/domains should be allowlisted and never blocked/deleted?
12. What unwanted sender actions are allowed initially: report only, unsubscribe with approval, block/filter with approval, delete with approval?
13. How long should the system wait after unsubscribe before treating it as failed: 7 days, 14 days, or another window?
14. For bulk cleanup, should the first approved action be label/quarantine, move to trash, or another reversible folder?
15. What folders/labels should be protected from bulk cleanup?
16. Should starred/flagged/important messages and threads where you replied always be excluded from cleanup?
17. What sample size is enough before approving a large sender cleanup: 10 messages, 25 messages, or another number?
18. Should the system remain read-only, or may it eventually label emails/create todos?
19. What todo system should be used if persistent todos are desired?
20. Should alerts be immediate, batched, or both?
21. Should inbound WhatsApp and/or SMS monitoring be considered in scope for a later phase, after outbound WhatsApp alerts work?
22. What phone platform is used for SMS: Android, iPhone, both, or something else?
23. Is WhatsApp personal or WhatsApp Business involved?
24. For WhatsApp/SMS, is read-only monitoring enough, or should the assistant eventually help draft replies for approval?
25. Do you currently use Gmail Priority Inbox, Multiple Inboxes, stars, importance markers, labels, filters, or categories in a deliberate way?
26. Should Hermes classification remain separate from Gmail at first, or should it eventually create Gmail labels under a `Hermes/` prefix?
27. Would Multiple Inboxes be useful for panes such as Important, Review, Finance/Tax, Appointments, Todo Candidates, and Cleanup Candidates?

---

## Recommended Next Action

Start with a read-only proof of concept:

1. Confirm Gmail + Google Calendar as the provider.
2. Confirm Yahoo access through IMAP/Himalaya and set it up as a second inbox.
3. Keep Gmail-to-Yahoo forwarding disabled and retain only lightweight duplicate protection for old forwarded messages.
4. Complete Google Workspace OAuth with `email,calendar` scopes.
5. Define a short VIP/keyword/quiet-hours rules file.
6. Create initial `important-senders.md` and `important-categories.md` for known important sources such as banks, HMRC, appointments, government, medical, legal, insurance, utilities, travel, payments, renewals, and security alerts.
7. Configure smart importance scoring so new high-confidence important senders/categories are surfaced even when not listed.
8. Define `allowed-senders.md` and start `unwanted-senders.md` in report-only mode.
9. Create one manual email triage job and one manual calendar sentinel job.
10. Create one manual spam/unwanted sender dry-run job.
11. Create a preview-only bulk cleanup workflow for approved unwanted `From` addresses.
12. Run each manually and tune prompts/rules.
13. Test a tiny approved cleanup sample using a reversible action.
14. Configure/test WhatsApp gateway delivery and send a manual test alert.
15. Draft `whatsapp-alert-format.md` for concise phone-friendly alerts, daily updates, and calendar reminders.
16. Add daily briefing and deliver it to WhatsApp once the format is approved.
17. Enable cron schedules only after manual results and WhatsApp delivery look useful.
18. Investigate inbound WhatsApp/SMS feasibility as a later phase and document options in `messaging-integration-notes.md`.
19. If feasible, add read-only WhatsApp/SMS important-message ingestion with `important-contacts.md` and confidence-based review.
20. Evaluate Gmail-native workflow features: Priority Inbox, Multiple Inboxes, labels, filters, stars, categories, and importance markers.
21. Draft a `gmail-label-plan.md` for optional `Hermes/` labels and Multiple Inboxes searches, but do not create labels/filters yet.
22. Add unsubscribe/filter/block/delete actions only after user approval and dry-run validation.
23. Add permanent deletion only after quarantine/trash recovery is verified and separately approved.
24. Add persistent todo integration only after the user approves suggested-todo behavior.
