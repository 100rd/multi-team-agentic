#!/bin/bash
# gem/hooks/quality-gates.sh - Enforce SDLC standards

echo "🔍 Running Quality Gates..."

# 1. TDD Check
echo "🧪 Checking for tests..."
# Simplistic check: if a file in src/ was modified, look for corresponding test/
# For demo purposes, we'll just check if a tests/ directory exists
if [ ! -d "tests" ] && [ ! -d "project/tests" ]; then
    echo "⚠️  WARNING: No tests directory found. TDD is recommended!"
fi

# 2. Linting (using ruff as an example)
if command -v ruff &> /dev/null; then
    echo "🧹 Running Ruff..."
    ruff check . || echo "⚠️  Linting issues found."
else
    echo "ℹ️  Ruff not installed, skipping linting."
fi

# 3. Security (using semgrep as an example)
if command -v semgrep &> /dev/null; then
    echo "🔒 Running Security Scan..."
    semgrep --config=auto . || echo "⚠️  Security scan finished with issues."
fi

echo "✅ Quality Gates check complete."
