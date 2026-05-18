"""InfoFunnel Web Application - FastAPI interface for the news monitoring system."""

import os
import sys
from pathlib import Path

# Add src/ to path so we can import the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yaml

from productivity_agent.config import load_config, get_topic, ConfigError

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


@app.get("/api/config")
async def api_get_config():
    """Return the full configuration."""
    return _load_config()


def create_app():
    """Factory function for creating the app (used by uvicorn)."""
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=True)
