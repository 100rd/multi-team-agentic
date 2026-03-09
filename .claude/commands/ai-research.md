---
name: ai-research
description: Launch a self-managed AI research agent team for deep analysis of AI infrastructure, training, fine-tuning, inference, and MLOps
args: "<research-topic> [--project NAME] [--focus training|inference|mlops|oss|all] [--depth shallow|deep|comprehensive]"
---

# AI Research Team Command

Spawns a native Claude Code agent team specialized for deep research in AI infrastructure and software architecture. The team self-manages through scope definition -> parallel research -> fact-check -> peer review -> synthesize -> report.

## What This Command Does

1. **Creates an agent team** with the Lead in delegate mode (coordination only)
2. **Spawns specialized researchers** based on the research topic
3. **Creates a task list** with dependencies that auto-unblock
4. **Requires plan approval** before any research thread begins
5. **Runs quality gates** at every stage (fact-checking, peer review)
6. **Produces a comprehensive research report** with citations and comparison matrices

## Team Roles

| Teammate | Agent | Mode | Responsibility |
|----------|-------|------|----------------|
| AI Architect | solution-architect | plan first | AI system design patterns, training/inference architectures |
| MLOps Researcher | devops-engineer | plan first | MLOps pipelines, experiment tracking, model monitoring |
| Infra Analyst | terraform-engineer | plan first | Compute infrastructure, cloud GPU, cost modeling |
| OSS Scout | senior-backend-engineer | normal | Open source ecosystem mapping, framework comparisons |
| Fact Checker | qa-engineer | normal | Citation verification, claim validation, freshness checks |
| Peer Reviewer | best-practices-validator | normal | Quality, depth, bias, and objectivity review |

## Execution Flow

When this command is invoked:

### Phase 1: Team Setup
```
Create agent team "research-{project}-{timestamp}"
Enable delegate mode on Lead (Shift+Tab)
Spawn researchers with appropriate agent types
Set all researchers to plan-approval-required mode
```

### Phase 2: Scope Definition
```
Task 1: Define research scope and questions [Lead]
  → Break topic into parallel research threads
  → Define evaluation criteria and comparison dimensions
  → Set citation and freshness requirements
```

### Phase 3: Parallel Research (Plan Approval Required)
```
Task 2: AI architecture research [AI Architect, plan mode]
  → Lead reviews and approves/rejects research plan
Task 3: MLOps landscape research [MLOps Researcher, plan mode]
  → Lead reviews and approves/rejects research plan
Task 4: Infrastructure & cost research [Infra Analyst, plan mode]
  → Lead reviews and approves/rejects research plan
Task 5: OSS ecosystem mapping [OSS Scout]
  → All four threads run in parallel after approval
```

### Phase 4: Quality Review
```
Task 6: Fact-check all findings [Fact Checker]
  → Verify citations, flag outdated info, check benchmarks
Task 7: Peer review all sections [Peer Reviewer]
  → Review depth, objectivity, practical applicability
  → Both must pass before proceeding
```

### Phase 5: Revision
```
Task 8: Revise based on review feedback [original researchers]
  → Address all fact-check and peer review findings
  → Re-review if needed
```

### Phase 6: Synthesis & Delivery
```
Task 9: Synthesize final report [Lead]
  → Compile all sections into coherent report
  → Write executive summary
  → Create comparison matrices
Task 10: Commit report and create PR [Lead]
```

## Usage Examples

```bash
# Comprehensive inference optimization research
/ai-research "Compare inference optimization strategies for LLMs — vLLM, TensorRT-LLM, and Triton for production serving at scale"

# Training infrastructure deep dive
/ai-research "Design training infrastructure for fine-tuning 70B parameter models — distributed training, checkpointing, cost analysis" --project llm-finetune --focus training

# MLOps landscape analysis
/ai-research "Full landscape analysis of MLOps tooling in 2026 — experiment tracking, model registry, feature store, monitoring" --focus mlops --depth comprehensive

# Cloud GPU comparison
/ai-research "Compare cloud GPU offerings for ML workloads — AWS, GCP, Azure, CoreWeave pricing and performance" --focus inference --project gpu-comparison

# RAG architecture research
/ai-research "Research RAG architectures for enterprise — vector databases, embedding strategies, retrieval patterns, evaluation methods"

# Fine-tuning methods comparison
/ai-research "Compare fine-tuning approaches for LLMs — LoRA, QLoRA, full fine-tuning, when to use each, cost/quality tradeoffs" --depth deep

# On-premise vs cloud for AI
/ai-research "Analyze on-premise vs cloud strategies for AI training and inference — TCO, latency, data sovereignty, hybrid approaches"
```

## Research Output

After the team finishes, you get:

```
project/{name}/
├── research/
│   ├── final-report.md              # Comprehensive synthesized report
│   ├── executive-summary.md         # TL;DR with key findings & recommendations
│   │
│   ├── sections/                    # Individual research threads
│   │   ├── ai-architecture.md       # Training/inference architectures
│   │   ├── mlops-landscape.md       # MLOps tooling analysis
│   │   ├── infrastructure.md        # Compute/storage/networking/cost
│   │   └── oss-ecosystem.md         # Open source framework map
│   │
│   ├── comparisons/                 # Decision matrices
│   │   ├── training-frameworks.md   # PyTorch vs JAX vs ...
│   │   ├── serving-solutions.md     # vLLM vs TGI vs Triton vs ...
│   │   ├── mlops-platforms.md       # MLflow vs W&B vs ...
│   │   ├── cloud-gpu-pricing.md     # AWS vs GCP vs Azure GPU costs
│   │   └── fine-tuning-methods.md   # LoRA vs QLoRA vs full FT
│   │
│   ├── reviews/                     # Quality gate artifacts
│   │   ├── fact-check-report.md     # All verified/flagged claims
│   │   └── peer-review-report.md    # Quality assessment
│   │
│   └── references/
│       └── bibliography.md          # All sources cited
```

Plus:
- All changes on a feature branch
- Pull Request with full description
- Project history updated by all team members

## Quality Guarantees

Every research deliverable passes through:

| Gate | What | Who Reviews |
|------|------|-------------|
| Scope Review | Research questions are well-defined | Lead |
| Plan Approval | Research approach is sound and complete | Lead |
| Citation Check | All claims have verifiable sources | Fact Checker |
| Freshness Check | No outdated info for fast-moving topics | Fact Checker |
| Objectivity Check | Comparisons are fair and balanced | Peer Reviewer |
| Depth Check | Analysis goes beyond surface-level | Peer Reviewer |
| Practical Check | Recommendations are actionable | Peer Reviewer |
| Coherence Check | Final report is consistent and complete | Lead |

## Team Spawn Prompt Template

The Lead will spawn each researcher with a detailed prompt including:

```
You are the {ROLE} on the AI research team for: {RESEARCH_TOPIC}

Project: {PROJECT_NAME}
Working directory: project/{PROJECT_NAME}/research/
Your output directory: project/{PROJECT_NAME}/research/sections/{YOUR_SECTION}

Your research thread:
{ROLE_SPECIFIC_RESEARCH_QUESTIONS}

Research standards:
- Every factual claim MUST have a citation (official docs, papers, benchmarks)
- Comparisons must define clear evaluation criteria
- Include "when to use" practical guidance, not just feature lists
- Flag anything you're uncertain about rather than guessing
- Prefer primary sources (official docs, papers) over blog posts
- Note the date of any benchmark or pricing data you reference

Communication rules:
- Message the Lead for status updates and blockers
- Message other researchers for cross-thread coordination
- Never edit files outside your assigned directories
- Follow the plan approval protocol before starting research

Quality requirements:
- All claims must be verifiable
- Comparisons must be fair (same benchmarks, similar configs)
- Include both strengths AND limitations of each option
- Provide actionable recommendations, not just information

Read project history first:
cat project/PROJECT_HISTORY.md | tail -50
```

## Focus Mode

Use `--focus` to narrow the team to specific research areas:

| Focus | Active Researchers | Reduced Team |
|-------|-------------------|--------------|
| `training` | AI Architect, Infra Analyst, OSS Scout | 5 agents |
| `inference` | AI Architect, Infra Analyst, OSS Scout | 5 agents |
| `mlops` | MLOps Researcher, OSS Scout | 4 agents |
| `oss` | OSS Scout (expanded scope) | 3 agents |
| `all` (default) | All researchers | 7 agents |

## Depth Levels

| Depth | Description | Typical Output |
|-------|-------------|----------------|
| `shallow` | Quick survey, key findings only | 5-10 page report |
| `deep` (default) | Thorough analysis with comparisons | 15-30 page report |
| `comprehensive` | Exhaustive research with benchmarks | 30-50+ page report |

## Resuming a Research Session

If you need to continue research from a previous session:

```bash
# Check what was researched before
/query-history --tag {project-name} --limit 20

# Resume where you left off
/ai-research "Continue the inference optimization research" --project llm-inference
```

The team will read project history and pick up where the last session ended.

## Arguments

- `research-topic`: Natural language description of what to research
- `--project NAME`: Project directory name (created under `project/`)
- `--focus training|inference|mlops|oss|all`: Narrow research scope (default: all)
- `--depth shallow|deep|comprehensive`: Research depth level (default: deep)

## Integration with Existing Commands

This command integrates with:
- `/log-activity` — every researcher logs to project history
- `/query-history` — every researcher reads history on startup
- `/investigate` — can be used for deep-dive into specific sub-topics

## When the Team Finishes

1. All tasks marked complete
2. All quality gates passed
3. Research report synthesized and committed
4. PR created with all research artifacts
5. Team cleanup runs (removes team resources)
6. Project history updated by all researchers
