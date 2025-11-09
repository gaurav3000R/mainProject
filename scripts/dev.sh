#!/bin/bash
# Development startup script

set -e

echo "🚀 Starting Agentic AI Platform..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please update .env with your API keys before running!"
    exit 1
fi

# Sync dependencies
echo "📦 Installing dependencies with UV..."
uv sync

# Run the server
echo "🌐 Starting FastAPI server..."
uv run python main.py
