# Important Email Review

Last updated: 2026-05-17 19:10:25 GMTDT

## Manual read-only Gmail triage pass

Scope:
- Gmail only; Yahoo is not configured yet.
- Read-only metadata/snippet review plus short body excerpts for likely important candidates only.
- Queries used:
  - `newer_than:2d is:unread`
  - `newer_than:7d is:unread -category:promotions -category:social`
  - `newer_than:14d (bank OR payment OR refund OR tax OR HMRC OR appointment OR booking OR reminder OR cancellation OR renewal OR invoice OR security OR verification OR password OR login OR insurance OR utility OR travel)`
- No mailbox changes were made.

## Immediate alerts

None found in this pass.

## Important / review candidates

| priority | sender | subject | received | confidence | reason | suggested action |
|---|---|---|---|---|---|---|
| important, not urgent | O2 <notification@billing.o2.com> | Your O2 bill is ready | 2026-05-16 09:10 +0000 | high | Official utility/mobile billing message; bill is ready and direct debit date is stated. | Review if you want to check the amount; likely include in daily briefing rather than interrupt immediately. |
| review | LifeSight Pensions Team <lifesightsupport@wtwco.com> | Clive, your LifeSight Account has reached a new milestone! | 2026-05-16 20:16 GMT | medium-high | Pension/account milestone from a plausible provider; informational but financially relevant. | Add LifeSight/WTW to important senders if this provider is legitimate for you; include similar account/pension notices in daily briefing unless action/deadline is present. |

## Low-priority / likely noise examples from recent unread mail

| sender | subject | reason |
|---|---|---|
| Holland & Barrett <email@mailer.hollandandbarrett.com> | Final hours for EXTRA 25% off / EXTRA 25% off, only in the app | Promotional retail marketing. |
| All Saints Kettering Posts <reply@rs.email.nextdoor.co.uk> | Neighbourhood/social posts | Community/social updates; not personal urgent unless a specific local utility/security issue is relevant. |
| Rightmove Partners <partnerpromotions@partner.rightmove.co.uk> | Clive, is your home worth more than you thought? | Partner promotion. |
| AVSForum.com digest | Designed a physical TV remote... | Forum digest/newsletter. |
| GulfTalent Jobs / CV-Library / LinkedIn job alerts | Job listings | Job digests; only important if active job-search alerts are desired. |
| Restore Britain | Makerfield update | Political/newsletter-style update. |
| Citywire Investment Trust Insider | Sunday investment newsletter | Newsletter/digest. |
| Comparethemarket.com | Need more breathing room for bigger spends? | Financial marketing; contains credit-card language but appears promotional. |
| Airbnb | Save 15% on your ideal summer home | Travel marketing, not booking/trip-critical. |
| Substack | Weekend/newsletter content | Newsletter. |

## Suggested rule tuning for approval

Candidate additions to `important-senders.md` / `allowed-senders.md` if the user confirms they are legitimate and useful:

| sender_or_domain | category | suggested_action | reason |
|---|---|---|---|
| notification@billing.o2.com / billing.o2.com | utility/mobile billing | daily briefing or immediate if payment failure/overdue/security | Real billing notices are important; marketing from O2 should still be suppressible. |
| lifesightsupport@wtwco.com / wtwco.com | pension/finance | daily briefing; immediate only if action/deadline/security | Pension account notifications are financially important but not always urgent. |

Possible unwanted/noisy sender review candidates, subject to user approval before any rule changes:

| sender_or_domain | reason |
|---|---|
| email@mailer.hollandandbarrett.com | repeated retail promotions in recent unread mail |
| reply@rs.email.nextdoor.co.uk | repeated community/social digest posts |
| partnerpromotions@partner.rightmove.co.uk | partner promotion |
| jobs@gulftalent.com, admin@cv-library.co.uk, jobs-listings@linkedin.com | job digests; keep only if wanted |

## Calendar check

Google Calendar default upcoming-event check returned no upcoming events in its default window.

## Safety notes

- No emails were sent, archived, labelled, marked read, deleted, unsubscribed, filtered, or modified.
- No calendar items were created, edited, accepted, declined, or deleted.
- Further tuning should update project files only after user approval.
