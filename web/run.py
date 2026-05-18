#!/usr/bin/env python3
"""Run the InfoFunnel web application.

Usage:
    python web/run.py

Then open http://127.0.0.1:9090 in your browser.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path so `web` and `src` packages are findable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

PORT = 9090

if __name__ == "__main__":
    print(f"Starting InfoFunnel at http://127.0.0.1:{PORT}")
    print("Press Ctrl+C to stop")
    uvicorn.run(
        "web.app:app",
        host="127.0.0.1",
        port=PORT,
        reload=True,
        reload_dirs=["web", "config"],
    )
