---
name: design-system
description: End-to-end infrastructure system design with agent team - from architecture through tested deployment
args: "<system-description> [--project NAME] [--cloud aws|gcp|azure] [--budget AMOUNT]"
---

# System Design Command

Runs the full infrastructure lifecycle for a new system: design → review → implement → test → deploy → validate → commit. Uses a self-managed agent team that produces a fully tested, reviewed, and compliant result.

## This Is Your Main Workflow

This command orchestrates the complete "idea to tested infrastructure" pipeline:

```
User describes system
       │
       ▼
┌──────────────────┐
│ 1. DESIGN        │  Architect creates system design
│    (plan mode)   │  Security reviews design
│                  │  Cost analyst estimates budget
└────────┬─────────┘
         │ Lead approves design
         ▼
┌──────────────────┐
│ 2. IMPLEMENT     │  Terraform engineer writes modules
│    (plan mode)   │  DevOps writes K8s/deployment
│                  │  Security reviews code
│                  │  Best practices validates
└────────┬─────────┘
         │ Lead approves implementation
         ▼
┌──────────────────┐
│ 3. TEST          │  terraform fmt + validate
│                  │  Checkov/tfsec security scan
│                  │  terraform plan (review output)
└────────┬─────────┘
         │ All tests pass
         ▼
┌──────────────────┐
│ 4. DEPLOY        │  terraform apply (dev)
│                  │  ⚠️ Human approval required
│                  │  Post-deploy validation
└────────┬─────────┘
         │ Validation passes
         ▼
┌──────────────────┐
│ 5. PROMOTE       │  Promote to staging
│                  │  Full validation suite
│                  │  ⚠️ Human approval for prod
└────────┬─────────┘
         │ All environments healthy
         ▼
┌──────────────────┐
│ 6. DELIVER       │  Create feature branch
│                  │  Commit all changes
│                  │  Create Pull Request
│                  │  Update project history
└──────────────────┘
```

## How to Use

### New System From Scratch
```bash
/design-system "Ultra-low-latency HFT trading system on AWS with FPGA acceleration, \
  multi-AZ failover, market data ingestion, and order execution pipeline"

/design-system "Multi-tenant SaaS platform with per-tenant encryption, \
  auto-scaling EKS, RDS Aurora, and ElastiCache" --budget 5000

/design-system "Event-driven data pipeline with Kinesis, Lambda, S3, \
  and Redshift for real-time analytics" --cloud aws --project analytics-platform
```

### Evolve Existing System
```bash
/design-system "Add DR region (us-west-2) to existing production infrastructure" \
  --project platform-design

/design-system "Migrate from ECS to EKS with zero-downtime" \
  --project snips

/design-system "Add comprehensive monitoring, alerting, and runbooks \
  for all production services" --project opsfleet
```

## What Gets Produced

After the team finishes, you get:

```
project/{name}/
├── docs/
│   └── architecture/
│       ├── system-design.md           # Full architecture document
│       ├── decisions/                  # Architecture Decision Records
│       │   ├── ADR-001-compute.md
│       │   ├── ADR-002-network.md
│       │   └── ADR-003-storage.md
│       └── diagrams/                  # Component and flow diagrams
│
├── terraform/
│   ├── modules/                       # Reusable Terraform modules
│   │   ├── vpc/
│   │   ├── eks/
│   │   ├── rds/
│   │   └── ...
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   ├── staging/
│   │   └── prod/
│   └── tests/                         # Terraform tests
│
├── kubernetes/                        # K8s manifests
│   ├── manifests/
│   ├── helm/
│   └── argocd/
│
├── security/
│   └── review-reports/
│       ├── design-review.md           # Security review of architecture
│       └── code-review.md             # Security review of implementation
│
└── validation/
    └── reports/
        ├── dev-validation.md          # Post-deploy validation results
        └── staging-validation.md
```

Plus:
- All changes on a feature branch
- Pull Request with full description
- Project history updated by all team members
- Cost estimate documented

## Quality Guarantees

Every deliverable passes through:

| Gate | What | Who Reviews |
|------|------|-------------|
| Design Review | Architecture meets requirements | Security + Cost Analyst |
| Plan Approval | Implementation approach is sound | Lead |
| Code Review | Code follows best practices | Best Practices Validator |
| Security Scan | No vulnerabilities, CIS compliant | Security Reviewer |
| Cost Check | Within budget, right-sized | Cost Analyst |
| Terraform Validate | Syntax and logic correct | Automated |
| Terraform Plan | No unexpected changes | Terraform Engineer |
| Deploy Validation | Infrastructure healthy | Infrastructure Validator |
| E2E Check | System works end-to-end | Validator |

## Resuming a Session

If you need to continue work from a previous session:

```bash
# Check what was done before
/query-history --tag {project-name} --limit 20

# Resume where you left off
/design-system "Continue implementing the HFT system" --project hft-system
```

The team will read project history and pick up where the last session ended.

## Arguments

- `system-description`: Natural language description of what to build
- `--project NAME`: Project directory name (created under `project/`)
- `--cloud aws|gcp|azure`: Target cloud provider (default: aws)
- `--budget AMOUNT`: Monthly budget cap in USD (triggers cost gate)
- `--skip-deploy`: Stop after code review, don't apply to any environment
- `--env-only dev|staging|prod`: Only deploy to specific environment

## Example: Complete HFT System

```
User: /design-system "High-frequency trading system on AWS"

Lead creates team → 7 teammates spawn in tmux panes

Architect (plan mode):
  - Designs ultra-low-latency architecture
  - AWS Direct Connect + placement groups
  - FPGA on F1 instances for order matching
  - Amazon Time Sync for PTP
  - Multi-AZ with active-active
  → Submits plan to Lead

Lead reviews: ✅ Approved (addresses all pillars, cost-conscious)

Security reviews design: ⚠️ "Add encryption for market data at rest"
Cost estimates: "$12,400/month - within typical HFT budgets"

Architect revises: Adds encryption → Lead re-approves

Terraform Engineer (plan mode):
  - Plans modules: vpc, ec2-placement, eks, direct-connect
  - Plans tests: unit + plan validation
  → Submits plan to Lead

Lead reviews: ✅ Approved

Terraform Engineer implements:
  - Writes all modules
  - Writes tests
  - Runs terraform fmt + validate

Security reviews code: ✅ Passed (encryption, IAM, SG rules)
Best Practices reviews: ⚠️ "Add lifecycle ignore for EBS volumes"

Terraform Engineer fixes → Re-reviewed → ✅ Passed

terraform plan → Clean output
terraform apply (dev) → ⚠️ Human approves → Applied
Validator checks → ✅ All healthy

Promote to staging → ⚠️ Human approves → Applied
Validator checks → ✅ All healthy

Lead creates branch, commits, creates PR
All teammates log to project history
Team cleanup → Done

Result: One PR with fully tested HFT infrastructure
```
