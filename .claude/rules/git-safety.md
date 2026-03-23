---
paths:
  - "**"
---

# Git Rules (STRICTLY ENFORCED)

## Forbidden Actions (BLOCKED by hooks)

1. **No direct commits/merges to main/master**
   - Always use feature branches
   - Always create Pull Requests
   - Never `git merge` directly into main/master

2. **No Claude/AI mentions in commits**
   - No "Claude" in commit messages
   - No "Anthropic" in commit messages
   - No "Co-Authored-By: Claude" or similar
   - Keep commits looking human-authored

## Correct Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make commits (no AI mentions!)
git commit -m "Add user authentication endpoint"

# 3. Push to remote
git push -u origin feature/my-feature

# 4. Create PR via GitHub
gh pr create --title "Add user authentication" --body "..."
```

## Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**DO NOT include**: Claude, Anthropic, AI, Co-Authored-By: Claude, etc.
