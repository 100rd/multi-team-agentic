---
name: pipeline
description: Launch full lifecycle pipeline team — research, design, implement, deploy, validate in one autonomous flow
args: "<goal-description> [--project NAME] [--phases research,design,infra,validate] [--auto-approve dev,staging] [--skip-deploy]"
---

# Pipeline Command

Spawns a single unified agent team that runs the full lifecycle autonomously: **research → design → implement → deploy → validate → report**. The team uses phased role spawning — different specialists activate at each phase while the Lead coordinates throughout.

## What This Command Does

1. **Creates one agent team** with the Lead in delegate mode
2. **Spawns researchers** (Phase 1) — 4 agents research the topic in parallel
3. **Spawns architect** (Phase 2) — designs based on research findings
4. **Spawns implementers** (Phase 3) — write Terraform + K8s based on design
5. **Spawns reviewers** (Phase 4) — security + best practices review
6. **Auto-deploys** (Phase 5) — terraform apply to dev/staging (auto-approved)
7. **Validates + finds gaps** (Phase 5) — health checks + gap analysis
8. **Delivers** (Phase 6) — final report, commit, PR

## Team Roles (By Phase)

| Phase | Teammate | Agent | Mode | Writes To |
|-------|----------|-------|------|-----------|
| 1 | AI Architect | solution-architect | plan first | `research/sections/ai-architecture.md` |
| 1 | MLOps Researcher | devops-engineer | plan first | `research/sections/mlops-landscape.md` |
| 1 | Infra Analyst | terraform-engineer | plan first | `research/sections/infrastructure.md` |
| 1 | OSS Scout | senior-backend-engineer | normal | `research/sections/oss-ecosystem.md` |
| 2 | Solution Architect | solution-architect | plan first | `docs/architecture/` |
| 3 | Terraform Engineer | terraform-engineer | plan first | `terraform/` |
| 3 | DevOps Engineer | devops-engineer | plan first | `kubernetes/` |
| 4 | Security Reviewer | security-expert | normal | `security/review-reports/` |
| 4 | Best Practices | best-practices-validator | normal | (messages only) |
| 5 | Validator | infrastructure-validator | normal | `validation/reports/` |
| 5 | Gap Analyzer | qa-engineer | normal | `validation/reports/gap-analysis.md` |
| 6 | Lead (compiles) | prime-orchestrator | delegate | `final-report.md` |

## Execution Flow

### Phase 1: Research
```
Spawn 4 researchers (parallel, worktree isolation)
Each researches their assigned thread:
  - AI Architect: system architecture patterns
  - MLOps Researcher: MLOps tooling landscape
  - Infra Analyst: compute infrastructure + cost modeling
  - OSS Scout: open source ecosystem mapping
Wait for all to complete
Lead reviews research quality
Merge worktree branches → Shutdown researchers
```

### Phase 2: Design
```
Spawn Solution Architect (plan mode, worktree)
Architect reads Phase 1 research at project/{name}/research/
Designs system architecture with ADRs
Submits plan → Lead approves/rejects
Merge worktree branch → Shutdown architect
```

### Phase 3: Implement
```
Spawn Terraform Engineer + DevOps Engineer (plan mode, worktree)
Each submits implementation plan → Lead approves
Terraform writes modules, tests, environments
DevOps writes K8s manifests, Helm, ArgoCD
terraform fmt + validate run automatically
Keep agents alive (may need fixes from Phase 4)
```

### Phase 4: Review
```
Spawn Security Reviewer + Best Practices (normal, no isolation)
Security reviews design + code for CIS compliance
Best Practices validates against standards
If findings → Phase 3 agents fix and re-submit
When all pass → Merge worktree branches → Shutdown Phase 3+4
```

### Phase 5: Deploy + Validate
```
terraform plan + apply to dev (AUTO-APPROVED by env-check hook)
Spawn Validator → checks health (DNS, SSL, K8s, ArgoCD)
terraform plan + apply to staging (AUTO-APPROVED by env-check hook)
Validator re-checks staging health
Spawn Gap Analyzer → finds problems, edge cases, improvements
Shutdown Phase 5 agents
```

### Phase 6: Report + Deliver
```
Lead compiles final-report.md from all phases
Create feature branch
Commit all changes
Create Pull Request
Update project history
Team cleanup
```

## Usage Examples

```bash
# Full autonomous pipeline — research through deployment
/pipeline "Build production LLM inference platform on AWS with auto-scaling and multi-model serving"

# With project name and custom auto-approve
/pipeline "Multi-tenant SaaS platform with per-tenant encryption" --project saas-platform

# Research + design only, skip implementation and deployment
/pipeline "Compare GPU strategies for distributed training" --project gpu-research --phases research,design

# Skip research, go straight to implementation (when you already know what to build)
/pipeline "EKS cluster with Karpenter and GPU node groups" --project eks-gpu --phases design,infra,validate

# Most conservative — manual approval everywhere
/pipeline "Payment processing system" --project payments --auto-approve none

# Auto-approve only dev
/pipeline "Internal analytics pipeline" --project analytics --auto-approve dev

# Skip deployment entirely (design + code only)
/pipeline "Federated learning infrastructure" --project fedml --skip-deploy
```

## Auto-Approve Behavior

By default, terraform apply is auto-approved for dev and staging environments:

| Environment | terraform apply | terraform destroy |
|-------------|----------------|-------------------|
| dev | AUTO | AUTO |
| staging | AUTO | CHECKPOINT |
| prod | BLOCKED (human) | BLOCKED (human) |
| unknown | CHECKPOINT | CHECKPOINT |

Override with `--auto-approve`:
- `--auto-approve none` — all environments require human approval
- `--auto-approve dev` — only dev auto-approved
- `--auto-approve dev,staging` — both auto-approved (default)

The environment detection script (`scripts/terraform-env-check.sh`) determines the environment from:
1. Working directory path patterns (`environments/dev/`)
2. Tfvars file names (`dev.tfvars`)
3. `-var-file` arguments
4. Terragrunt directory patterns

See `.claude/agents/_shared/team-protocols/auto-approve-protocol.md` for full governance.

## Phase Customization

Use `--phases` to run only specific phases:

| Phases | What Runs | Use When |
|--------|-----------|----------|
| `research` | Phase 1 only | You just want research, no implementation |
| `research,design` | Phases 1-2 | Research + architecture, no code |
| `design,infra,validate` | Phases 2-5 | You already have research, need implementation |
| `infra,validate` | Phases 3-5 | You already have a design, need code + deploy |
| `research,design,infra,validate` | All phases (default) | Full lifecycle |

## Team Spawn Prompt Template

The Lead spawns each teammate with context appropriate to their phase:

### Phase 1 Researcher Template
```
You are the {ROLE} on the pipeline team for: {GOAL}

Project: {PROJECT_NAME}
Working directory: project/{PROJECT_NAME}/research/sections/{YOUR_FILE}

Your research thread: {SPECIFIC_RESEARCH_QUESTIONS}

Research standards:
- Every factual claim MUST have a citation
- Include "when to use" practical guidance
- Flag anything uncertain rather than guessing
- Prefer primary sources over blog posts

Read project history: cat project/PROJECT_HISTORY.md | tail -50
```

### Phase 2-3 Implementer Template
```
You are the {ROLE} on the pipeline team for: {GOAL}

Project: {PROJECT_NAME}
IMPORTANT: Read the research at project/{PROJECT_NAME}/research/ before designing
IMPORTANT: Read the design at project/{PROJECT_NAME}/docs/architecture/ before implementing

Your responsibilities: {ROLE_RESPONSIBILITIES}

Auto-approve environments: {AUTO_APPROVE_ENVS}
For these environments, terraform apply proceeds without human approval.

Quality requirements:
- All code must pass security review
- All Terraform must pass fmt, validate, and checkov
- Rollback plan required for every change
```

## Output

After the pipeline team finishes:

```
project/{name}/
├── research/                    # Phase 1: Research findings
├── docs/architecture/           # Phase 2: System design + ADRs
├── terraform/                   # Phase 3: Infrastructure code
├── kubernetes/                  # Phase 3: Deployment configs
├── security/review-reports/     # Phase 4: Security review
├── validation/reports/          # Phase 5: Health checks + gap analysis
└── final-report.md              # Phase 6: Compiled report
```

Plus:
- Feature branch with all changes
- Pull Request with full description
- Project history updated by all agents
- Gap analysis with improvement recommendations

## Resuming a Pipeline

```bash
# Check what was done
/query-history --tag {project-name} --limit 50

# Resume — agents read history and pick up where left off
/pipeline "Continue the inference platform pipeline" --project llm-inference
```

## Arguments

- `goal-description`: Natural language description of what to research, build, and deploy
- `--project NAME`: Project directory name (created under `project/`)
- `--phases LIST`: Comma-separated phases to run (default: `research,design,infra,validate`)
- `--auto-approve LIST`: Environments to auto-approve (default: `dev,staging`; use `none` for manual)
- `--skip-deploy`: Stop after code review, don't apply to any environment

## Integration with Existing Commands

This command integrates with:
- `/cost-estimate` — run during research + before apply
- `/blast-radius` — run before terraform apply
- `/validate-deployment` — used by Validator in Phase 5
- `/log-activity` — every agent logs to project history
- `/query-history` — every agent reads history on startup

## When the Pipeline Finishes

1. All phases completed (or requested phases completed)
2. All quality gates passed
3. Infrastructure deployed and validated (if not --skip-deploy)
4. Gap analysis completed with improvement recommendations
5. Final report compiled
6. PR created with all changes
7. Project history updated by all agents
8. Team cleanup completed
