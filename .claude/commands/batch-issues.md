---
name: batch-issues
description: Fetch GitHub issues and spawn parallel coding+QA agent pairs to process them concurrently
args: "<repo> [--label LABEL] [--milestone NAME] [--limit N] [--max-agents N] [--qa] [--dry-run]"
---

# Batch Issues Command

Processes multiple GitHub issues in parallel by spawning one coding agent per issue (with optional QA pairing). Designed for sprint backlog processing, bulk bug fixes, and batch feature implementation.

## What This Command Does

1. **Fetches issues** from a GitHub repository (filtered by label, milestone, etc.)
2. **Calculates agent count** — `min(issue_count, max_agents)`
3. **Spawns parallel agent pairs** — one coder + one QA per issue
4. **Each pair works independently** in an isolated worktree
5. **Creates one Draft PR per issue** when complete
6. **Reports summary** — N succeeded, M failed, K skipped

## Execution Flow

### Phase 1: Issue Discovery

```bash
# Fetch issues
gh issue list --repo REPO --label LABEL --state open --limit N \
  --json number,title,body,labels,milestone

# Calculate
num_issues = len(issues)
num_agents = min(num_issues, max_agents)  # default max_agents = 5
```

The Lead (opus) analyzes each issue and determines:
- Agent type based on issue labels (see mapping below)
- Complexity estimate (simple/medium/complex)
- Skip if insufficient context in issue body

### Phase 2: Parallel Execution (per issue)

For each issue, in parallel (up to `max_agents` concurrent):

```
1. Create worktree branch: feature/issue-{number}-{slug}
2. Spawn Coder agent (sonnet, worktree isolation)
   - Reads issue body as task description
   - Writes code following project patterns
   - Runs verification loop (fmt/validate/tflint/checkov/plan for TF)
   - Reports completion to Lead
3. If --qa flag:
   Spawn QA agent (sonnet, reads coder's worktree)
   - Reviews code quality, tests, security
   - Reports findings or approves
   - If findings: Coder fixes -> QA re-reviews (max 3 cycles)
4. Create Draft PR:
   gh pr create --draft --title "fix: #{number} {title}" \
     --body "Fixes #{number}\n\n{summary}"
```

### Phase 3: Collection

```
Lead collects results from all pairs:
- For each completed: PR URL + summary
- For each failed: error reason + issue number
- For each skipped: skip reason

Report to user:
  Processed: N issues
  Succeeded: X (PR URLs listed)
  Failed: Y (reasons listed)
  Skipped: Z (reasons listed)
```

## Agent Type Selection by Issue Label

| Issue Label(s) | Agent Type | Verification |
|----------------|-----------|--------------|
| `terraform`, `infrastructure`, `iac` | terraform-engineer | fmt/validate/tflint/checkov/plan loop |
| `backend`, `api`, `server` | senior-backend-engineer | lint + test |
| `frontend`, `ui`, `react` | senior-frontend-engineer | lint + test + build |
| `devops`, `ci-cd`, `pipeline` | devops-engineer | lint + validate |
| `security` | security-expert | checkov + tfsec |
| `fullstack`, `feature` | fullstack-engineer | lint + test |
| (no matching label) | fullstack-engineer | lint + test |

## Concurrency Control

- `--max-agents N` caps concurrent coding agents (default: 5)
- QA agents share the concurrency pool — so `--max-agents 5 --qa` = up to 10 total agents
- If `num_issues > max_agents`: process in batches (batch 1 finishes -> batch 2 starts)
- Each batch is `max_agents` pairs

## Model Selection

| Role | Model | Reason |
|------|-------|--------|
| Lead (orchestrator) | **opus** | Complex reasoning: issue triage, agent type selection, result synthesis |
| Coder agents | sonnet | Cost-effective implementation |
| QA agents | sonnet | Cost-effective review |

## Usage Examples

```bash
# Process all terraform issues with QA review
/batch-issues qbiq-ai/infra --label terraform --qa

# Process bug backlog, limit to 10 issues, 3 concurrent agents
/batch-issues qbiq-ai/infra --label bug --limit 10 --max-agents 3 --qa

# Dry run — show what would be processed without spawning agents
/batch-issues qbiq-ai/infra --label enhancement --dry-run

# Process milestone backlog
/batch-issues qbiq-ai/infra --milestone "Sprint 5" --qa

# Process specific labels, no QA (faster, less thorough)
/batch-issues qbiq-ai/infra --label "phase:1-landing-zone"
```

## Worktree Strategy

Each coder gets an isolated worktree:
- Branch: `feature/issue-{number}-{slug}` (e.g., `feature/issue-64-sso-groups`)
- Directory: `.claude/worktrees/batch-issue-{number}/`
- Auto-cleanup: worktree removed if no changes made
- Persist: worktree kept if changes exist (for PR)

QA agents read from their paired coder's worktree path (no isolation needed for readers).

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Issue has no body/description | Skip with reason "insufficient context" |
| Agent fails 3 times on same issue | Mark as failed, move to next |
| CI fails on Draft PR | Coder fixes, pushes, CI re-runs (max 3 cycles) |
| Worktree conflict | Abort that issue, report conflict |
| Rate limit (GitHub API) | Pause all agents, wait, resume |

## Integration

- Works with any GitHub repository the user has access to
- Respects all safety hooks from `settings.json` (no apply, no secrets, no push to main)
- Each PR links to its source issue via `Fixes #N`
- Project history updated by Lead after batch completes

## When NOT to Use This

- Single issue -> just delegate to a subagent
- Issues requiring cross-issue coordination -> use `/infra-team` instead
- Research/investigation -> use `/ai-research` instead
- Issues that depend on each other -> process sequentially, not in batch
