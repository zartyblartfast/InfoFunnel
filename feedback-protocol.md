# Structured Feedback Protocol

Purpose: reduce friction by asking the user predefined, low-effort classification questions instead of relying on free-form messages.

## When to ask

Ask only when the answer will change future behavior. Do not ask about resolved facts already stored in the registry.

Good reasons to ask:
- unknown applicability for a recurring sender
- possible paid subscription/cancellation opportunity
- whether a noisy sender should be weekly cleanup, suppress, or proposed filter
- whether a category should trigger immediate alerts

Bad reasons to ask:
- curiosity with no policy impact
- facts the user already confirmed
- cases where default safe handling is adequate

## Question format

Use compact multiple choice.

```text
Classify <service/sender>:
1 current important
2 current low priority
3 historical free-tier
4 historical paid-risk
5 historical unknown cost
6 noise candidate
7 suspicious
8 ignore/suppress
Reply with: <service> <number>
```

Optional second question:

```text
Action policy for <service/sender>:
1 report only
2 manual check
3 optional account closure
4 possible cancellation
5 propose filter
6 propose unsubscribe
7 ignore
Reply with: <service> action <number>
```

## Mapping: classification answer

1 `current important`
- user_relationship: `current_applicable`
- trust_level: `trusted_confirmed`
- urgency: `daily_briefing` by default; immediate only for security/payment/deadline/action-required
- disposition: `review_today`

2 `current low priority`
- user_relationship: `current_applicable`
- trust_level: `trusted_confirmed`
- urgency: `low_priority`
- disposition: `monitor_only`

3 `historical free-tier`
- user_relationship: `historical_unused`
- cost_status: `free_tier`
- urgency: `weekly_cleanup` or `low_priority`
- disposition: `optional_cleanup`
- action_policy: `optional_account_closure`

4 `historical paid-risk`
- user_relationship: `historical_unused`
- cost_status: `paid_possible` or `paid_active` if confirmed
- urgency: `weekly_cleanup`; immediate only for imminent payment/deadline/security
- disposition: `review_when_convenient`
- action_policy: `possible_cancellation`

5 `historical unknown cost`
- user_relationship: `historical_unused`
- cost_status: `unknown`
- disposition: `needs_user_classification`
- action_policy: `manual_check`

6 `noise candidate`
- user_relationship: `unwanted_marketing`
- urgency: `weekly_cleanup` or `suppress_unless_changed`
- disposition: `noise_candidate`
- action_policy: `propose_filter` or `propose_unsubscribe`

7 `suspicious`
- trust_level: `suspicious`
- disposition: `suspicious_do_not_click`
- action_policy: `report_only`

8 `ignore/suppress`
- urgency: `suppress_unless_changed`
- disposition: `safe_to_ignore`
- action_policy: `ignore`

## Mapping: action answer

1 `report only` -> action_policy `report_only`
2 `manual check` -> action_policy `manual_check`
3 `optional account closure` -> action_policy `optional_account_closure`
4 `possible cancellation` -> action_policy `possible_cancellation`
5 `propose filter` -> action_policy `propose_filter`
6 `propose unsubscribe` -> action_policy `propose_unsubscribe`
7 `ignore` -> action_policy `ignore`

## Applying feedback

After receiving an answer:

1. Update `sender-service-registry.csv`.
2. Add or update a case in `triage-evaluation-cases.jsonl`.
3. If relevant, update `subscription-savings-watchlist.md`.
4. Remove stale uncertainty from older project files if it would mislead future agents.
5. Confirm the update in one short sentence.

## Example

Agent:

```text
Classify Backblaze:
1 current important
2 current low priority
3 historical free-tier
4 historical paid-risk
5 historical unknown cost
6 noise candidate
7 suspicious
8 ignore/suppress
Reply with: Backblaze <number>
```

User:

```text
Backblaze 3
```

Result:

- registry: historical_unused + free_tier
- disposition: optional_cleanup
- future briefings: low urgency, optional account closure/data cleanup only
