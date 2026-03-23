---
paths:
  - "**"
---

# Orchestration Flow

When user asks to do something:

1. **Identify scope** — Full system design or quick task?
2. **Choose mode** — Agent team (complex) or subagent (simple)?
3. **Check history** — What was done before? `/query-history`
4. **Launch team or delegate** — Use the right tool for the job
5. **Monitor progress** — Track task completion
6. **Quality gates** — Ensure all reviews pass
7. **Deliver** — Commit, PR, update history

## Primary Workflows

### Infrastructure System Design
**Triggers**: `/design-system`, `/infra-team`, "design a system", "create infrastructure"
Spawns a self-managed agent team for the full lifecycle.

### AI Deep Research
**Triggers**: `/ai-research`, "research AI infrastructure", "compare inference frameworks"
Spawns research team with parallel threads, fact-checking, peer review.

### Full Lifecycle Pipeline
**Triggers**: `/pipeline`, "research and build", "full lifecycle"
Phased spawning: research -> design -> implement -> deploy -> validate -> report.

### Competing Hypothesis Investigation
**Triggers**: `/investigate`, "debug this", "why is X happening"
Spawns parallel agents testing different theories adversarially.

### Project Initialization
**Triggers**: `/project`, "start new project", "initialize"
Workflow: [docs/workflows/project-initialization.md](docs/workflows/project-initialization.md)

### Feature Development
**Triggers**: `/start-feature`, "implement feature", "begin coding"
Workflow: [docs/workflows/feature-development.md](docs/workflows/feature-development.md)

### Deployment
**Triggers**: "deploy", "release", "go to production"
Workflow: [docs/workflows/deployment.md](docs/workflows/deployment.md)

## Agent Categories

- `teams/` — Pre-configured agent teams
- `engineering/` — Developers (frontend, backend, fullstack, terraform)
- `architecture/` — System designers
- `operations/` — DevOps, SRE, migration
- `security/` — Security experts
- `quality/` — QA, testing
- `review/` — Simplifier, best practices
- `validation/` — Infrastructure validators
- `product/` — Product managers
- `memory/` — Activity tracking

## Status Tracking

- Overall: `cat PROJECT_STATUS.md`
- Feature: `/project-status --feature [name]`
- Task locks: `ls project/.locks/`
- History: `/query-history --limit 20`

## Project History

Every agent MUST:
1. **Read history on startup** (startup-protocol.md)
2. **Write history on shutdown** (shutdown-protocol.md)

History files:
- `project/PROJECT_HISTORY.md` — human-readable chronological log
- `project/project_history.json` — machine-queryable structured data
