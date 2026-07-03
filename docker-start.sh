#!/bin/bash
# Double-click-friendly launcher for macOS/Linux.
# Ensures db.sqlite3 exists as a file before Docker touches it — if it's
# missing, Docker Compose's bind mount creates a directory there instead of a
# file, which breaks Django's migrate step on a brand-new machine.
cd "$(dirname "$0")"

if [ ! -f db.sqlite3 ]; then
    echo "No db.sqlite3 found — creating an empty one (Docker will set it up on first run)."
    touch db.sqlite3
fi

if [ ! -f credentials.json ]; then
    echo "ERROR: credentials.json is missing. Add it to this folder before running." >&2
    exit 1
fi

if [ ! -f .env ]; then
    echo "ERROR: .env is missing. Copy .env.example to .env and add your ANTHROPIC_API_KEY." >&2
    exit 1
fi

docker compose up --build
