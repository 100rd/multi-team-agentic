---
name: pipeline-team
description: Full lifecycle pipeline team — research, design, implement, deploy, validate in one autonomous flow
model: opus
effort: high
---

# Pipeline Team Definition

A single unified agent team that runs the full lifecycle autonomously: **research → design → implement → deploy → validate → report**. Uses phased role spawning — the Lead spawns different specialists at each phase, shutting down completed-phase agents before moving to the next. This keeps the active agent count manageable (~4-5 at a time) while covering the entire journey from research to deployed infrastructure.

## Key Difference from Other Teams

| | `/infra-team` | `/ai-research` | `/pipeline` |
|---|---|---|---|
| **Scope** | Design → deploy | Research only | Research → design → deploy → validate |
| **Output** | Terraform + K8s code | Research reports | Both: research + code + deployment + gap analysis |
| **Autonomy** | Needs human at apply | Fully autonomous | Auto-approve dev/staging, human only for prod |
| **Phases** | Single phase | Single phase | 6 sequential phases |
| **Agent Lifecycle** | All spawn at once | All spawn at once | Phased: spawn, work, shutdown, next phase |

## Team Composition (Phased Spawning)

### Phase 1: Research (4 agents, parallel)

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **AI Architect** | solution-architect | `worktree` | Research AI system patterns — training clusters, inference serving, GPU/TPU topology, distributed training, model parallelism |
| **MLOps Researcher** | devops-engineer | `worktree` | Research MLOps pipelines — experiment tracking, model registries, feature stores, CI/CD for ML, model monitoring |
| **Infra Analyst** | terraform-engineer | `worktree` | Research compute infrastructure — cloud GPU instances, K8s for ML, storage, networking, cost modeling |
| **OSS Scout** | senior-backend-engineer | `worktree` | Map OSS ecosystem — frameworks (PyTorch, JAX, vLLM), serving solutions, orchestrators, vector DBs |

### Phase 2: Design (1 agent)

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **Solution Architect** | solution-architect | `worktree` | Design system architecture based on Phase 1 research — component diagrams, ADRs, AWS Well-Architected, trade-off analysis |

### Phase 3: Implement (2 agents, parallel)

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **Terraform Engineer** | terraform-engineer | `worktree` | Write Terraform/Terragrunt modules, tests, CI/CD for infrastructure |
| **DevOps Engineer** | devops-engineer | `worktree` | Write K8s manifests, Helm charts, ArgoCD config, deployment automation |

### Phase 4: Review (2 agents, parallel)

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **Security Reviewer** | security-expert | none | Review design + code for CIS compliance, IAM, encryption, network security |
| **Best Practices** | best-practices-validator | none | Review code against Terraform/K8s/AWS standards |

### Phase 5: Deploy + Validate (2 agents)

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **Validator** | infrastructure-validator | none | Post-apply health checks — DNS, SSL, K8s status, ArgoCD sync |
| **Gap Analyzer** | qa-engineer | none | Find gaps, problems, edge cases, missing configs, improvement opportunities |

### Phase 6: Report (Lead only)

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **Lead** | prime-orchestrator | none | Compile final report, commit to feature branch, create PR |

### Always Active

| Role | Agent Type | Isolation | Responsibility |
|------|-----------|-----------|----------------|
| **Lead** | prime-orchestrator | none | Coordinates all phases. Delegate mode — never writes research or code. Spawns/shuts down agents per phase. Approves plans. Compiles final report. |

## Phased Spawning Protocol

### How the Lead Manages Phase Transitions

```
┌─────────────────────────────────────────────────┐
│                LEAD (always active)             │
│                delegate mode                     │
└────────────────────┬────────────────────────────┘
                     │
    Phase 1          │ Spawn 4 researchers (parallel, worktree)
    RESEARCH         │ Wait for all to complete
                     │ Review research quality
                     │ Merge worktree branches
                     │ Shutdown all 4 researchers
                     │
    Phase 2          │ Spawn Solution Architect (plan mode, worktree)
    DESIGN           │ Approve/reject design plan
                     │ Wait for design completion
                     │ Merge worktree branch
                     │ Shutdown architect
                     │
    Phase 3          │ Spawn Terraform + DevOps (plan mode, worktree)
    IMPLEMENT        │ Approve/reject implementation plans
                     │ Wait for implementation completion
                     │ DO NOT shutdown yet (may need fixes from review)
                     │
    Phase 4          │ Spawn Security + Best Practices (normal, no isolation)
    REVIEW           │ Wait for reviews
                     │ If findings: message Phase 3 agents to fix
                     │ Re-review if needed
                     │ When all pass: merge worktree branches
                     │ Shutdown Phase 3 + 4 agents
                     │
    Phase 5          │ Terraform apply dev (AUTO-APPROVED)
    DEPLOY           │ Terraform apply staging (AUTO-APPROVED)
                     │ Spawn Validator + Gap Analyzer
                     │ Wait for validation and gap analysis
                     │ Shutdown Phase 5 agents
                     │
    Phase 6          │ Compile final report from all phases
    REPORT           │ Create feature branch
                     │ Commit all changes
                     │ Create PR
                     │ Update project history
                     │ Team cleanup
                     │
                     ▼ DONE
```

### Phase Transition Rules

1. **Phase N+1 does NOT start until Phase N is complete**
2. **"Complete" means**: all agents in that phase have finished AND Lead has reviewed output
3. **Exception**: Phase 3 agents stay alive through Phase 4 (may need to fix review findings)
4. **Shutdown is graceful**: Lead sends `shutdown_request`, agent approves, then terminates
5. **Research output persists**: Phase 1 writes to `project/{name}/research/` — these files persist for all later phases to read

## Communication Patterns

### Phase 1 (Research)

```
Lead ──► AI Architect: "Research training/inference architectures"
Lead ──► MLOps Researcher: "Research MLOps tooling landscape"
Lead ──► Infra Analyst: "Research compute infrastructure + costs"
Lead ──► OSS Scout: "Map open source framework ecosystem"

AI Architect ◄──► Infra Analyst: coordinate on GPU/compute details
MLOps Researcher ◄──► OSS Scout: coordinate on tool evaluations
Any ──► Lead: status updates, questions, completion
```

### Phase 2 (Design)

```
Lead ──► Solution Architect: "Design based on Phase 1 research at project/{name}/research/"
Solution Architect ──► Lead: submits plan for approval
Lead ──► Solution Architect: approve/reject with feedback
```

### Phase 3-4 (Implement + Review)

```
Lead ──► Terraform Engineer: "Implement design at project/{name}/docs/architecture/"
Lead ──► DevOps Engineer: "Write deployment configs per design"
Terraform Engineer ──► Security Reviewer: "Please review modules at path X"
DevOps Engineer ──► Security Reviewer: "Please review K8s manifests"
Security Reviewer ──► Terraform Engineer: "BLOCKED: finding X needs fix"
Best Practices ──► DevOps Engineer: "FINDING: missing resource limits"
```

### Phase 5 (Deploy + Validate)

```
Lead ──► Validator: "Validate deployment health"
Lead ──► Gap Analyzer: "Find gaps, problems, edge cases"
Validator ──► Lead: "Health check results: [pass/fail]"
Gap Analyzer ──► Lead: "Found N gaps: [list]"
```

## Task Dependency Chain

```
Phase 1 — Research (parallel)
  Task 1: Define research scope & assign threads (Lead)
  Task 2: AI system architecture research (AI Architect)         ─┐
  Task 3: MLOps tooling landscape research (MLOps Researcher)     ├── parallel
  Task 4: Infrastructure & cost research (Infra Analyst)          │
  Task 5: OSS ecosystem mapping (OSS Scout)                      ─┘
    │
    ▼ (blocked until 2-5 complete + Lead reviews)

Phase 2 — Design
  Task 6: System architecture design (Solution Architect, plan mode)
    → Lead approves/rejects plan
    │
    ▼ (blocked until 6 complete + approved)

Phase 3 — Implement (parallel)
  Task 7: Write Terraform modules (Terraform Engineer, plan mode) ─┐
    → Lead approves/rejects plan                                    ├── parallel
  Task 8: Write K8s/deployment configs (DevOps Engineer, plan mode)─┘
    → Lead approves/rejects plan
    │
    ▼ (blocked until 7+8 complete)

Phase 4 — Review (parallel)
  Task 9: Security review of design + code (Security Reviewer)   ─┐
  Task 10: Best practices review (Best Practices Validator)       ─┘ parallel
    │
    ▼ if findings → Task 11: Fix review findings (Phase 3 agents)
    │
    ▼ (blocked until 9+10 pass, all fixes applied)

Phase 5 — Deploy + Validate
  Task 12: terraform plan + apply to dev (AUTO-APPROVED)
  Task 13: Validate dev deployment (Validator)
    │
    ▼ (blocked until 13 passes)
  Task 14: terraform plan + apply to staging (AUTO-APPROVED)
  Task 15: Validate staging deployment (Validator)
  Task 16: Gap analysis (Gap Analyzer)
    │
    ▼ (blocked until 15+16 complete)

Phase 6 — Report + Deliver
  Task 17: Compile final report (Lead)
  Task 18: Create feature branch + commit (Lead)
  Task 19: Create Pull Request (Lead)
  Task 20: Update project history + cleanup (Lead)
```

## Plan Approval Criteria

### For Research Plans (Phase 1)

The Lead approves research plans when:
- [ ] Clear scope: which topics/technologies to cover
- [ ] Evaluation criteria defined (not just feature lists)
- [ ] Both open-source and commercial options included
- [ ] Practical "when to use what" guidance planned
- [ ] Citation/source requirements acknowledged

### For Design Plans (Phase 2)

The Lead approves design plans when:
- [ ] Informed by Phase 1 research (references specific findings)
- [ ] AWS Well-Architected Framework pillars addressed
- [ ] High availability and disaster recovery considered
- [ ] Cost-conscious (right-sized based on research cost analysis)
- [ ] Security by design (encryption, least privilege, network segmentation)
- [ ] Architecture Decision Records (ADRs) planned

### For Implementation Plans (Phase 3)

The Lead approves implementation plans when:
- [ ] Follows the design from Phase 2 (no unauthorized deviations)
- [ ] Module structure follows community conventions
- [ ] Tests included (unit + integration)
- [ ] Variables have descriptions and validation
- [ ] No hardcoded values
- [ ] State management strategy defined
- [ ] Rollback plan present

### Auto-Approve Criteria (Autonomous Pipeline Mode)

When running autonomously, the Lead can auto-approve plans if ALL criteria above are met. See `auto-approve-protocol.md` for full governance rules.

### Rejection Criteria (Auto-Reject)

- Missing security considerations
- No test strategy
- Hardcoded secrets or credentials
- Research scope too broad (trying to cover everything superficially)
- Design doesn't reference Phase 1 research
- Implementation deviates from approved design
- No rollback plan

## Quality Gates (Must ALL Pass)

| Gate | Phase | Check | Blocker |
|------|-------|-------|---------|
| G1 | 1 | Research scope well-defined, no gaps | Lead |
| G2 | 1 | Research findings are substantiated | Lead (reviews) |
| G3 | 2 | Design addresses Well-Architected pillars | Lead |
| G4 | 2 | Design references research findings | Lead |
| G5 | 3 | terraform fmt + validate pass | Automated |
| G6 | 3 | Checkov/tfsec security scan passes | Security Reviewer |
| G7 | 4 | Security review passes | Security Reviewer |
| G8 | 4 | Best practices review passes | Best Practices |
| G9 | 5 | terraform plan shows expected changes | Lead |
| G10 | 5 | Post-apply validation healthy | Validator |
| G11 | 5 | Gap analysis completed | Gap Analyzer |
| G12 | 6 | Final report coherent and complete | Lead |

## Auto-Approve Integration

### How Auto-Approve Works in the Pipeline

1. The `/pipeline` command accepts `--auto-approve dev,staging` (default)
2. The Lead includes auto-approve scope in terraform-related teammate prompts
3. `scripts/terraform-env-check.sh` is called by settings.json hooks automatically
4. For dev/staging: hook returns exit 0 with AUTO_APPROVED message → agent proceeds
5. For prod: hook returns exit 1 with BLOCKED message → agent stops, waits for human

### Environments

| Environment | terraform apply | terraform destroy |
|-------------|----------------|-------------------|
| dev | AUTO | AUTO |
| staging | AUTO | CHECKPOINT |
| prod | BLOCKED | BLOCKED |
| unknown | CHECKPOINT | CHECKPOINT |

See `auto-approve-protocol.md` for full governance rules.

## Handling Failures

### Phase 1 Failures

- Research hits dead end → researcher reports to Lead, scope adjusted
- Researcher produces shallow output → Lead requests deeper analysis
- 3+ revision requests → Lead accepts current output, notes limitation in report

### Phase 2 Failures

- Design doesn't reference research → Lead rejects, points to specific research files
- Design over-provisions → Lead rejects, requests right-sizing

### Phase 3-4 Failures

- Security review fails → implementer fixes, re-submits for review
- Best practices fails → implementer fixes, re-submits
- 3+ review cycles → Lead intervenes with specific guidance
- Implementation deviates from design → Lead rejects, refers back to design doc

### Phase 5 Failures

- terraform apply fails → Lead asks implementers to investigate (respawn if needed)
- Validation fails → Gap Analyzer investigates, Lead may respawn implementers
- 3+ apply failures → Escalate to human

### General

- If any phase produces no output after max retries → pipeline aborts with partial report
- All failures logged to project history

## Working Directory Convention

```
project/{project-name}/
│
├── research/                    # ═══ Phase 1 output ═══
│   ├── executive-summary.md     # TL;DR with key findings
│   ├── sections/
│   │   ├── ai-architecture.md   # AI Architect writes here
│   │   ├── mlops-landscape.md   # MLOps Researcher writes here
│   │   ├── infrastructure.md    # Infra Analyst writes here
│   │   └── oss-ecosystem.md     # OSS Scout writes here
│   ├── comparisons/             # Decision matrices
│   │   ├── training-frameworks.md
│   │   ├── serving-solutions.md
│   │   ├── mlops-platforms.md
│   │   └── cloud-gpu-pricing.md
│   └── references/
│       └── bibliography.md
│
├── docs/                        # ═══ Phase 2 output ═══
│   └── architecture/
│       ├── system-design.md     # Solution Architect writes here
│       ├── decisions/           # Architecture Decision Records
│       │   ├── ADR-001-compute.md
│       │   ├── ADR-002-network.md
│       │   └── ADR-003-storage.md
│       └── diagrams/
│
├── terraform/                   # ═══ Phase 3 output (Terraform Engineer) ═══
│   ├── modules/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── tests/
│
├── kubernetes/                  # ═══ Phase 3 output (DevOps Engineer) ═══
│   ├── manifests/
│   ├── helm/
│   └── argocd/
│
├── security/                    # ═══ Phase 4 output ═══
│   └── review-reports/
│       ├── design-review.md
│       └── code-review.md
│
├── validation/                  # ═══ Phase 5 output ═══
│   └── reports/
│       ├── dev-validation.md
│       ├── staging-validation.md
│       └── gap-analysis.md
│
└── final-report.md              # ═══ Phase 6 — Lead compiles ═══
```

## Example: AI Inference Platform Pipeline

User says: `/pipeline "Build a production LLM inference platform on AWS with auto-scaling, multi-model serving, and cost optimization"`

### Execution:

**Phase 1 — Research (4 agents, ~20 min)**

Lead creates team, spawns 4 researchers:

1. **AI Architect** researches:
   - Serving architectures (single-model vs multi-model vs router)
   - Batching strategies (continuous, speculative decoding)
   - KV cache management, PagedAttention
   - Multi-GPU inference (tensor parallelism, pipeline parallelism)

2. **MLOps Researcher** researches:
   - LLM monitoring (TTFT, TPS, latency percentiles)
   - Model versioning and A/B testing
   - Cost tracking dashboards
   - Prompt management

3. **Infra Analyst** researches:
   - GPU instances: A100 vs H100 vs L40S vs Inferentia2
   - EKS with Karpenter for GPU autoscaling
   - Cost: reserved vs spot vs Bedrock/SageMaker
   - Storage: model artifact caching strategies

4. **OSS Scout** maps:
   - Serving: vLLM, TGI, TensorRT-LLM, Triton, SGLang
   - Quantization: GPTQ, AWQ, FP8
   - Routing: LiteLLM, OpenRouter patterns

→ All write to `project/llm-inference/research/`
→ Lead reviews quality → Shuts down 4 researchers

**Phase 2 — Design (1 agent, ~10 min)**

Lead spawns Solution Architect with context: "Read research at project/llm-inference/research/"

- Designs multi-model serving platform on EKS
- Uses vLLM on GPU nodes with Karpenter autoscaling
- Adds API Gateway + Lambda for routing
- Writes ADRs for key decisions
- Submits plan → Lead approves

→ Writes to `project/llm-inference/docs/architecture/`
→ Lead shuts down architect

**Phase 3 — Implement (2 agents, ~15 min)**

Lead spawns Terraform Engineer + DevOps Engineer:

- **Terraform**: VPC, EKS, GPU node groups, ALB, S3 for models, IAM
- **DevOps**: Helm charts for vLLM, Karpenter configs, ArgoCD apps, monitoring

→ Write to `project/llm-inference/terraform/` and `kubernetes/`

**Phase 4 — Review (2 agents, ~10 min)**

Lead spawns Security + Best Practices:

- **Security**: "SG needs tighter rules on port 8080", "Add encryption for S3 model bucket"
- **Best Practices**: "Add resource limits to vLLM pods", "Use Terraform modules for DRY"

→ Phase 3 agents fix findings → Re-reviewed → Pass
→ Lead shuts down Phase 3+4 agents

**Phase 5 — Deploy + Validate (~15 min)**

- `terraform apply` to dev → **AUTO-APPROVED** → Applied
- Validator checks: EKS healthy, pods running, ALB responding
- `terraform apply` to staging → **AUTO-APPROVED** → Applied
- Validator checks: staging healthy
- Gap Analyzer: "Missing HPA for vLLM pods", "No PDB configured", "Consider adding Prometheus ServiceMonitor"

→ Lead shuts down Phase 5 agents

**Phase 6 — Report**

Lead compiles `final-report.md`:
- Executive summary of the full journey
- Research highlights
- Architecture decisions
- What was deployed
- Validation results
- Gaps found (from Gap Analyzer)
- Recommendations for prod deployment

→ Creates feature branch, commits, creates PR
→ Team cleanup

**Total**: One PR with research + design + infrastructure + deployment + gap analysis
