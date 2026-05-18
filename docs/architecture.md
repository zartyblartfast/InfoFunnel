# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Cron Scheduler                        │
│              (4x daily: 8a, 12p, 6p, 10p)              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  Digest Generator                        │
│                                                          │
│  1. Load config (news-monitor.yaml)                     │
│  2. For each enabled topic:                             │
│     a. Fetch RSS feeds (blogwatcher-cli)                │
│     b. Search X (x_search tool)                         │
│     c. Apply filters (keywords, dedup, ranking)         │
│  3. Format digest (Jinja2 templates)                    │
│  4. Deliver (CLI / webhook / email)                     │
└─────────────────────────────────────────────────────────┘
```

## Component Map

| Component | Location | Purpose |
|-----------|----------|---------|
| Config | `config/news-monitor.yaml` | User-editable topic/source/rules |
| Config loader | `src/productivity_agent/config/` | Load, validate, query config |
| RSS source | `src/productivity_agent/sources/rss.py` | Fetch from blogwatcher-cli |
| X source | `src/productivity_agent/sources/x_search.py` | Search X via x_search tool |
| Filter engine | `src/productivity_agent/filtering/` | Keyword filter, dedup, rank |
| Digest generator | `src/productivity_agent/digest/` | Format output |
| Admin CLI | `src/productivity_agent/admin/` | Manage topics/sources |
| Cron job | Hermes scheduler | Run digest on schedule |

## Data Flow

```
Config YAML ──► Config Loader ──► Enabled Topics
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
              RSS Source          X Search Source       Web Source
                    │                    │                    │
                    └────────────────────┼────────────────────┘
                                         ▼
                              Filter Engine
                              (keywords, dedup, rank)
                                         │
                                         ▼
                              Digest Generator
                              (format, cap, template)
                                         │
                                         ▼
                              Delivery (CLI/webhook/email)
```

## Extending

- **New topic**: Add to `config/news-monitor.yaml`
- **New source type**: Create class in `src/productivity_agent/sources/`
- **New filter**: Add to `src/productivity_agent/filtering/`
- **New output format**: Add template to `src/productivity_agent/digest/templates/`
