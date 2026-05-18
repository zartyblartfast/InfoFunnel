# Sender Legitimacy and Applicability Checks

Purpose: help distinguish between messages from known applicable services, likely legitimate but unconfirmed services, and suspicious/phishing messages.

Default posture:
- Do not click email links during automated analysis.
- Do not log in, pay, unsubscribe, reply, or modify mailbox state without explicit approval.
- For uncertain senders, recommend manually navigating to the official website/app or checking account records rather than clicking links in the email.

## Assessment fields for reports

| field | meaning |
|---|---|
| known_to_user | Whether the user has confirmed using the service/sender. Values: yes, no, uncertain. |
| organization_legitimacy | Whether the organization/domain appears to be a real legitimate organization. Values: likely legitimate, uncertain, suspicious. |
| email_authentication | SPF/DKIM/DMARC evidence where available. Passing authentication is helpful but not proof the email is applicable to the user. |
| applicability | Whether the message appears relevant to the user/account. Values: confirmed, likely, uncertain, unlikely. |
| link_safety | Whether the message asks the user to click/log in/pay and whether safer manual navigation is recommended. |
| recommended_action | What the user should do next, preferably without clicking email links if uncertain. |

## Legitimacy/applicability tiers

| tier | definition | handling |
|---|---|---|
| Known applicable | User has confirmed the service/sender is used and the sender/domain is expected. | Classify by importance; include in alert/briefing according to rules. |
| Likely legitimate but unconfirmed | Organization/domain looks legitimate and email authentication passes, but the user has not confirmed they use the service. | Include evidence and ask the user to confirm applicability; recommend manual navigation, not email links. |
| Suspicious | Authentication fails, domain is lookalike/mismatched, content pressures payment/login, or sender/service is unknown with risky links. | Warn clearly; do not click links; suggest verifying independently or ignoring/reporting. |
| Marketing/noise | Legitimate organization but message is promotional/non-actionable. | Suppress or include as cleanup candidate, not an important alert. |
| Known historical / no longer needed | User confirms they used the service before, but it may not be needed anymore. | Treat as an admin/subscription review opportunity, especially if messages mention billing, quotas, renewals, storage, or account status. |
| Opportunity-check | A message may reveal a money-saving/admin opportunity, such as cancelling an unused paid account. | Include the open question and safe verification steps in the briefing; do not cancel, unsubscribe, or click links without approval. |

## Backblaze example from 2026-05-17

Message:
- From: Backblaze Team <no-reply@backblaze.com>
- Subject: Backblaze Daily Storage Cap reached 100%.

Observed evidence:
- Organization/domain: Backblaze appears to be a real backup/storage company with an active official website at `https://www.backblaze.com`.
- Gmail authentication headers passed:
  - DKIM: pass for `service.backblaze.com`
  - SPF: pass for `service.backblaze.com`
  - DMARC: pass with header.from `backblaze.com`
- Applicability: known historical; user remembers using Backblaze for a prototype app, no longer needs it, and confirmed it is free-tier.
- Open question: whether the free-tier account is still active and whether any stored data should be kept, deleted, or closed out.
- Risk note: authentication passing means the email is likely from Backblaze or its authorized sender, but it does not prove the user should click email links. User has confirmed the account is free-tier, so storage-cap notices are low-urgency unless they mention security, payment, account access, data loss, or quota blocking.

Recommended report wording:

```text
Backblaze storage cap reached 100%.
Importance: medium-high — account/quota alert, and possible subscription/admin cleanup opportunity.
Legitimacy/applicability: likely legitimate and historically applicable — backblaze.com is a real backup/storage company and Gmail authentication passed SPF/DKIM/DMARC; you remember using it for a prototype app, no longer need it, and confirmed it is free-tier.
Suggested action: no payment urgency. Optionally close the account or delete unused data if convenient. Avoid clicking email links.
```

## O2 contrast example

- User has confirmed O2 is real and applicable.
- O2 billing messages from the approved sender/domain should be treated as known applicable, while still suppressing unrelated marketing and remaining alert to payment/security anomalies.
