"""InfoFunnel Web Application - FastAPI interface for the news monitoring system."""

import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add src/ to path so we can import the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import yaml

from productivity_agent.config import load_config, get_topic, ConfigError, get_enabled_topics
from productivity_agent.sources.rss import RSSSource
from productivity_agent.filtering import FilterEngine
from productivity_agent.digest import DigestGenerator

# Determine project root (parent of web/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "news-monitor.yaml"

app = FastAPI(
    title="InfoFunnel",
    description="Personal news and information monitoring dashboard",
    version="0.1.0",
)

# Templates directory
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _load_config():
    """Load config with error handling."""
    try:
        return load_config(str(CONFIG_PATH))
    except ConfigError as e:
        raise HTTPException(status_code=500, detail=str(e))


def _save_config(config: dict):
    """Save config back to YAML file."""
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ─── HTML Pages ───────────────────────────────────────────────────────────────


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page showing all topics and their status."""
    config = _load_config()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "config": config,
            "config_path": str(CONFIG_PATH),
        },
    )


@app.get("/topic/{topic_name}", response_class=HTMLResponse)
async def topic_detail(request: Request, topic_name: str):
    """Detail page for a single topic."""
    config = _load_config()
    topic = get_topic(config, topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")
    return templates.TemplateResponse(
        request=request,
        name="topic.html",
        context={
            "topic": topic,
            "config_path": str(CONFIG_PATH),
        },
    )


@app.get("/digest", response_class=HTMLResponse)
async def digest_page(request: Request):
    """Show the latest digest results."""
    return templates.TemplateResponse(
        request=request,
        name="digest.html",
        context={
            "config": _load_config(),
        },
    )


# ─── API Endpoints ─────────────────────────────────────────────────────────────


@app.get("/api/topics")
async def api_list_topics():
    """Return all topics with their status."""
    config = _load_config()
    return {
        "global": config.get("global", {}),
        "topics": config.get("topics", []),
    }


@app.get("/api/topics/{topic_name}")
async def api_get_topic(topic_name: str):
    """Return a single topic's configuration."""
    config = _load_config()
    topic = get_topic(config, topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")
    return topic


@app.post("/api/topics/{topic_name}/enable")
async def api_enable_topic(topic_name: str):
    """Enable a topic."""
    config = _load_config()
    topic = get_topic(config, topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")
    topic["enabled"] = True
    _save_config(config)
    return {"status": "ok", "action": "enabled", "topic": topic_name}


@app.post("/api/topics/{topic_name}/disable")
async def api_disable_topic(topic_name: str):
    """Disable a topic."""
    config = _load_config()
    topic = get_topic(config, topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")
    topic["enabled"] = False
    _save_config(config)
    return {"status": "ok", "action": "disabled", "topic": topic_name}


@app.delete("/api/topics/{topic_name}")
async def api_delete_topic(topic_name: str):
    """Delete a topic permanently."""
    config = _load_config()
    topic = get_topic(config, topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")
    config["topics"] = [t for t in config["topics"] if t["name"].lower() != topic_name.lower()]
    _save_config(config)
    return {"status": "ok", "action": "deleted", "topic": topic_name}


@app.post("/api/topics")
async def api_add_topic(
    name: str = Form(...),
    summary: str = Form(""),
    max_items: int = Form(3),
):
    """Add a new topic."""
    config = _load_config()

    # Check for duplicates
    if get_topic(config, name):
        raise HTTPException(status_code=409, detail=f"Topic '{name}' already exists")

    new_topic = {
        "name": name,
        "enabled": False,
        "max_items": max_items,
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
    _save_config(config)
    return {"status": "ok", "action": "created", "topic": name}


@app.get("/api/topics/{topic_name}/test")
async def api_test_topic(topic_name: str):
    """Show what searches would run for a topic (dry run)."""
    config = _load_config()
    topic = get_topic(config, topic_name)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")

    return {
        "topic": topic_name,
        "rss_feeds": topic.get("rss_feeds", []),
        "x_queries": [
            {
                "query": q,
                "allowed_handles": topic.get("x_allowed_handles", []),
                "excluded_handles": topic.get("x_excluded_handles", []),
            }
            for q in topic.get("x_queries", [])
        ],
        "keywords_include": topic.get("keywords_include", []),
        "keywords_exclude": topic.get("keywords_exclude", []),
        "importance_rules": topic.get("importance_rules", ""),
        "max_items": topic.get("max_items", 3),
    }


@app.post("/api/digest/run")
async def api_run_digest():
    """Run a digest scan across all enabled topics and return results."""
    config = _load_config()
    enabled_topics = get_enabled_topics(config)

    if not enabled_topics:
        return {"status": "ok", "message": "No enabled topics to scan", "digest": ""}

    # Initialize sources
    rss_source = RSSSource()

    # Collect items per topic
    topic_results = {}
    errors = []

    for topic in enabled_topics:
        topic_name = topic["name"]
        all_items = []

        # Fetch RSS items
        try:
            rss_items = rss_source.fetch(topic, since=datetime.now() - timedelta(hours=24))
            all_items.extend(rss_items)
        except Exception as e:
            errors.append(f"RSS error for {topic_name}: {e}")

        # Apply filters
        engine = FilterEngine(topic)
        filtered = engine.filter_items(all_items)
        topic_results[topic_name] = filtered

    # Generate digest
    generator = DigestGenerator(config)
    digest_text = generator.generate(topic_results)

    return {
        "status": "ok",
        "topics_scanned": len(enabled_topics),
        "total_items": sum(len(items) for items in topic_results.values()),
        "errors": errors,
        "digest": digest_text,
    }


@app.get("/api/config")
async def api_get_config():
    """Return the full configuration."""
    return _load_config()


def create_app():
    """Factory function for creating the app (used by uvicorn)."""
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.app:app", host="127.0.0.1", port=9090, reload=True)
