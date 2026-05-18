"""Configuration loading and validation."""

import os
import yaml
import json
from pathlib import Path
from typing import Any, Optional

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "news-monitor.yaml"
SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "news-monitor.schema.json"


class ConfigError(Exception):
    pass


def load_config(path: Optional[str | Path] = None) -> dict[str, Any]:
    """Load and validate the news monitor configuration.

    Args:
        path: Path to YAML config file. Defaults to config/news-monitor.yaml
              relative to the project root.

    Returns:
        Parsed configuration dict with 'global' and 'topics' keys.

    Raises:
        ConfigError: If the file is missing, unreadable, or invalid.
    """
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH

    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in {config_path}: {e}")

    if not isinstance(config, dict):
        raise ConfigError(f"Config must be a YAML mapping, got {type(config).__name__}")

    # Validate against schema if available
    if SCHEMA_PATH.exists():
        _validate_schema(config, SCHEMA_PATH)

    # Ensure required sections exist
    if "global" not in config:
        config["global"] = {}
    if "topics" not in config:
        config["topics"] = []

    return config


def _validate_schema(config: dict, schema_path: Path) -> None:
    """Validate config against JSON Schema. Raises ConfigError on failure."""
    import jsonschema
    with open(schema_path) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(config, schema)
    except jsonschema.ValidationError as e:
        raise ConfigError(f"Config validation error: {e.message} at {list(e.absolute_path)}")


def get_enabled_topics(config: dict) -> list[dict[str, Any]]:
    """Return only enabled topics from the config."""
    return [t for t in config.get("topics", []) if t.get("enabled", False)]


def get_topic(config: dict, name: str) -> Optional[dict[str, Any]]:
    """Find a topic by name (case-insensitive)."""
    for topic in config.get("topics", []):
        if topic.get("name", "").lower() == name.lower():
            return topic
    return None
