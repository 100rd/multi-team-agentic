#!/bin/bash

# Claude Code Agent Generator Setup Script

echo "=== Claude Code Agent Generator Setup ==="
echo

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 found"

# Create necessary directories
echo "Creating directory structure..."
mkdir -p .claude/agents
mkdir -p templates
mkdir -p scripts
mkdir -p docs

echo "✓ Directories created"

# Check if PROJECT.md exists
if [ ! -f "PROJECT.md" ]; then
    echo
    echo "PROJECT.md not found. Creating from template..."
    cp PROJECT.md PROJECT.md.example 2>/dev/null || true
    echo "✓ PROJECT.md created"
    echo
    echo "Next steps:"
    echo "1. Edit PROJECT.md with your project details"
    echo "2. Run: python scripts/generate-agents.py"
else
    echo "✓ PROJECT.md exists"
fi

# Make scripts executable
chmod +x scripts/generate-agents.py 2>/dev/null || true

echo
echo "Setup complete!"
echo
echo "To generate agents for your project:"
echo "1. Edit PROJECT.md with your project information"
echo "2. Run: python scripts/generate-agents.py"
echo "3. Find your agents in .claude/agents/"
echo
echo "For more information, see:"
echo "- README.md for overview"
echo "- docs/AGENT_GUIDELINES.md for creating effective agents"
echo "- docs/EXAMPLE_USAGE.md for usage examples"