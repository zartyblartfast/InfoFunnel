# WhatsApp Alert Format

Use this format once WhatsApp delivery is configured. During setup, the same concise format can be tested in the current Hermes chat.

## Important email alert

```
Important email: <short reason>
From: <sender>
Subject: <subject>
Received: <time>
Importance: <high/medium> — <why>
Legitimacy/applicability: <known applicable / likely legitimate but unconfirmed / suspicious> — <brief evidence>
Suggested action: <reply/review/pay attention/manual login/etc.>
```

## Calendar reminder

```
Upcoming: <event title>
When: <time>
Where: <location/link if present>
Prep: <short prep note if useful>
```

## Daily briefing

```
Daily briefing
1. Must know today: ...
2. Calendar: ...
3. Important email: ...
4. Suggested todos: ...
5. Watchlist: ...
```

Guidelines:

- Keep phone alerts short.
- Avoid dumping full private email bodies.
- Include enough context to decide whether to open the source system.
- If legitimacy/applicability is uncertain, say so clearly and recommend manually navigating to the official website/app instead of clicking email links.
- Avoid duplicate alerts for the same message/event.

## Current dry-run renderer

The project now has a tested renderer at `scripts/briefing_renderer.py`. It takes normalized/classified read-only items and emits a compact briefing with:

- `Mode: read-only dry run; 0 mutations`
- `Must know today` for applicable daily items
- `Calendar` for calendar events
- `Cleanup/watchlist` for optional cleanup, noise, and weekly-review items
- `Classification questions` for items whose action policy is `ask_user`
- a privacy footer confirming full email bodies are omitted

Latest local sample preview is saved at `.tmp/daily_briefing_preview.txt`.
