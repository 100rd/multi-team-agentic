#!/bin/bash
# gem/commands/auto-fix.sh - The "Think-Act-Verify" Loop

FILE_TO_FIX=$1
TEST_COMMAND=$2

echo "🤖 Starting Auto-Fix loop for $FILE_TO_FIX..."

# 1. Run Tests
echo "🧪 Running: $TEST_COMMAND..."
ERROR_LOG=$(eval $TEST_COMMAND 2>&1)

if [ $? -eq 0 ]; then
    echo "✅ Verification Passed! The code is solid."
    exit 0
fi

echo "❌ Verification Failed. Analysis of error log:"
echo "$ERROR_LOG" | head -n 20

# 2. Instruct the Agent to fix it
echo "🤖 REQUESTING REPAIR: Gemini is analyzing the error log to apply a fix..."
# In a real CLI environment, the next interaction would automatically include this log
# We write it to a temp file for the agent to pick up in its context
echo "$ERROR_LOG" > .gemini/last_error.log

