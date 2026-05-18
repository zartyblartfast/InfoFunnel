# Web App (Planned)

This directory will contain the web interface for the Personal Productivity Agent.

## Planned Architecture

- **Framework**: FastAPI (async, modern, Pythonic)
- **Frontend**: Simple HTML + HTMX (no heavy JS framework needed)
- **Auth**: Session-based with optional OAuth
- **Database**: SQLite (simple) or PostgreSQL (if scaling needed)

## Planned Features

- Dashboard showing all topics and their status
- Visual config editor (forms instead of YAML)
- Real-time digest preview
- Source health monitoring
- Historical digest archive
- Per-topic statistics (items/day, signal-to-noise ratio)

## Getting Started (Future)

```bash
pip install -e ".[web]"
uvicorn web.app:create_app --reload
```
