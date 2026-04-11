# Batch Issues Team Definition

A dynamically-sized agent team that processes multiple GitHub issues in parallel. The Lead fetches issues, triages them, spawns one coding agent per issue (with optional QA pairing), and collects results into Draft PRs.

## Key Difference from Other Teams

| | `/infra-team` | `/batch-issues` |
|---|---|---|
| **Input** | Free-text description | GitHub issues from backlog |
| **Sizing** | Fixed 8 roles | Dynamic: 1 Lead + N coders + N QA |
| **Parallelism** | Sequential task chain | Fully parallel (one pair per issue) |
| **Cross-agent comms** | Rich messaging | None between pairs (independent) |
| **Output** | One PR for all work | One Draft PR per issue |
| **Use case** | Design + implement system | Burn down issue backlog |

## Team Composition (Dynamic)

### Always Active

| Role | Agent Type | Model | Isolation | Responsibility |
|------|-----------|-------|-----------|----------------|
| **Lead** | prime-orchestrator | **opus** | none | Fetch issues, triage, spawn pairs, collect results, create PRs |

### Per-Issue Pair (spawned dynamically, up to `max_agents` concurrent)

| Role | Agent Type | Model | Isolation | Responsibility |
|------|-----------|-------|-----------|----------------|
| **Coder-{N}** | (varies by label) | sonnet | `worktree` | Implement the issue, run verification, report completion |
| **QA-{N}** | qa-engineer | sonnet | none | Review code, report findings or approve |

### Agent Count Formula

```
num_issues    = gh issue list --repo REPO --label LABEL | count
max_agents    = user-specified (default: 5)
num_coders    = min(num_issues, max_agents)
num_qa        = num_coders if --qa flag else 0
total_agents  = 1 (Lead) + num_coders + num_qa
```

**Example**: 20 issues with `--max-agents 5 --qa`:
- Batch 1: 5 coders + 5 QA = 10 agents + Lead
- Batch 2: 5 coders + 5 QA = 10 agents + Lead
- Batch 3: 5 coders + 5 QA = 10 agents + Lead
- Batch 4: 5 coders + 5 QA = 10 agents + Lead
- Total: 4 batches, processed sequentially

## Task Dependency Chain (Per Pair)

Each issue is an independent unit with its own mini task chain:

```
Task A-{N}: Implement issue #{N} (Coder-{N})
  │   1. Read issue body + labels
  │   2. Explore codebase for context
  │   3. Write implementation
  │   4. Run verification loop (type-specific)
  │   5. Report completion to Lead
  │
  ▼ (blocked until A-{N} complete)
Task B-{N}: QA review (QA-{N}) [only if --qa]
  │   1. Read coder's changes
  │   2. Review for quality, tests, security
  │   3. If findings → message Coder-{N} to fix
  │   4. Re-review after fix (max 3 cycles)
  │   5. Report approval or final findings to Lead
  │
  ▼ (blocked until B-{N} complete or skipped)
Task C-{N}: Create Draft PR (Lead)
  │   gh pr create --draft --title "fix: #{N} {title}"
  │   Body includes: implementation summary, verification results, linked issue
  │
  ▼ DONE for this issue
```

### No Cross-Pair Communication

Pairs are **fully independent**:
- Coder-1 never messages Coder-2
- QA-1 never messages QA-2
- This enables true parallelism without coordination overhead

If issues have dependencies on each other, they should NOT be processed in batch mode — use `/infra-team` instead.

## Verification by Agent Type

| Agent Type | Verification Loop |
|-----------|-------------------|
| terraform-engineer | `terraform fmt` -> `validate` -> `tflint` -> `checkov` -> `plan` |
| senior-backend-engineer | `lint` -> `test` -> `build` |
| senior-frontend-engineer | `lint` -> `test` -> `build` -> `type-check` |
| devops-engineer | `lint` -> `validate` (K8s/Helm) |
| fullstack-engineer | `lint` -> `test` -> `build` |

## Lead Responsibilities

### Issue Triage (Phase 1)

For each issue, the Lead determines:

1. **Agent type** — based on labels (see mapping in `batch-issues.md` command)
2. **Complexity** — simple (< 3 files), medium (3-10 files), complex (> 10 files)
3. **Skip?** — if issue body is empty/vague, skip with reason
4. **Dependencies** — if issue depends on another issue in the batch, defer to next batch

### Batch Management (Phase 2)

1. Spawn `max_agents` pairs in parallel
2. Monitor progress via task list
3. When a pair finishes: collect PR URL, spawn next pair from queue
4. Handle failures: retry once, then mark as failed

### Result Collection (Phase 3)

```markdown
## Batch Processing Report

**Repository**: {repo}
**Filter**: label={label}
**Processed**: {total} issues

### Succeeded ({count})
| Issue | PR | Agent Type | Summary |
|-------|-----|-----------|---------|
| #64 | #PR-1 | terraform-engineer | Configured SSO groups |
| #65 | #PR-2 | terraform-engineer | Added budget alerts |

### Failed ({count})
| Issue | Reason | Last Error |
|-------|--------|------------|
| #67 | Verification loop failed 3x | checkov: S3 public access |

### Skipped ({count})
| Issue | Reason |
|-------|--------|
| #70 | Insufficient context in issue body |
```

## Cost Estimation

| Component | Cost per Issue | Notes |
|-----------|---------------|-------|
| Lead (opus) | ~$0.50 triage + collection | Runs for entire batch |
| Coder (sonnet) | ~$1-5 per issue | Depends on complexity |
| QA (sonnet) | ~$0.50-2 per issue | Optional |
| **Batch of 20 issues** | **~$40-120 total** | With QA, sonnet coders |

## Spawn Prompt Template

### Coder Agent Spawn Prompt

```
You are Coder-{N} on the batch processing team.

Your task: Implement GitHub issue #{number}
Repository: {repo}
Working directory: (your worktree)

## Issue
Title: {title}
Body: {body}
Labels: {labels}

## Instructions
1. Read the issue carefully
2. Explore the codebase for existing patterns and related code
3. Implement the change following project conventions
4. Run the verification loop for your agent type
5. Report completion with VERIFICATION_COMPLETE message

## Rules
- Stay focused on THIS issue only
- Do NOT modify files unrelated to this issue
- Do NOT run terraform apply (CI/CD only from main)
- Follow existing code patterns and conventions
- Include tests if the project has a test framework
```

### QA Agent Spawn Prompt

```
You are QA-{N} reviewing Coder-{N}'s work on issue #{number}.

Worktree path: {coder_worktree_path}
Issue: #{number} — {title}

## Review Checklist
- [ ] Code quality: clean, readable, follows project patterns
- [ ] Tests: adequate coverage for the change
- [ ] Security: no hardcoded secrets, proper IAM, encrypted resources
- [ ] Verification: coder ran full verification loop
- [ ] Scope: changes match the issue description (no scope creep)

## Reporting
- If APPROVED: Report "QA_APPROVED: issue={number}" to Lead
- If FINDINGS: Report findings to Coder-{N} with FINDING format
  Max 3 review cycles. After 3 cycles, report final status to Lead.
```
