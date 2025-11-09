#!/bin/bash
# Code quality check script

set -e

echo "🔍 Running code quality checks..."

echo "1️⃣ Black formatting..."
uv run black --check src/ tests/

echo "2️⃣ Ruff linting..."
uv run ruff check src/ tests/

echo "3️⃣ MyPy type checking..."
uv run mypy src/ || true

echo "✅ Code quality checks completed!"
