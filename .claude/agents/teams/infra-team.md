# Infrastructure Team Definition

An agent team specialized for infrastructure design, implementation, and validation. Operates as a self-managed unit with inter-agent messaging, plan approval gates, and a shared task list.

## Team Composition

| Role | Agent Type | Responsibility | Starts In |
|------|-----------|----------------|-----------|
| **Lead** | prime-orchestrator | Coordination only (delegate mode). Breaks work, assigns tasks, approves plans, synthesizes results. Never writes code. | delegate mode |
| **Architect** | solution-architect | System design, cloud architecture, component diagrams, trade-off analysis. Produces design docs. | plan mode |
| **Terraform Engineer** | terraform-engineer | Writes Terraform/Terragrunt modules, tests, CI/CD. Implements the architect's design. | plan mode |
| **DevOps Engineer** | devops-engineer | Kubernetes manifests, Helm charts, ArgoCD config, CI/CD pipelines, deployment automation. | plan mode |
| **Security Reviewer** | security-expert | Reviews all plans/code for CIS compliance, IAM least-privilege, network segmentation, secret management. | normal |
| **Cost Analyst** | devops-engineer | Runs /cost-estimate, /blast-radius. Challenges over-provisioning. Reports cost implications. | normal |
| **Validator** | infrastructure-validator | Post-apply validation: terraform plan/apply verification, deployment health, DNS/SSL checks. | normal |
| **Best Practices** | best-practices-validator | Reviews all code against Terraform/K8s/AWS standards. Blocks merge on violations. | normal |

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
  ▼ (blocked until 4 complete)
Task 6: Security review of code (Security)
  │
  ├──► Task 7: Best practices review (Best Practices)
  │
  ▼ (blocked until 6+7 complete)
Task 8: Apply to dev environment (Terraform Engineer)
  │
  ▼ (blocked until 8 complete)
Task 9: Validate deployment (Validator)
  │
  ▼ (blocked until 9 complete)
Task 10: Promote to staging (Lead - requires human approval)
  │
  ▼ (after approval)
Task 11: Final validation (Validator)
  │
  ▼
Task 12: Commit and create PR (Lead)
```

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
8. **Apply to dev** (terraform plan → human approval → apply)
9. **Validator checks** deployment
10. **Promote** through environments with gates
11. **Commit + PR** when all validations pass

### Quality Gates (Must ALL Pass)

| Gate | Check | Blocker |
|------|-------|---------|
| G1 | Architecture design reviewed | Security Reviewer |
| G2 | Cost within budget | Cost Analyst |
| G3 | Terraform fmt + validate | Terraform Engineer |
| G4 | Checkov/tfsec scan | Security Reviewer |
| G5 | Best practices check | Best Practices Validator |
| G6 | terraform plan clean | Terraform Engineer |
| G7 | Post-apply validation | Infrastructure Validator |
| G8 | Deployment health | Infrastructure Validator |

### Handling Failures

- If Security review fails → Implementer fixes, re-submits
- If Cost exceeds threshold → Architect redesigns, team restarts from Task 1
- If terraform apply fails → DevOps investigates, Terraform Engineer fixes
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
9. **Apply** to dev → **Validate** → **Promote** staging → **Validate** → PR

Total: One PR with fully tested, reviewed, compliant infrastructure.
