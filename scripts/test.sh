#!/bin/bash
# Testing script

set -e

echo "🧪 Running tests..."

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing --cov-report=html

echo "✅ Tests completed!"
echo "📊 Coverage report: htmlcov/index.html"
