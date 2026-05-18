# Important Categories

| category | signals | default_action | notes |
|---|---|---|---|
| bank/security | login, verification, suspicious activity, card, account, payment, password reset | immediate alert | Suppress obvious marketing. |
| tax/HMRC/government | HMRC, tax, self assessment, notice, code, payment, government gateway | immediate alert | Verify sender carefully. |
| appointments | appointment, booking, reminder, cancellation, reschedule, prescription, results | immediate alert | Include date/time if found. |
| legal/insurance/utilities | policy, claim, renewal, contract, outage, bill, arrears, mobile bill, direct debit, account number | high or daily briefing | Interrupt only when deadline/action/security/payment failure/unusual amount is clear. |
| pension/finance account | pension, LifeSight, WTW, account milestone, contribution, statement, retirement, investment account | daily briefing; immediate for deadline/action/security | Treat financial-account notices as important, but avoid interrupting for routine informational milestones unless action is required. |
| travel | flight, train, hotel, check-in, boarding, booking reference, disruption | immediate alert when time-sensitive | Include dates and references. |
| deadlines/renewals | due, deadline, renewal, expires, fine, penalty, form, invoice | high or daily briefing | Include deadline when extractable. |
