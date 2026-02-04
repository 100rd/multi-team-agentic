#!/bin/bash
# gem/commands/start-feature.sh - Orchestrate new feature development

set -e

echo "🚀 Starting new feature workflow (Gemini/Copilot Edition)..."

# 1. Gather Input (in a real interactive CLI, we'd use 'read', but here we assume args or context)
FEATURE_NAME=$1
if [ -z "$FEATURE_NAME" ]; then
    echo "❌ Error: Feature name required."
    echo "Usage: ./gem/commands/start-feature.sh <feature-name>"
    exit 1
fi

echo "📂 Creating feature context for: $FEATURE_NAME"

# 2. Simulate Worktree / Branch creation
git checkout -b "feature/$FEATURE_NAME"

# 3. Initialize feature directory in a temp or specific space if needed
# For this repo, we'll just log it
echo "Issue created: [Feature] $FEATURE_NAME" >> PROJECT_STATUS.md

# 4. Assign Agents (via context files)
cat <<EOF > "gem/current-task.json"
{
  "feature": "$FEATURE_NAME",
  "status": "in-progress",
  "agents": ["architecture-lead", "senior-backend-engineer"],
  "started_at": "$(date)"
}
EOF

echo "✅ Feature branch created and agents assigned."
echo "🤖 Gemini is now analyzing the impact..."
# Here we would normally call gemini-cli with a specific prompt
