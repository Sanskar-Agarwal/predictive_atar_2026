@echo off
REM Double-click-friendly launcher for Windows.
REM Ensures db.sqlite3 exists as a file before Docker touches it -- if it's
REM missing, Docker Compose's bind mount creates a directory there instead of
REM a file, which breaks Django's migrate step on a brand-new machine.
cd /d "%~dp0"

if not exist db.sqlite3 (
    echo No db.sqlite3 found - creating an empty one ^(Docker will set it up on first run^).
    type nul > db.sqlite3
)

if not exist credentials.json (
    echo ERROR: credentials.json is missing. Add it to this folder before running.
    pause
    exit /b 1
)

if not exist .env (
    echo ERROR: .env is missing. Copy .env.example to .env and add your ANTHROPIC_API_KEY.
    pause
    exit /b 1
)

docker compose up --build
pause
