# Unwanted Senders

Status values:

- `candidate` — suspected unwanted sender, needs review.
- `unsubscribe-safe` — unsubscribe appears legitimate; wait for approval.
- `unsubscribe-attempted` — unsubscribe was attempted; monitor recurrence.
- `unsubscribe-failed` — messages continued after waiting period.
- `filter-recommended` — recommend provider-side filtering/blocking.
- `blocked-or-filtered` — provider-side rule active.
- `delete-recommended` — safe to delete future matches after approval.
- `allowed` — should not be treated as spam.

| sender | domain | account | status | evidence | first_seen | last_seen | count | recommended_action | notes |
|---|---|---|---|---|---|---|---:|---|---|
| email@mailer.hollandandbarrett.com | mailer.hollandandbarrett.com | Gmail | candidate | Repeated retail promotion subjects in recent unread mail, including `Final hours for EXTRA 25% off` and `EXTRA 25% off, only in the app`. | 2026-05-17 | 2026-05-17 | 2+ | report-only review; consider unsubscribe/filter only after approval | Do not modify mail yet. |
| reply@rs.email.nextdoor.co.uk | rs.email.nextdoor.co.uk | Gmail | candidate | Repeated community/social digest posts in recent unread mail. | 2026-05-17 | 2026-05-17 | 2+ | report-only review; keep only if local/community alerts are wanted | Some local utility/security posts could be relevant; avoid broad blocking until sampled. |
| partnerpromotions@partner.rightmove.co.uk | partner.rightmove.co.uk | Gmail | candidate | Partner promotion: `Clive, is your home worth more than you thought?` | 2026-05-17 | 2026-05-17 | 1+ | report-only review; consider unsubscribe/filter only after approval | Keep distinct from core Rightmove account/alert emails if those are useful. |
| jobs@gulftalent.com | gulftalent.com | Gmail | candidate | Job digest: `Clive, latest job in Riyadh for you`. | 2026-05-16 | 2026-05-16 | 1+ | report-only review; keep only if job-search alerts are wanted | Do not block if user is actively job searching. |
| admin@cv-library.co.uk | cv-library.co.uk | Gmail | candidate | Repeated job digest subjects, including `17 new jobs based on your recent activity` and `25 new jobs based on your recent activity`. | 2026-05-16 | 2026-05-17 | 2+ | report-only review; keep only if job-search alerts are wanted | Do not block if user is actively job searching. |
| jobs-listings@linkedin.com | linkedin.com | Gmail | candidate | Job listing digest: `Deloitte is hiring a SQL Server Database Administrator`. | 2026-05-16 | 2026-05-16 | 1+ | report-only review; keep only if LinkedIn job alerts are wanted | Avoid broad linkedin.com filtering. |

