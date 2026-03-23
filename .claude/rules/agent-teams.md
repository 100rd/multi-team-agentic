---
paths:
  - ".claude/agents/**"
  - ".claude/commands/**"
  - ".claude/skills/**"
---

# Agent Teams

Agent teams are **persistent Claude Code sessions** that communicate directly with each other via messaging, coordinate through a shared task list, and self-manage their work.

## When to Use Agent Teams vs Subagents

| Use Case | Use Agent Team | Use Subagent |
|----------|---------------|-------------|
| Infrastructure design + implement | Team | |
| Deep AI/ML research with citations | Team | |
| Full lifecycle: research -> deploy -> validate | Team | |
| Quick file search | | Subagent |
| Multi-role review (security + cost + practices) | Team | |
| Single focused task | | Subagent |
| Tasks requiring inter-agent debate | Team | |
| Simple delegation | | Subagent |

## Worktree Isolation

| Teammate Type | Isolation | Reason |
|---------------|-----------|--------|
| Writers (Architect, Terraform, DevOps, Engineers) | `worktree` | Each gets own repo copy |
| Readers (Security, Cost, Validator, Best Practices) | none | Read-only reviews via messages |

The orchestrator decides isolation per teammate.

## Plan Approval

All implementers (Architect, Terraform, DevOps) start in **plan mode**:
1. Explore codebase and design approach
2. Submit plan to Lead
3. Lead approves or rejects with feedback
4. Only after approval can they write code

Auto-reject criteria:
- Missing security considerations
- No test strategy
- Hardcoded secrets
- Missing cost analysis
- No rollback plan

## Task Dependencies

Tasks auto-unblock when their dependencies complete:
```
Task 1: Design architecture        -> assigned to Architect
Task 2: Security review of design  -> blocked by Task 1
Task 3: Cost estimate              -> blocked by Task 1
Task 4: Write Terraform            -> blocked by Tasks 2 + 3
Task 5: Write K8s manifests        -> blocked by Tasks 2 + 3
Task 6: Security review of code    -> blocked by Tasks 4 + 5
```

## Delegate Mode

Enable with Shift+Tab to restrict Lead to coordination-only:
- Spawn teammates, message, manage tasks, approve plans
- No file writes, no bash commands, no implementation

## Available Teams

- `/infra-team` — Infrastructure: design, implement, validate (`.claude/agents/teams/infra-team.md`)
- `/ai-research` — AI research: training, inference, MLOps (`.claude/agents/teams/ai-research-team.md`)
- `/dev-team` — Development: fullstack, security, QA (`.claude/agents/teams/dev-team.md`)
- `/pipeline` — Full lifecycle: research -> deploy -> validate (`.claude/agents/teams/pipeline-team.md`)
- `/investigate` — Competing hypothesis debugging
- `/design-system` — Full lifecycle with agent team
