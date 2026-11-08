#!/usr/bin/env python3
"""
NyayaSetu - Prototype Launcher
Run `python3 run_app.py` to start the interactive web application.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from nyayasetu.app.server import start_server

if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    print("=" * 70)
    print("⚖️  NyayaSetu (न्याय सेतु) - AI Legal Navigator for Indian Everyday Rights")
    print("=" * 70)
    start_server(port)
