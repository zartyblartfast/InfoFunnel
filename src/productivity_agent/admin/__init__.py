"""Admin CLI for managing the news monitor."""

import click
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from productivity_agent.config import load_config, get_enabled_topics, get_topic, ConfigError


@click.group()
@click.option("--config", "-c", default=None, help="Path to config file")
@click.pass_context
def cli(ctx, config):
    """Personal Productivity Agent - Admin CLI"""
    ctx.ensure_object(dict)
    try:
        ctx.obj["config"] = load_config(config)
        ctx.obj["config_path"] = str(config) if config else "config/news-monitor.yaml"
    except ConfigError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    """List all topics and their status."""
    config = ctx.obj["config"]
    global_settings = config.get("global", {})

    click.echo("\n=== News Monitor Topics ===\n")
    click.echo(f"Schedule: {global_settings.get('schedule', 'not set')}")
    click.echo(f"Delivery: {global_settings.get('delivery', 'not set')}")
    click.echo(f"Max total items: {global_settings.get('max_total_items', 'not set')}")
    click.echo(f"Quiet hours: {global_settings.get('quiet_hours', 'none')}")
    click.echo()

    for topic in config.get("topics", []):
        status = "ENABLED" if topic.get("enabled") else "DISABLED"
        click.echo(f"  [{status}] {topic['name']}")
        click.echo(f"    Summary: {topic.get('summary', 'N/A')}")
        click.echo(f"    Max items: {topic.get('max_items', 'N/A')}")
        feeds = topic.get("rss_feeds", [])
        click.echo(f"    RSS feeds: {', '.join(feeds) if feeds else 'none'}")
        queries = topic.get("x_queries", [])
        click.echo(f"    X queries: {len(queries)} configured")
        handles = topic.get("x_allowed_handles", [])
        click.echo(f"    X allowed handles: {len(handles)} configured")
        inc_kw = topic.get("keywords_include", [])
        exc_kw = topic.get("keywords_exclude", [])
        click.echo(f"    Include keywords: {len(inc_kw)} | Exclude keywords: {len(exc_kw)}")
        click.echo()


@cli.command()
@click.argument("topic_name")
@click.pass_context
def enable(ctx, topic_name):
    """Enable a topic."""
    _update_topic_enabled(ctx.obj["config"], ctx.obj["config_path"], topic_name, True)


@cli.command()
@click.argument("topic_name")
@click.pass_context
def disable(ctx, topic_name):
    """Disable a topic."""
    _update_topic_enabled(ctx.obj["config"], ctx.obj["config_path"], topic_name, False)


def _update_topic_enabled(config, config_path, topic_name, enabled):
    import yaml
    topic = get_topic(config, topic_name)
    if not topic:
        click.echo(f"Topic '{topic_name}' not found.", err=True)
        sys.exit(1)
    topic["enabled"] = enabled
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    state = "Enabled" if enabled else "Disabled"
    click.echo(f"{state} topic: {topic['name']}")


@cli.command()
@click.argument("topic_name")
@click.pass_context
def test(ctx, topic_name):
    """Show what searches would run for a topic (dry run)."""
    config = ctx.obj["config"]
    topic = get_topic(config, topic_name)
    if not topic:
        click.echo(f"Topic '{topic_name}' not found.", err=True)
        sys.exit(1)

    click.echo(f"\n=== Test Digest: {topic['name']} ===\n")
    click.echo(f"This would run the following searches for '{topic['name']}':")
    click.echo()

    click.echo("RSS feeds to scan:")
    for f in topic.get("rss_feeds", []):
        click.echo(f"  - {f}")
    if not topic.get("rss_feeds"):
        click.echo("  (none configured)")

    click.echo()
    click.echo("X searches to run:")
    for q in topic.get("x_queries", []):
        handles = topic.get("x_allowed_handles", [])
        handle_filter = f" (from: {', '.join(handles)})" if handles else ""
        click.echo(f"  - x_search: \"{q}\"{handle_filter}")
    if not topic.get("x_queries"):
        click.echo("  (none configured)")

    click.echo()
    click.echo(f"Include keywords: {', '.join(topic.get('keywords_include', [])) or '(any)'}")
    click.echo(f"Exclude keywords: {', '.join(topic.get('keywords_exclude', [])) or '(none)'}")
    click.echo()
    click.echo("Importance rules:")
    click.echo(topic.get("importance_rules", "Not defined"))
    click.echo()
    click.echo(f"Max items: {topic.get('max_items', 3)}")


@cli.command()
@click.pass_context
def config(ctx):
    """Show config file path."""
    click.echo(f"Config file: {ctx.obj['config_path']}")


def main():
    cli()


if __name__ == "__main__":
    main()
