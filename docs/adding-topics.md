# Adding Topics

## Quick Way (Admin CLI)

```bash
cd C:\hermes\PersonalProductivity
python -m productivity_agent.admin add-topic
```

## Manual Way (Edit YAML)

Add a new entry to the `topics` list in `config/news-monitor.yaml`:

```yaml
- name: "Artificial Intelligence"
  enabled: false           # start disabled
  max_items: 3
  summary: "AI developments and breakthroughs"

  rss_feeds:
    - "MIT Technology Review"
    - "The Verge AI"

  x_queries:
    - "artificial intelligence"
    - "AI breakthrough"
    - "ChatGPT OR Claude OR Gemini"

  x_allowed_handles:
    - "sama"
    - "ylecun"
    - "karpathy"
    - "AnthropicAI"
    - "OpenAI"

  keywords_include:
    - "AI"
    - "artificial intelligence"
    - "machine learning"
    - "LLM"
    - "GPT"
    - "Claude"
    - "Gemini"
    - "AGI"
    - "safety"
    - "regulation"

  keywords_exclude:
    - "crypto"
    - "NFT"
    - "shill"
    - "1000x"

  importance_rules: |
    Focus on: major model releases, safety research, regulatory actions,
    breakthrough research papers, major company announcements.
    Skip: minor product updates, opinion pieces without new information,
    promotional content.
```

Then enable it:
```bash
python -m productivity_agent.admin enable "Artificial Intelligence"
```

## Finding RSS Feeds

1. Check if the site has `/feed`, `/rss`, or `/atom.xml`
2. Use browser dev tools → Network tab → look for RSS/Atom links
3. Test with: `blogwatcher-cli add "Name" <url>`
4. If no RSS, use `--scrape-selector` with a CSS selector for article links

## Finding X Handles

1. Search X for your topic
2. Note which accounts consistently post high-quality content
3. Add them to `x_allowed_handles` for focused results
4. Add noisy accounts to `x_excluded_handles`
