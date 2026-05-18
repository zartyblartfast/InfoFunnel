#!/usr/bin/env python3
"""
news-monitor-admin -- Admin tool for Hermes Personal Information Monitor

Usage:
    python news-monitor-admin.py list                  # Show all topics and status
    python news-monitor-admin.py enable <topic>        # Enable a topic
    python news-monitor-admin.py disable <topic>       # Disable a topic
    python news-monitor-admin.py add-topic             # Interactive: add a new topic
    python news-monitor-admin.py add-feed <topic>      # Interactive: add RSS feed to topic
    python news-monitor-admin.py add-handle <topic>    # Interactive: add X handle to topic
    python news-monitor-admin.py add-query <topic>     # Interactive: add X query to topic
    python news-monitor-admin.py remove-feed <topic>   # Interactive: remove RSS feed
    python news-monitor-admin.py remove-handle <topic> # Interactive: remove X handle
    python news-monitor-admin.py test <topic>          # Run a test digest for a topic
    python news-monitor-admin.py config                # Show config file path
"""

import sys
import os
import yaml

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "news-monitor.yaml"
)


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"Config saved to {CONFIG_PATH}")


def find_topic(config, name):
    for topic in config.get("topics", []):
        if topic["name"].lower() == name.lower():
            return topic
    return None


def cmd_list(config):
    print("\n=== News Monitor Topics ===\n")
    global_settings = config.get("global", {})
    print(f"Schedule: {global_settings.get('schedule', 'not set')}")
    print(f"Delivery: {global_settings.get('delivery', 'not set')}")
    print(f"Max total items: {global_settings.get('max_total_items', 'not set')}")
    print(f"Quiet hours: {global_settings.get('quiet_hours', 'none')}")
    print()

    for topic in config.get("topics", []):
        status = "ENABLED" if topic.get("enabled") else "DISABLED"
        print(f"  [{status}] {topic['name']}")
        print(f"    Summary: {topic.get('summary', 'N/A')}")
        print(f"    Max items: {topic.get('max_items', 'N/A')}")
        feeds = topic.get("rss_feeds", [])
        print(f"    RSS feeds: {', '.join(feeds) if feeds else 'none'}")
        queries = topic.get("x_queries", [])
        print(f"    X queries: {len(queries)} configured")
        handles = topic.get("x_allowed_handles", [])
        print(f"    X allowed handles: {len(handles)} configured")
        inc_kw = topic.get("keywords_include", [])
        exc_kw = topic.get("keywords_exclude", [])
        print(f"    Include keywords: {len(inc_kw)} | Exclude keywords: {len(exc_kw)}")
        print()


def cmd_enable(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return
    topic["enabled"] = True
    save_config(config)
    print(f"Enabled topic: {topic['name']}")


def cmd_disable(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return
    topic["enabled"] = False
    save_config(config)
    print(f"Disabled topic: {topic['name']}")


def cmd_add_topic(config):
    print("\n=== Add New Topic ===\n")
    name = input("Topic name (e.g., 'Artificial Intelligence'): ").strip()
    if not name:
        print("Cancelled.")
        return

    if find_topic(config, name):
        print(f"Topic '{name}' already exists.")
        return

    summary = input("Brief summary: ").strip()
    max_items = input("Max items per digest [3]: ").strip() or "3"

    new_topic = {
        "name": name,
        "enabled": False,  # start disabled until feeds/queries are configured
        "max_items": int(max_items),
        "summary": summary or f"{name} developments",
        "rss_feeds": [],
        "x_queries": [],
        "x_allowed_handles": [],
        "x_excluded_handles": [],
        "keywords_include": [],
        "keywords_exclude": [],
        "importance_rules": f"Define what counts as important for {name}.\nInclude: major developments, breakthroughs, regulatory changes.\nExclude: minor updates, speculation, memes.",
    }

    config["topics"].append(new_topic)
    save_config(config)
    print(f"\nAdded topic: {name}")
    print("Next steps:")
    print(f"  1. Add RSS feeds:  python {sys.argv[0]} add-feed \"{name}\"")
    print(f"  2. Add X queries:  python {sys.argv[0]} add-query \"{name}\"")
    print(f"  3. Add X handles:  python {sys.argv[0]} add-handle \"{name}\"")
    print(f"  4. Enable:         python {sys.argv[0]} enable \"{name}\"")


def cmd_add_feed(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return

    feed_name = input(f"RSS feed name for {topic_name} (must match blogwatcher-cli name): ").strip()
    if not feed_name:
        print("Cancelled.")
        return

    if feed_name in topic.get("rss_feeds", []):
        print(f"Feed '{feed_name}' already exists for {topic_name}.")
        return

    topic.setdefault("rss_feeds", []).append(feed_name)
    save_config(config)
    print(f"Added RSS feed '{feed_name}' to {topic_name}")
    print(f"Make sure blogwatcher-cli has this feed: blogwatcher-cli add \"{feed_name}\" <url>")


def cmd_add_query(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return

    query = input(f"X search query for {topic_name}: ").strip()
    if not query:
        print("Cancelled.")
        return

    if query in topic.get("x_queries", []):
        print(f"Query already exists.")
        return

    topic.setdefault("x_queries", []).append(query)
    save_config(config)
    print(f"Added X query to {topic_name}: {query}")


def cmd_add_handle(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return

    handle = input(f"X handle to add (without @): ").strip().lstrip("@")
    if not handle:
        print("Cancelled.")
        return

    allowed = topic.get("x_allowed_handles", [])
    excluded = topic.get("x_excluded_handles", [])

    if handle in allowed:
        print(f"Handle @{handle} already in allowed list.")
        return
    if handle in excluded:
        print(f"Handle @{handle} is in excluded list. Remove it first.")
        return

    scope = input("Add to (1) allowed list or (2) excluded list? [1]: ").strip() or "1"
    if scope == "2":
        topic.setdefault("x_excluded_handles", []).append(handle)
        print(f"Added @{handle} to excluded handles for {topic_name}")
    else:
        topic.setdefault("x_allowed_handles", []).append(handle)
        print(f"Added @{handle} to allowed handles for {topic_name}")

    save_config(config)


def cmd_remove_feed(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return

    feeds = topic.get("rss_feeds", [])
    if not feeds:
        print("No RSS feeds configured.")
        return

    print("Current feeds:")
    for i, f in enumerate(feeds, 1):
        print(f"  {i}. {f}")

    choice = input("Remove which (number or name)? ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(feeds):
        removed = feeds.pop(int(choice) - 1)
    elif choice in feeds:
        feeds.remove(choice)
        removed = choice
    else:
        print("Not found.")
        return

    save_config(config)
    print(f"Removed feed: {removed}")


def cmd_remove_handle(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return

    allowed = topic.get("x_allowed_handles", [])
    excluded = topic.get("x_excluded_handles", [])
    all_handles = [(h, "allowed") for h in allowed] + [(h, "excluded") for h in excluded]

    if not all_handles:
        print("No handles configured.")
        return

    print("Current handles:")
    for i, (h, scope) in enumerate(all_handles, 1):
        print(f"  {i}. @{h} ({scope})")

    choice = input("Remove which (number or handle)? ").strip().lstrip("@")
    if choice.isdigit() and 1 <= int(choice) <= len(all_handles):
        handle, scope = all_handles[int(choice) - 1]
    else:
        handle = choice
        scope = None
        for h, s in all_handles:
            if h == handle:
                scope = s
                break

    if scope == "allowed" and handle in allowed:
        allowed.remove(handle)
        print(f"Removed @{handle} from allowed handles")
    elif scope == "excluded" and handle in excluded:
        excluded.remove(handle)
        print(f"Removed @{handle} from excluded handles")
    else:
        print("Not found.")
        return

    save_config(config)


def cmd_test(config, topic_name):
    topic = find_topic(config, topic_name)
    if not topic:
        print(f"Topic '{topic_name}' not found.")
        return

    print(f"\n=== Test Digest: {topic['name']} ===\n")
    print(f"This would run the following searches for '{topic['name']}':")
    print()

    print("RSS feeds to scan:")
    for f in topic.get("rss_feeds", []):
        print(f"  - {f}")
    if not topic.get("rss_feeds"):
        print("  (none configured)")

    print()
    print("X searches to run:")
    for q in topic.get("x_queries", []):
        handles = topic.get("x_allowed_handles", [])
        handle_filter = f" (from: {', '.join(handles)})" if handles else ""
        print(f"  - x_search: \"{q}\"{handle_filter}")
    if not topic.get("x_queries"):
        print("  (none configured)")

    print()
    print("Include keywords:", ", ".join(topic.get("keywords_include", [])) or "(any)")
    print("Exclude keywords:", ", ".join(topic.get("keywords_exclude", [])) or "(none)")
    print()
    print("Importance rules:")
    print(topic.get("importance_rules", "Not defined"))
    print()
    print(f"Max items: {topic.get('max_items', 3)}")
    print()
    print("To run an actual test, use:")
    print(f'  hermes chat -q "Run a test digest for {topic_name} using the news monitor config at {CONFIG_PATH}"')


def cmd_config():
    print(f"Config file: {CONFIG_PATH}")
    print(f"Exists: {os.path.exists(CONFIG_PATH)}")


COMMANDS = {
    "list": cmd_list,
    "enable": cmd_enable,
    "disable": cmd_disable,
    "add-topic": cmd_add_topic,
    "add-feed": cmd_add_feed,
    "add-query": cmd_add_query,
    "add-handle": cmd_add_handle,
    "remove-feed": cmd_remove_feed,
    "remove-handle": cmd_remove_handle,
    "test": cmd_test,
    "config": cmd_config,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return

    command = sys.argv[1]
    handler = COMMANDS.get(command)

    if not handler:
        print(f"Unknown command: {command}")
        print("Run with --help for usage.")
        sys.exit(1)

    config = load_config()

    # Commands that need a topic name
    topic_commands = {"enable", "disable", "add-feed", "add-query", "add-handle", "remove-feed", "remove-handle", "test"}
    if command in topic_commands:
        if len(sys.argv) < 3:
            print(f"Usage: {sys.argv[0]} {command} <topic_name>")
            sys.exit(1)
        handler(config, sys.argv[2])
    else:
        handler(config)


if __name__ == "__main__":
    main()
