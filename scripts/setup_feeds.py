"""Setup script for initial RSS feed configuration."""

import subprocess
import sys
import os

# Default feeds to set up
DEFAULT_FEEDS = [
    ("CoinDesk", "https://www.coindesk.com", "https://www.coindesk.com/arc/outboundfeeds/rss"),
    ("Bitcoin Magazine", "https://bitcoinmagazine.com", "https://bitcoinmagazine.com/feed"),
]


def find_blogwatcher():
    """Find blogwatcher-cli binary."""
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, "bin", "blogwatcher-cli.exe"),
        os.path.join(home, "AppData", "Local", "hermes", "profiles", "productivity", "home", "bin", "blogwatcher-cli.exe"),
        "blogwatcher-cli",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
        if c == "blogwatcher-cli":
            try:
                subprocess.run([c, "--help"], capture_output=True, timeout=5)
                return c
            except Exception:
                pass
    return None


def main():
    binary = find_blogwatcher()
    if not binary:
        print("ERROR: blogwatcher-cli not found.")
        print("Install it from: https://github.com/JulienTant/blogwatcher-cli")
        sys.exit(1)

    print(f"Using blogwatcher-cli: {binary}\n")

    # Add feeds
    for name, url, feed_url in DEFAULT_FEEDS:
        print(f"Adding feed: {name}...")
        try:
            result = subprocess.run(
                [binary, "add", name, url, "--feed-url", feed_url],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                print(f"  OK: {result.stdout.strip()}")
            else:
                print(f"  FAIL: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ERROR: {e}")

    # Scan all feeds
    print("\nScanning all feeds...")
    try:
        result = subprocess.run(
            [binary, "scan"],
            capture_output=True, text=True, timeout=60
        )
        print(result.stdout)
    except Exception as e:
        print(f"Scan error: {e}")


if __name__ == "__main__":
    main()
