"""Default configuration values."""

DEFAULT_GLOBAL = {
    "schedule": "0 8,12,18,22 * * *",
    "delivery": "origin",
    "model": "",
    "max_total_items": 10,
    "quiet_hours": "23:00-07:00",
}

DEFAULT_TOPIC = {
    "enabled": False,
    "max_items": 3,
    "rss_feeds": [],
    "x_queries": [],
    "x_allowed_handles": [],
    "x_excluded_handles": [],
    "keywords_include": [],
    "keywords_exclude": [],
    "importance_rules": "",
}
