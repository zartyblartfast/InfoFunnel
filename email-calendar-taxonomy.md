# Email and Calendar Controlled Taxonomy

Purpose: provide fixed labels for the personal productivity agent. Agents must classify using these enum values rather than inventing free-form status strings.

## Core principles

1. Separate legitimacy from personal applicability.
2. Sender/domain policy is durable state; individual messages/events may override it.
3. Live email/calendar data is read-only test/sample data unless mutation is explicitly approved.
4. Unknowns should produce structured questions, not ad-hoc prose.
5. Confidence is about the classification, not about whether an action is authorized.

## Enums

### trust_level

- `trusted_confirmed` — user confirmed this sender/service/domain is expected or current.
- `likely_legitimate` — evidence suggests it is real, but user has not confirmed current relevance.
- `unknown` — insufficient evidence.
- `suspicious` — phishing/scam/lookalike/authentication/content concerns.
- `blocked_or_unwanted` — user identified as unwanted or unsafe.

### user_relationship

- `current_applicable` — user currently uses/cares about the service.
- `historical_unused` — user used it previously but no longer needs it.
- `unknown_applicability` — could be relevant but not confirmed.
- `not_applicable` — confirmed not relevant to user.
- `unwanted_marketing` — marketing/promotional material not wanted.

### cost_status

- `free_tier` — confirmed no payment urgency.
- `paid_active` — confirmed active paid service.
- `paid_possible` — may be paid; needs verification.
- `no_account` — user confirms no account/relationship.
- `unknown` — not yet known.
- `not_relevant` — cost does not apply.

### source_type

- `gmail`
- `google_calendar`
- `yahoo_mail`
- `manual_user_input`
- `registry_default`

### message_category

- `billing`
- `payment_failure`
- `security`
- `account_access`
- `government_tax`
- `pension_finance`
- `calendar_event`
- `delivery_travel`
- `subscription`
- `quota_usage`
- `newsletter`
- `marketing`
- `job_alert`
- `community_digest`
- `social`
- `system_notification`
- `unknown`

### event_category

- `meeting`
- `appointment`
- `travel`
- `deadline`
- `personal_commitment`
- `reminder`
- `holiday`
- `unknown`

### urgency

- `immediate` — interrupt/alert now.
- `daily_briefing` — include in daily summary.
- `weekly_cleanup` — include in low-priority cleanup digest.
- `low_priority` — record only; surface sparingly.
- `suppress_unless_changed` — do not surface unless a new risk/action/deadline appears.

### disposition

- `action_required_now`
- `review_today`
- `review_when_convenient`
- `optional_cleanup`
- `monitor_only`
- `safe_to_ignore`
- `noise_candidate`
- `suspicious_do_not_click`
- `needs_user_classification`

### action_policy

- `report_only` — describe only; no side effects.
- `ask_user` — ask structured question before deciding.
- `manual_check` — suggest user navigates manually to official site/app or account records.
- `optional_account_closure` — user may close/delete unused account/data manually.
- `possible_cancellation` — potential paid-service cancellation; no cancellation by agent.
- `propose_filter` — can propose a Gmail/Yahoo filter but not create it.
- `propose_unsubscribe` — can propose unsubscribe but not click.
- `ignore` — do not surface unless conditions change.

### mutation_policy

- `none_read_only` — no mutation allowed.
- `propose_only` — may draft an action for approval.
- `approved_specific_action` — one explicitly approved action.
- `approved_class_action` — future class of actions approved by user.

Default for this project is `none_read_only`.

### confidence

- `high`
- `medium`
- `low`
- `needs_review`

## Recommended combinations

### Historical free-tier account

Example: Backblaze after user confirmation.

- trust_level: `likely_legitimate`
- user_relationship: `historical_unused`
- cost_status: `free_tier`
- urgency: `weekly_cleanup` or `low_priority`
- disposition: `optional_cleanup`
- action_policy: `optional_account_closure`
- mutation_policy: `none_read_only`

### Current important billing/service account

Example: O2 billing.

- trust_level: `trusted_confirmed`
- user_relationship: `current_applicable`
- cost_status: `paid_active` or `unknown`
- message_category: `billing`
- urgency: `daily_briefing`; `immediate` for payment failure, security, overdue, unusual amount, or deadline.
- disposition: `review_today` or `action_required_now`
- action_policy: `manual_check`
- mutation_policy: `none_read_only`

### Noisy marketing/newsletter

- trust_level: `likely_legitimate` or `unknown`
- user_relationship: `unwanted_marketing`
- cost_status: `not_relevant`
- message_category: `marketing` or `newsletter`
- urgency: `weekly_cleanup` or `suppress_unless_changed`
- disposition: `noise_candidate`
- action_policy: `propose_filter` or `propose_unsubscribe`
- mutation_policy: `none_read_only`

### Suspicious message

- trust_level: `suspicious`
- user_relationship: `unknown_applicability`
- urgency: `immediate` if likely harmful or impersonating important service.
- disposition: `suspicious_do_not_click`
- action_policy: `report_only`
- mutation_policy: `none_read_only`
