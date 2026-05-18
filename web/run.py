#!/usr/bin/env python3
"""Run the InfoFunnel web application.

Usage:
    python web/run.py

Then open http://127.0.0.1:9090 in your browser.

If you get a port error, change PORT below or use:
    python -m uvicorn web.app:app --host 127.0.0.1 --port 9090 --reload
"""

import uvicorn

PORT = 9090  # Change if this port is in use on your machine

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
