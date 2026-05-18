# Email and Calendar Alert Rules

## Operating mode

- Default mode: read-only.
- Do not modify email, calendar, todo, or messaging systems without explicit approval.
- Alerts should include importance confidence and reason.
- For uncertain senders, reports should also include a legitimacy/applicability assessment: known-to-user status, official organization/domain evidence, email authentication signals when available (SPF/DKIM/DMARC), whether the message asks the user to click/log in/pay, and a safer suggested action such as manually navigating to the official website/app instead of clicking email links.
- Check `email-sender-classification-ledger.md` before classifying senders. If a sender is new, ambiguous, or a potential subscription/savings opportunity, propose a ledger update instead of silently changing behaviour.
- If an email suggests an unused paid service or subscription, add/report it as an opportunity-check item, not just an email alert.

## VIP senders/domains

Add known people, businesses, services, and domains here.

| sender_or_domain | category | default_action | notes |
|---|---|---|---|
| hmrc.gov.uk | tax/government | immediate alert | Verify sender carefully. |

## Important message signals

High-confidence candidates:

- Directly addressed to me and action-oriented.
- From a VIP sender/domain/contact.
- Banks, cards, payments, refunds, suspicious activity, account access, password reset, verification/security alerts.
- HMRC/tax authority, government, legal, insurance, mortgage, pension, utilities.
- Medical, appointment, prescription, test results, booking reminders, cancellations, reschedules.
- Travel, tickets, hotel, flight/train disruption, check-in, booking reference.
- Deadlines, renewals, fines, penalties, invoices, contracts, forms.
- Replies in active threads I recently participated in.

Medium-confidence candidates:

- Unknown sender with strong finance/tax/medical/security/deadline wording.
- Credible appointment or admin message where sender is not yet known.
- Message may be important but should go to review/briefing rather than interrupting.

Suppress by default:

- Generic promotions/newsletters.
- Social/network updates.
- Automated status messages unless they contain failure, outage, payment, security, or deadline terms.
- Marketing that merely contains important-sounding words.

## Calendar alert rules

- Alert before upcoming meetings/appointments.
- Alert earlier if location/travel is involved.
- Alert for conflicts, cancellations, location/link changes, or prep-heavy events.
- Include title, start time, location/link if present, and suggested preparation.

## Quiet hours

Default placeholder: `22:00-07:00 local time`.

Exceptions: urgent/security/travel/family/VIP only.

## Unwanted sender handling

- Maintain allowlist first.
- Report suspected unwanted senders before taking action.
- Prefer unsubscribe only for legitimate commercial senders and only after approval.
- Do not click unsubscribe links from obvious scams/phishing.
- Bulk cleanup must be preview-only first.
- Use exact From address matching before considering domain-wide rules.
- Permanent deletion requires separate explicit approval.
