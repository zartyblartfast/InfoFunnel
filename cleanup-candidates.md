# Cleanup Candidates

Default mode: preview-only.

Rules:

- Exact From address matching first.
- Exclude allowlisted senders.
- Exclude starred/flagged/important messages by default.
- Exclude threads where the user replied by default.
- Exclude attachments until sampled and approved.
- Prefer quarantine/label/trash before permanent deletion.
- Permanent deletion requires a separate explicit approval.

| sender | account | query | preview_count | folders_or_labels | oldest | newest | sample_subjects | exclusions | proposed_action | approval_status |
|---|---|---|---:|---|---|---|---|---|---|---|

