#!/bin/bash
# Startup script for Panconvert
# Launches Panconvert from the virtual environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Launch Panconvert
exec "$SCRIPT_DIR/Panconvert" "$@"
