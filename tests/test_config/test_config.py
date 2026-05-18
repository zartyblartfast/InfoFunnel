"""Tests for configuration loading and validation."""

import pytest
import os
import tempfile
import yaml

from productivity_agent.config import load_config, get_enabled_topics, get_topic, ConfigError


class TestLoadConfig:
    def test_load_valid_config(self):
        """Test loading a valid YAML config."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({
                "global": {"schedule": "0 8 * * *", "max_total_items": 5},
                "topics": [{"name": "Test", "enabled": True, "max_items": 3}],
            }, f)
            f.flush()
            config = load_config(f.name)
            assert config["global"]["schedule"] == "0 8 * * *"
            assert len(config["topics"]) == 1
        os.unlink(f.name)

    def test_missing_file_raises_error(self):
        """Test that missing config file raises ConfigError."""
        with pytest.raises(ConfigError, match="not found"):
            load_config("/nonexistent/path/config.yaml")

    def test_invalid_yaml_raises_error(self):
        """Test that invalid YAML raises ConfigError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("{{invalid yaml{{{")
            f.flush()
            with pytest.raises(ConfigError, match="Invalid YAML"):
                load_config(f.name)
        os.unlink(f.name)


class TestGetEnabledTopics:
    def test_returns_only_enabled(self):
        config = {
            "topics": [
                {"name": "A", "enabled": True},
                {"name": "B", "enabled": False},
                {"name": "C", "enabled": True},
            ]
        }
        enabled = get_enabled_topics(config)
        assert len(enabled) == 2
        assert enabled[0]["name"] == "A"
        assert enabled[1]["name"] == "C"


class TestGetTopic:
    def test_case_insensitive_lookup(self):
        config = {"topics": [{"name": "Bitcoin", "enabled": True}]}
        assert get_topic(config, "bitcoin") is not None
        assert get_topic(config, "Bitcoin") is not None
        assert get_topic(config, "BITCOIN") is not None

    def test_missing_returns_none(self):
        config = {"topics": []}
        assert get_topic(config, "Nonexistent") is None
