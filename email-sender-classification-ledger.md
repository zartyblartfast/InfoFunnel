# Email Sender Classification Ledger

Last updated: 2026-05-17 19:49:00 GMTDT

Purpose: keep a reviewable record of known, uncertain, unwanted, and opportunity-related senders so the assistant can improve triage without relying only on memory or one-off judgement.

Default safety rules:
- This ledger is classification only; it does not authorize mailbox changes.
- Do not click email links, unsubscribe, filter, block, delete, label, mark read, or reply without explicit approval.
- For uncertain or cancellation-related senders, recommend manual navigation to the official website/app or checking password manager/payment records.
- Email authentication passing is useful evidence of legitimacy, but it does not prove the service is still applicable or worth paying for.

## Classification statuses

| status | meaning |
|---|---|
| known-applicable | User confirms the organisation/service is real and currently relevant. |
| known-historical | User confirms they used it before, but may no longer need it. |
| uncertain-applicability | Organisation may be legitimate, but user does not know whether it applies. |
| opportunity-check | Potential money/time/admin opportunity, such as cancelling an unused paid service. |
| important | Should appear in daily briefing or immediate alert depending on rules. |
| allowed | Should not be blocked/deleted/filtered as unwanted without separate approval. |
| noisy-candidate | Candidate for report-only unwanted/noise review. |
| suspicious | Possible phishing/scam; do not click links. |
| resolved | Classification/action decision has been completed. |

## Ledger

| sender_or_domain | organisation/service | status | applicability | legitimacy evidence | importance / handling | open question | recommended next action | last_reviewed | notes |
|---|---|---|---|---|---|---|---|---|---|
| notification@billing.o2.com | O2 | known-applicable; important; allowed | Confirmed current/applicable by user. | Known provider and approved billing sender. | Daily briefing by default; immediate only for payment failure, overdue, security, or unusual amount. | None currently. | Review bill only if desired or amount looks wrong. | 2026-05-17 | User explicitly contrasted O2 as real/applicable. |
| billing.o2.com | O2 | known-applicable; important; allowed | Confirmed current/applicable by user. | Known provider and approved billing domain. | Same as O2 billing sender. | None currently. | Treat account/payment/security messages as relevant; suppress unrelated marketing. | 2026-05-17 | Domain-level rule should be used carefully. |
| no-reply@backblaze.com | Backblaze | known-historical; free-tier; opportunity-check | User remembers using Backblaze for a prototype app, does not need it anymore, and confirmed current usage is free-tier. | Gmail authentication passed SPF/DKIM/DMARC; `backblaze.com` appears to be a real backup/storage organisation. | Low urgency; include as optional admin cleanup/watchlist item, not as money-saving urgent. Escalate only for payment, security, account-access, data-loss, or quota-blocking issues. | Is the account still active and storing anything worth keeping/deleting? | No payment urgency. Consider manually closing the account or deleting unused data if convenient. Do not click email links. | 2026-05-17 | User confirmed Backblaze is free-tier; future storage-cap emails can be treated as low-urgency admin cleanup unless they indicate security/payment/account risk. |
| backblaze.com | Backblaze | known-historical; free-tier; opportunity-check | User used it historically for a prototype app, no longer needs it, and confirmed it is free-tier. | Official website exists; email authentication observed on `no-reply@backblaze.com`. | Low urgency; optional watchlist/admin cleanup only. | Account still active? Any stored data worth keeping/deleting? | If convenient, manually close the account or leave as free-tier/no-payment-risk. | 2026-05-17 | Payment-status question resolved: free-tier. |
| lifesightsupport@wtwco.com | LifeSight / WTW | important; allowed | User approved as relevant enough for pension/finance review. | Plausible pension/finance sender; sender/domain approved after manual triage. | Daily briefing; immediate only for action, deadline, security, or account-access issue. | Confirm ongoing relevance if needed. | Review when convenient; avoid treating as noise. | 2026-05-17 | Financial-account notices should not be deleted/filtered without approval. |
| wtwco.com | WTW / LifeSight | important; allowed | User approved as relevant enough for pension/finance review. | Known approved domain after manual triage. | Same as LifeSight sender. | Confirm ongoing relevance if needed. | Include account notices in briefing. | 2026-05-17 | Domain-level classification should avoid suppressing unrelated marketing incorrectly. |
| hmrc.gov.uk | HMRC / UK tax authority | known-applicable?; important; allowed | Generally important category; user-specific applicability presumed for UK tax/admin, but verify message-by-message. | Official government domain pattern; still verify phishing/lookalikes. | Immediate alert for credible tax/government messages. | None currently. | Verify carefully; never click suspicious links. | 2026-05-17 | Keep high-sensitivity. |
| email@mailer.hollandandbarrett.com | Holland & Barrett | noisy-candidate | No current importance confirmed. | Retail marketing sender observed. | Report-only unwanted/noise candidate. | Keep or unsubscribe/filter? | No action unless user approves. | 2026-05-17 | Repeated promotions. |
| reply@rs.email.nextdoor.co.uk | Nextdoor community digests | noisy-candidate | Some local posts might occasionally matter; not generally important. | Community/social digest sender observed. | Report-only candidate; avoid broad blocking until sampled. | Are local alerts useful? | No action unless user approves. | 2026-05-17 | Could contain local utility/security issues, so classify carefully. |
| partnerpromotions@partner.rightmove.co.uk | Rightmove partner promotions | noisy-candidate | Partner promotions not confirmed useful. | Sender observed in recent unread mail. | Report-only noise candidate. | Keep or unsubscribe/filter? | No action unless user approves. | 2026-05-17 | Keep distinct from core Rightmove alerts. |
| jobs@gulftalent.com | GulfTalent jobs | noisy-candidate | Job-search relevance unknown. | Job digest sender observed. | Report-only candidate. | Is user actively job searching for these roles? | No action unless user approves. | 2026-05-17 | Do not block if job alerts are wanted. |
| admin@cv-library.co.uk | CV-Library | noisy-candidate | Job-search relevance unknown. | Job digest sender observed. | Report-only candidate. | Is user actively job searching? | No action unless user approves. | 2026-05-17 | Repeated job alerts. |
| jobs-listings@linkedin.com | LinkedIn jobs | noisy-candidate | Job-search relevance unknown. | LinkedIn job digest observed. | Report-only candidate; avoid broad linkedin.com filtering. | Are LinkedIn job alerts wanted? | No action unless user approves. | 2026-05-17 | Sender-specific only. |

## How future agents should use this file

1. Check this ledger before deciding whether an email is known-applicable, uncertain, noisy, or suspicious.
2. If a new sender is important or ambiguous, propose a ledger entry rather than silently changing behaviour.
3. Use `open question` and `recommended next action` fields to generate useful daily briefing/watchlist items.
4. For opportunity-check entries, help the user find possible savings or admin cleanup, but do not cancel, unsubscribe, or click links without approval.
5. When the user confirms a fact, update the relevant row with date and evidence.
