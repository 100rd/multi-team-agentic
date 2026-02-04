#!/bin/bash
# Setup Git Hooks for Enterprise Workflow Automation

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Git hooks for enterprise workflow...${NC}"

# Create hooks directory if it doesn't exist
HOOKS_DIR=".git/hooks"
mkdir -p "$HOOKS_DIR"

# Pre-commit hook - Branch protection + Code quality checks
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook: Branch protection + code quality

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# ============================================
# RULE 1: Block direct commits to main/master
# ============================================
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo ""
    echo "❌ BLOCKED: Direct commits to '$BRANCH' are forbidden."
    echo ""
    echo "   Create a feature branch instead:"
    echo "     git checkout -b feature/your-feature"
    echo "     git commit -m 'your message'"
    echo "     git push -u origin feature/your-feature"
    echo "     gh pr create"
    echo ""
    exit 1
fi

# ============================================
# RULE 2: Block sensitive files from commit
# ============================================
SENSITIVE_FILES=$(git diff --cached --name-only | grep -E '\.(env|pem|key|p12|pfx|credentials|secret)$' || true)
if [ -n "$SENSITIVE_FILES" ]; then
    echo ""
    echo "❌ BLOCKED: Sensitive files detected in commit:"
    echo "$SENSITIVE_FILES"
    echo ""
    echo "   Remove them with: git reset HEAD <file>"
    echo "   Add to .gitignore if needed."
    echo ""
    exit 1
fi

# ============================================
# RULE 3: Scan for hardcoded secrets
# ============================================
if git diff --cached -U0 | grep -qiE '(password|secret|api_key|apikey|token|private_key)\s*[:=]\s*["\x27][^$\{]'; then
    echo ""
    echo "⚠️ WARNING: Potential hardcoded secret detected in staged changes."
    echo "   Use environment variables or a secret manager instead."
    echo ""
    # Warning only, not blocking - some may be variable names
fi

echo "🔍 Running pre-commit checks..."

# Check for Python files
if git diff --cached --name-only | grep -q '\.py$'; then
    echo "→ Running Python linting..."
    if command -v flake8 &> /dev/null; then
        git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | xargs flake8
    fi

    echo "→ Running Python tests..."
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short || exit 1
    fi
fi

# Check for JavaScript/TypeScript files
if git diff --cached --name-only | grep -qE '\.(js|ts|jsx|tsx)$'; then
    echo "→ Running ESLint..."
    if command -v eslint &> /dev/null; then
        git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|jsx|tsx)$' | xargs eslint
    fi
fi

# Terraform format check
if git diff --cached --name-only | grep -qE '\.tf$'; then
    echo "→ Checking Terraform formatting..."
    if command -v terraform &> /dev/null; then
        terraform fmt -check -recursive . || {
            echo "❌ Terraform files not formatted. Run: terraform fmt -recursive"
            exit 1
        }
    fi
fi

# Security scan
echo "→ Running security scan..."
if command -v git-secrets &> /dev/null; then
    git secrets --pre_commit_hook -- "$@"
fi

# Check for large files
echo "→ Checking file sizes..."
for file in $(git diff --cached --name-only); do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        if [ $size -gt 5242880 ]; then  # 5MB
            echo "❌ Error: $file is larger than 5MB"
            exit 1
        fi
    fi
done

echo "✅ Pre-commit checks passed!"
EOF

# Pre-push hook - Block push to main/master + comprehensive checks
cat > "$HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# Pre-push hook: Branch protection + comprehensive checks

BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE="$1"

# ============================================
# RULE 1: Block pushing to main/master
# ============================================
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo ""
    echo "❌ BLOCKED: Pushing directly to '$BRANCH' is forbidden."
    echo ""
    echo "   Use a feature branch and create a Pull Request:"
    echo "     git checkout -b feature/your-feature"
    echo "     git push -u origin feature/your-feature"
    echo "     gh pr create"
    echo ""
    exit 1
fi

# Also block if pushing TO main/master remote ref
while read local_ref local_sha remote_ref remote_sha; do
    if echo "$remote_ref" | grep -qE "refs/heads/(main|master)$"; then
        echo ""
        echo "❌ BLOCKED: Pushing to remote main/master is forbidden."
        echo "   Create a Pull Request instead."
        echo ""
        exit 1
    fi
done

echo "🚀 Running pre-push checks..."

# Run all tests
echo "→ Running full test suite..."
if [ -f "Makefile" ] && grep -q "test:" Makefile; then
    make test || exit 1
elif [ -f "package.json" ]; then
    npm test || exit 1
elif [ -f "requirements.txt" ]; then
    pytest || exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: You have uncommitted changes"
fi

# Verify no merge conflicts markers
if git diff HEAD --name-only | xargs grep -l '^<<<<<<< \|^======= \|^>>>>>>> ' 2>/dev/null; then
    echo "❌ Error: Merge conflict markers found!"
    exit 1
fi

# Scan all commits being pushed for Claude/AI mentions
COMMITS=$(git log "$REMOTE"/$(git rev-parse --abbrev-ref HEAD)..HEAD --format="%H" 2>/dev/null)
for commit in $COMMITS; do
    MSG=$(git log --format="%B" -n 1 "$commit")
    if echo "$MSG" | grep -qiE "claude|anthropic|co-authored-by.*(claude|anthropic)"; then
        echo ""
        echo "❌ BLOCKED: Commit $commit contains AI/Claude references."
        echo "   Amend or rebase to remove: git rebase -i HEAD~N"
        echo ""
        exit 1
    fi
done

echo "✅ Pre-push checks passed!"
EOF

# Post-merge hook - Update dependencies and notify
cat > "$HOOKS_DIR/post-merge" << 'EOF'
#!/bin/bash
# Post-merge hook: Update dependencies and notify team

echo "🔄 Running post-merge tasks..."

# Update dependencies if package files changed
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "requirements.txt"; then
    echo "→ Python dependencies changed, updating..."
    pip install -r requirements.txt
fi

if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "package.json"; then
    echo "→ Node dependencies changed, updating..."
    npm install
fi

# Notify about migration needs
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q "migrations/"; then
    echo "⚠️  Database migrations detected! Remember to run migrations."
fi

# Update agent registry if agents changed
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q ".claude/agents/"; then
    echo "🤖 Agent definitions changed. Orchestrator will reload agents."
fi

echo "✅ Post-merge tasks completed!"
EOF

# Commit-msg hook - Enforce commit message standards + block AI mentions
cat > "$HOOKS_DIR/commit-msg" << 'EOF'
#!/bin/bash
# Commit-msg hook: Enforce format + block AI mentions

MSG=$(cat "$1")

# ============================================
# RULE 1: Block Claude/AI mentions in commits
# ============================================
if echo "$MSG" | grep -qiE "claude|anthropic|co-authored-by.*claude|co-authored-by.*anthropic|generated by ai|ai-generated|openai|chatgpt"; then
    echo ""
    echo "❌ BLOCKED: Commit message contains AI/Claude references."
    echo ""
    echo "   Remove these from your commit message:"
    echo "     - Claude, Anthropic"
    echo "     - Co-Authored-By: Claude"
    echo "     - Any AI tool mentions"
    echo ""
    echo "   Commits must appear human-authored."
    echo ""
    exit 1
fi

# ============================================
# RULE 2: Conventional commit format
# ============================================
commit_regex='^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert)(\(.+\))?: .{1,50}'

if ! echo "$MSG" | head -1 | grep -qE "$commit_regex"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Commit message must follow conventional format:"
    echo "  <type>(<scope>): <subject>"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, test, chore, build, ci, perf, revert"
    echo ""
    echo "Example: feat(auth): add OAuth2 integration"
    echo ""
    exit 1
fi

# ============================================
# RULE 3: Check message length
# ============================================
first_line=$(head -n1 "$1")
if [ ${#first_line} -gt 72 ]; then
    echo "❌ Commit message first line is too long (${#first_line} > 72 characters)"
    exit 1
fi

echo "✅ Commit message validated!"
EOF

# Make all hooks executable
chmod +x "$HOOKS_DIR"/*

# Create workflow automation script
cat > "scripts/workflow-automation.sh" << 'EOF'
#!/bin/bash
# Workflow automation helpers

# Function to check if PR is ready for review
check_pr_ready() {
    echo "🔍 Checking if PR is ready for review..."
    
    # Check if all tests pass
    if ! make test > /dev/null 2>&1; then
        echo "❌ Tests are failing"
        return 1
    fi
    
    # Check code coverage
    coverage=$(pytest --cov=. --cov-report=term | grep TOTAL | awk '{print $4}' | sed 's/%//')
    if [ "$coverage" -lt 80 ]; then
        echo "❌ Code coverage is below 80% (current: $coverage%)"
        return 1
    fi
    
    # Check for TODO comments
    if grep -r "TODO\|FIXME\|XXX" --include="*.py" --include="*.js" --include="*.ts" .; then
        echo "⚠️  Warning: TODO/FIXME comments found"
    fi
    
    echo "✅ PR is ready for review!"
    return 0
}

# Function to notify about long-running PRs
check_stale_prs() {
    echo "🕒 Checking for stale PRs..."
    
    if command -v gh &> /dev/null; then
        gh pr list --json number,title,createdAt --jq '.[] | select((.createdAt | fromdateiso8601) < (now - 3*24*60*60)) | "PR #\(.number): \(.title) is over 3 days old"'
    fi
}

# Export functions
export -f check_pr_ready
export -f check_stale_prs
EOF

chmod +x scripts/workflow-automation.sh

echo -e "${GREEN}✅ Git hooks setup complete!${NC}"
echo ""
echo "Hooks installed:"
echo "  • pre-commit   - Code quality checks"
echo "  • pre-push     - Comprehensive testing"
echo "  • post-merge   - Dependency updates"
echo "  • commit-msg   - Message format validation"
echo ""
echo "To bypass hooks (emergency only): git commit --no-verify"