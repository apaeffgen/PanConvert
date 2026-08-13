#!/usr/bin/env bash
# Quick script to run all tests with pytest
set -e
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

exec python -m pytest tests/ "$@"
