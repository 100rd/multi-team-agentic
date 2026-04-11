---
name: infra-team
description: Launch a self-managed infrastructure agent team with architect, terraform, devops, security, cost, and validation specialists
args: "<task-description> [--project NAME] [--env dev|staging|prod] [--team-size 4-8]"
---

# Infrastructure Team Command

Spawns a native Claude Code agent team specialized for infrastructure design and implementation. The team self-manages through design → review → implement → validate → commit.

## What This Command Does

1. **Creates an agent team** with the Lead in delegate mode (coordination only)
2. **Spawns specialized teammates** based on the task complexity
3. **Creates a task list** with dependencies that auto-unblock
4. **Requires plan approval** before any implementation begins
5. **Runs quality gates** at every stage (security, cost, best practices)
6. **Produces a fully tested PR** with all reviews passed

## Team Roles

| Teammate | Agent | Model | Mode | Responsibility |
|----------|-------|-------|------|----------------|
| Lead | prime-orchestrator | **opus** | delegate | Coordination, plan approval, PR management |
| Architect | solution-architect | sonnet | plan first | System design, AWS architecture |
| Terraform | terraform-engineer | sonnet | plan first | IaC modules, testing, verification loop |
| DevOps | devops-engineer | sonnet | plan first | K8s, Helm, ArgoCD, CI/CD |
| Security | security-expert | sonnet | normal | CIS compliance, IAM review |
| Cost | devops-engineer | sonnet | normal | Cost analysis, right-sizing |
| Validator | infrastructure-validator | sonnet | normal | Post-merge validation |
| Best Practices | best-practices-validator | sonnet | normal | Standards enforcement |

## Execution Flow

When this command is invoked:

### Phase 1: Team Setup
```
Create agent team "infra-{project}-{timestamp}"
Enable delegate mode on Lead (Shift+Tab)
Spawn teammates with appropriate agent types
Set all implementers to plan-approval-required mode
```

### Phase 2: Design (Plan Approval Required)
```
Task 1: Design system architecture [Architect, plan mode]
  → Lead reviews and approves/rejects
Task 2: Security review of design [Security]
Task 3: Cost estimate of design [Cost Analyst]
  → Both must pass before implementation begins
```

### Phase 3: Implementation (Plan Approval Required)
```
Task 4: Write Terraform modules [Terraform, plan mode]
  → Lead approves implementation plan
Task 5: Write K8s/deployment config [DevOps, plan mode]
  → Lead approves implementation plan
Task 6: Security review of code [Security]
Task 7: Best practices review [Best Practices]
  → All reviews must pass
```

### Phase 4: Verification Loop
```
Task 8: Terraform verification loop [Terraform Engineer]
  fmt → validate → tflint → checkov → plan → fix → repeat until ALL clean
  Captures plan output for PR description
Task 9: Capture verification results [Terraform Engineer → Lead]
```

### Phase 5: Draft PR + CI Green
```
Task 10: Create Draft PR with plan output [Lead]
  gh pr create --draft with plan summary, review status, cost estimate
Task 11: CI pipeline verification [Lead monitors, Terraform fixes]
  Wait for CI: fmt, validate, tflint, trivy, checkov, plan
  If CI fails → fix → push → CI re-runs (loop until green)
Task 12: Mark PR ready for review [Lead]
  gh pr ready — converts Draft to ready for review
```

### Phase 6: Post-Merge Validation
```
Task 13: Post-merge apply verification [Validator]
  Verify CI/CD on main runs terraform apply successfully
  Validate deployment health after apply-from-main
Task 14: Team cleanup and shutdown [Lead]
```

### Key Rule: Agents NEVER Apply
Terraform apply runs ONLY from CI/CD on the main branch after PR merge.
Agents use `terraform plan` for verification only. See `auto-approve-protocol.md`.

## Usage Examples

```bash
# Design and implement a new HFT system
/infra-team "Design ultra-low-latency HFT trading system on AWS with FPGA acceleration"

# Add monitoring to existing infrastructure
/infra-team "Add comprehensive monitoring and alerting for EKS cluster" --project platform-design

# Create new environment
/infra-team "Create DR environment in us-west-2 matching prod" --env prod --project snips

# Network redesign
/infra-team "Redesign VPC architecture for multi-account strategy with Transit Gateway"
```

## How the Lead Spawns Teammates

The Lead uses the **Agent tool** to spawn each teammate. The Agent tool accepts ONLY these parameters:
- `prompt` (required) — full task description with team context
- `subagent_type` (optional) — agent definition name from `.claude/agents/`
- `isolation` (optional) — `"worktree"` for writing teammates
- `model` (optional) — `"opus"` or `"sonnet"`
- `run_in_background` (optional) — boolean for async

**Do NOT pass**: `name`, `team_name`, `teammate_name`, or any undefined parameters.

### Example Spawn Call

```
Agent(
  subagent_type: "terraform-engineer",
  model: "sonnet",
  isolation: "worktree",
  prompt: "You are the Terraform Engineer on the infrastructure team for: {TASK}..."
)
```

### Spawn Prompt Template

The Lead includes this context in each teammate's prompt:

```
You are the {ROLE} on the infrastructure team for: {TASK_DESCRIPTION}

Project: {PROJECT_NAME}
Working directory: project/{PROJECT_NAME}/

Your responsibilities:
{ROLE_SPECIFIC_RESPONSIBILITIES}

Communication rules:
- Message the Lead for status updates and blockers
- Message other teammates directly for coordination
- Never edit files outside your assigned directories
- Follow the plan approval protocol before implementing

Quality requirements:
- All code must pass security review
- All Terraform must pass fmt, validate, and checkov
- All designs must address AWS Well-Architected pillars
- Cost must be within reasonable bounds
- Rollback plan required for every change

Read project history first:
cat project/PROJECT_HISTORY.md | tail -50
```

## Plan Approval Criteria

The Lead uses these criteria to approve/reject teammate plans:

### Approve When
- Design addresses all AWS Well-Architected pillars
- Security is built-in (not bolted on)
- Tests are included in the plan
- Cost is considered and right-sized
- Rollback strategy is clear
- File ownership boundaries are respected

### Reject When
- Missing security considerations → feedback: "Add encryption, IAM, network security"
- No tests planned → feedback: "Include unit + integration test plan"
- Over-provisioned → feedback: "Right-size instances, use auto-scaling"
- No rollback plan → feedback: "Add rollback steps for each change"
- Violates team conventions → feedback: "Follow module structure in terraform/"

## Integration with Existing Commands

This command integrates with:
- `/blast-radius` — run before every apply
- `/cost-estimate` — run during design review
- `/validate-deployment` — run after every apply
- `/promote-environment` — run for environment progression
- `/log-activity` — every teammate logs to project history
- `/query-history` — every teammate reads history on startup

## Monitoring the Team

### In tmux mode (recommended)
Each teammate gets its own split pane. Click to interact directly.

### In in-process mode
Use `Shift+Up/Down` to select teammates.
Use `Ctrl+T` to toggle the shared task list.
Press `Enter` to view a teammate's session.

## When the Team Finishes

1. All tasks marked complete
2. All quality gates passed
3. Infrastructure deployed and validated
4. PR created with all changes
5. Team cleanup runs (removes team resources)
6. Project history updated by all teammates
