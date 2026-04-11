---
name: infra-team
description: Infrastructure team for system design, implementation, and validation with architect, terraform, devops, security, cost, and validation specialists
model: opus
effort: high
---

# Infrastructure Team Definition

An agent team specialized for infrastructure design, implementation, and validation. Operates as a self-managed unit with inter-agent messaging, plan approval gates, and a shared task list.

## Team Composition

| Role | Agent Type | Model | Responsibility | Starts In | Isolation |
|------|-----------|-------|----------------|-----------|-----------|
| **Lead** | prime-orchestrator | **opus** | Coordination only (delegate mode). Breaks work, assigns tasks, approves plans, synthesizes results. Never writes code. | delegate mode | none |
| **Architect** | solution-architect | sonnet | System design, cloud architecture, component diagrams, trade-off analysis. Produces design docs. | plan mode | `worktree` |
| **Terraform Engineer** | terraform-engineer | sonnet | Writes Terraform/Terragrunt modules, tests. Runs verification loop (fmt/validate/tflint/checkov/plan). Never applies. | plan mode | `worktree` |
| **DevOps Engineer** | devops-engineer | sonnet | Kubernetes manifests, Helm charts, ArgoCD config, CI/CD pipelines, deployment automation. | plan mode | `worktree` |
| **Security Reviewer** | security-expert | sonnet | Reviews all plans/code for CIS compliance, IAM least-privilege, network segmentation, secret management. | normal | none |
| **Cost Analyst** | devops-engineer | sonnet | Runs /cost-estimate, /blast-radius. Challenges over-provisioning. Reports cost implications. | normal | none |
| **Validator** | infrastructure-validator | sonnet | Post-merge validation: verify CI/CD apply-from-main succeeded, deployment health, DNS/SSL checks. | normal | none |
| **Best Practices** | best-practices-validator | sonnet | Reviews all code against Terraform/K8s/AWS standards. Blocks merge on violations. | normal | none |

### Worktree Isolation Strategy

Teammates that **write files** (Architect, Terraform Engineer, DevOps Engineer) are spawned with `isolation: "worktree"`, giving each their own repository copy. This eliminates file conflicts between parallel implementers.

Teammates that **only read and review** (Security, Cost, Validator, Best Practices) run without isolation — they read from the main working directory and report findings via messages.

The Lead merges each writer's worktree branch into the feature branch after reviews pass. See `agent-team-protocol.md` for the full isolation protocol.

## Team Communication Patterns

### Message Flow

```
                    ┌──────────────────┐
                    │   LEAD (You)     │
                    │ delegate mode    │
                    └────────┬─────────┘
                             │ assigns tasks / approves plans
               ┌─────────────┼──────────────┐
               ▼             ▼               ▼
        ┌──────────┐  ┌──────────┐   ┌──────────┐
        │ Architect │  │ Terraform│   │  DevOps  │
        │          │──│ Engineer │──│ Engineer │
        └────┬─────┘  └────┬─────┘   └────┬─────┘
             │              │               │
             ▼              ▼               ▼
        sends design   sends code     sends manifests
             │              │               │
             └──────┬───────┴───────┬───────┘
                    ▼               ▼
             ┌──────────┐   ┌──────────┐
             │ Security  │   │   Best   │
             │ Reviewer  │   │ Practices│
             └────┬──────┘   └────┬─────┘
                  │               │
                  ▼               ▼
            blocks/approves  blocks/approves
                  │               │
                  └───────┬───────┘
                          ▼
                   ┌──────────┐
                   │ Validator │
                   └──────────┘
                   post-apply checks
```

### Direct Messaging Rules

1. **Architect → Terraform Engineer**: Design doc ready, clarify requirements
2. **Architect → DevOps Engineer**: Deployment architecture, K8s topology
3. **Terraform Engineer → Security Reviewer**: "Please review module at path X"
4. **DevOps Engineer → Security Reviewer**: "Please review K8s manifests"
5. **Security Reviewer → Terraform Engineer**: "BLOCKED: finding X needs fix"
6. **Security Reviewer → DevOps Engineer**: "BLOCKED: finding X needs fix"
7. **Cost Analyst → Architect**: "Cost exceeds threshold, redesign needed"
8. **Any → Lead**: Status updates, blockers, completion

### Broadcast Rules

Use broadcast ONLY for:
- Team-wide blockers
- Architecture changes that affect everyone
- Final status before shutdown

## Task Dependency Chain

```
Task 1: Design architecture (Architect)
  │
  ├──► Task 2: Security review of design (Security)     ─┐
  │                                                        ├── Both must pass
  ├──► Task 3: Cost estimate of design (Cost Analyst)    ─┘
  │
  ▼ (blocked until 2+3 complete)
Task 4: Write Terraform modules (Terraform Engineer)
  │
  ├──► Task 5: Write K8s/Helm manifests (DevOps)
  │
  ▼ (blocked until 4+5 complete)
Task 6: Security review of code (Security)         ─┐
  │                                                    ├── Parallel reviews
Task 7: Best practices review (Best Practices)     ─┘
  │
  ▼ (blocked until 6+7 complete)
Task 8: Terraform verification loop (Terraform Engineer)
  │   fmt → validate → tflint → checkov → plan → fix → repeat until ALL clean
  │   Captures plan output for PR description
  │
  ▼ (blocked until 8 produces clean output)
Task 9: Create Draft PR (Lead)
  │   Commit to feature branch, push, gh pr create --draft
  │   PR description includes: plan output, review status, cost estimate
  │
  ▼ (blocked until 9 complete)
Task 10: CI pipeline verification (Lead monitors, Terraform Engineer fixes)
  │   Wait for CI checks: fmt, validate, tflint, trivy, checkov, plan
  │   If CI fails → Terraform Engineer fixes → pushes → CI re-runs
  │   Loop until ALL CI checks are green
  │
  ▼ (blocked until 10 — all CI checks green)
Task 11: Mark PR ready for review (Lead)
  │   gh pr ready — converts Draft to ready for review
  │   Adds reviewers if configured
  │
  ▼ (blocked until PR approved and merged to main)
Task 12: Post-merge verification (Validator)
  │   Verify CI/CD on main runs terraform plan + apply successfully
  │   Validate deployment health after apply-from-main completes
  │
  ▼ (blocked until 12 complete)
Task 13: Team cleanup and shutdown (Lead)
```

### Key Principle: Agents NEVER Apply

- Agents write code and verify with `terraform plan`
- `terraform apply` runs ONLY from CI/CD on the main branch after PR merge
- This eliminates drift between code in main and actual infrastructure state
- See `auto-approve-protocol.md` for full rules

## Plan Approval Criteria

The Lead approves plans ONLY when ALL of the following are met:

### For Architect Plans
- [ ] Clear component diagram with service boundaries
- [ ] AWS Well-Architected Framework pillars addressed
- [ ] High availability and disaster recovery considered
- [ ] Cost-conscious design (no over-provisioning)
- [ ] Security by design (encryption, least privilege, network segmentation)

### For Terraform Engineer Plans
- [ ] Module structure follows community conventions
- [ ] Tests included (unit + integration)
- [ ] Variables have descriptions and validation
- [ ] Outputs documented
- [ ] State management strategy defined
- [ ] No hardcoded values

### For DevOps Engineer Plans
- [ ] GitOps workflow defined (ArgoCD app-of-apps)
- [ ] Resource limits and requests set
- [ ] Health checks and readiness probes configured
- [ ] Network policies defined
- [ ] Monitoring and alerting included

### Rejection Criteria (Auto-Reject)
- Missing security considerations
- No test strategy
- Hardcoded secrets or credentials
- Missing cost analysis
- No rollback plan

## Self-Management Protocol

### During Work Session

1. **Lead creates task list** from user's request
2. **Architect plans first** (plan mode, requires approval)
3. **Security + Cost review design** in parallel
4. **Lead approves or rejects** with feedback
5. **Implementers work** (plan mode, requires approval before coding)
6. **Security + Best Practices review code** (parallel)
7. **Fixes applied** based on review findings
8. **Terraform verification loop** — fmt/validate/tflint/checkov/plan until clean
9. **Draft PR created** with plan output and review status
10. **CI pipeline verification** — wait for green, fix if needed
11. **PR marked ready** for human review
12. **Post-merge validation** — verify apply-from-main succeeds
13. **Team cleanup**

### Quality Gates (Must ALL Pass)

| Gate | Check | Blocker |
|------|-------|---------|
| G1 | Architecture design reviewed | Security Reviewer |
| G2 | Cost within budget | Cost Analyst |
| G3 | Terraform fmt + validate | Terraform Engineer |
| G4 | Checkov/tfsec scan | Security Reviewer |
| G5 | Best practices check | Best Practices Validator |
| G6 | Verification loop clean (all tools pass, plan clean) | Terraform Engineer |
| G7 | CI pipeline green on Draft PR | Automated (GitHub Actions) |
| G8 | Post-merge apply-from-main healthy | Infrastructure Validator |

### Handling Failures

- If Security review fails → Implementer fixes, re-submits
- If Cost exceeds threshold → Architect redesigns, team restarts from Task 1
- If verification loop fails → Terraform Engineer fixes code, re-runs loop from Step 1
- If CI pipeline fails → Terraform Engineer fixes, pushes, CI re-runs
- If post-merge apply fails → Escalate to human (do NOT attempt manual apply)
- If validation fails → Team debugs with competing hypothesis pattern
- If 3+ failures on same task → Escalate to human

## Working Directory Convention

```
project/{project-name}/
├── docs/
│   └── architecture/          # Architect writes here
│       ├── design.md
│       ├── diagrams/
│       └── decisions/
├── terraform/                  # Terraform Engineer writes here
│   ├── modules/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── tests/
├── kubernetes/                 # DevOps Engineer writes here
│   ├── manifests/
│   ├── helm/
│   └── argocd/
├── security/                   # Security Reviewer writes here
│   ├── review-reports/
│   └── compliance/
└── validation/                 # Validator writes here
    └── reports/
```

## Example: HFT AWS System Design

User says: "Design an HFT trading system on AWS"

### Team Execution:

1. **Lead** creates 12 tasks with dependencies
2. **Architect** designs:
   - Ultra-low-latency network (AWS Direct Connect, placement groups)
   - Kernel bypass networking (DPDK/SRD on ENA Express)
   - FPGA acceleration (AWS F1 instances)
   - Time synchronization (PTP via Amazon Time Sync)
   - Multi-AZ with sub-millisecond failover
   - Market data ingestion pipeline
3. **Security** reviews: Encryption at rest/transit, VPC design, IAM, compliance
4. **Cost Analyst**: Estimates reserved vs on-demand, data transfer costs
5. **Lead** approves (or rejects with feedback)
6. **Terraform Engineer** implements: VPC, EC2 placement, EKS, RDS, ElastiCache
7. **DevOps** implements: K8s configs, monitoring, Grafana dashboards
8. **Security + Best Practices** review all code
9. **Verification loop** (fmt/validate/tflint/checkov/plan) → **Draft PR** → **CI green** → **Ready for review** → **Merge** → **Apply from main** (CI/CD)

Total: One PR with fully tested, reviewed, compliant infrastructure.
