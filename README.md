# Personal Productivity Agent

An intelligent background news and information monitoring system built on Hermes Agent. Monitors RSS feeds, X (Twitter), and web sources for configured topics, filters out noise, and delivers focused digests.

## Features

- **Multi-source monitoring**: RSS feeds, X/Twitter search, web search
- **Smart filtering**: Keyword include/exclude, importance rules, deduplication
- **Topic-based**: Monitor multiple topics (Bitcoin, AI, etc.) with independent rules
- **Admin CLI**: Easy management of topics, sources, and search rules
- **Scheduled delivery**: Cron-based digests delivered to your chat
- **Web app ready**: Package structure designed for future web interface

## Quick Start

```bash
# Install
pip install -e .

# Configure
cp config/news-monitor.example.yaml config/news-monitor.yaml
# Edit config/news-monitor.yaml with your topics and sources

# Set up RSS feeds
python scripts/setup_feeds.py

# Run admin CLI
productivity-agent list
productivity-agent test Bitcoin

# Run a digest manually
productivity-agent digest
```

## Configuration

Edit `config/news-monitor.yaml` to add topics, RSS feeds, X search queries, and filtering rules. See `docs/adding-topics.md` for details.

## Architecture

```
src/productivity_agent/    # Main package
├── config/                # Config loading & validation
├── sources/               # Information source plugins (RSS, X, web)
├── filtering/             # Content filtering & ranking
├── digest/                # Digest generation & formatting
├── delivery/              # Output delivery (CLI, webhook, email)
└── admin/                 # Admin CLI tools
config/                    # User-editable YAML config
web/                       # Future web app
tests/                     # Test suite
docs/                      # Documentation
```

## License
MIT
