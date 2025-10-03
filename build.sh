#!/bin/bash
# Build script wrapper for Legs on the Ground site
# Activates venv and runs build.py

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "📦 Installing dependencies..."
    ./venv/bin/pip install -q jinja2 pyyaml markdown
fi

# Run build
./venv/bin/python build.py "$@"
