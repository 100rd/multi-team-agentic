# HOW-TO: Multi-Agent Squad Complete Usage Guide

This is the comprehensive manual for using the Multi-Agent Squad orchestration system. It covers starting new projects, continuing existing work, using agent teams, and getting fully tested deliverables.

---

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Starting a New Project](#2-starting-a-new-project)
3. [Continuing an Existing Project](#3-continuing-an-existing-project)
4. [Using Agent Teams](#4-using-agent-teams)
5. [Infrastructure Team (infra-team)](#5-infrastructure-team)
6. [System Design Workflow](#6-system-design-workflow)
7. [Competing Hypothesis Investigation](#7-competing-hypothesis-investigation)
8. [Project History & Memory](#8-project-history--memory)
9. [Commands Reference](#9-commands-reference)
10. [Troubleshooting](#10-troubleshooting)
11. [Advanced Patterns](#11-advanced-patterns)

---

## 1. Quick Start

### First-Time Setup

```bash
# 1. Ensure tmux is installed (for split-pane agent teams)
brew install tmux          # macOS
# or: sudo apt install tmux  # Ubuntu

# 2. Start Claude Code
claude

# 3. Verify agent teams are enabled
# Check: settings.json should have CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"
```

### The 3 Main Workflows

| What You Want | Command | What Happens |
|---------------|---------|-------------|
| Design + build new infrastructure | `/design-system "description"` | Full agent team: design → implement → test → deploy → PR |
| Launch infra specialists only | `/infra-team "task"` | Infrastructure team self-manages the task |
| Debug an infrastructure issue | `/investigate "problem"` | 3-5 agents test competing hypotheses |

### Simplest Possible Usage

```
You: /design-system "Create a highly available EKS cluster with Karpenter auto-scaling"

→ Agent team spawns automatically
→ Architect designs the cluster
→ Security reviews the design
→ Cost analyst estimates budget
→ Terraform engineer writes modules
→ All reviews pass
→ Applied to dev, validated
→ PR created

You: Review and merge the PR
```

---

## 2. Starting a New Project

### Option A: Full System Design (Recommended for Infrastructure)

Use when you want a complete, tested infrastructure deliverable.

```bash
# Describe what you want in natural language
/design-system "Multi-tenant SaaS platform on AWS with:
  - EKS cluster with Karpenter
  - RDS Aurora PostgreSQL with read replicas
  - ElastiCache Redis for session management
  - CloudFront CDN
  - WAF for API protection
  - Per-tenant encryption with KMS"
```

**What happens:**
1. Agent team spawns (7 specialists)
2. Each teammate visible in tmux pane
3. Architect creates design doc (you approve)
4. Security + Cost review in parallel
5. Terraform engineer implements (you approve plan)
6. Code reviewed by Security + Best Practices
7. Applied to dev environment (you approve terraform apply)
8. Validated automatically
9. Committed to feature branch, PR created

**Your involvement:** Approve 3 checkpoints (design, implementation plan, terraform apply). Everything else is automated.

### Option B: Simple Project Init

Use when you want to set up a project directory and work incrementally.

```bash
/project
```

**What happens:**
1. Asks for project name and description
2. Creates `project/{name}/` directory structure
3. Sets up project history files
4. Ready for incremental work

### Option C: Feature-Based Start

Use when you want to add something to an existing project.

```bash
/start-feature "Add monitoring dashboard for EKS cluster" --project platform-design
```

**What happens:**
1. Creates GitHub issue
2. Creates git worktree
3. Assigns agents
4. Begins implementation

---

## 3. Continuing an Existing Project

### The System Tracks Everything

Every agent writes to project history when it finishes. When you start a new session, agents automatically read this history.

### Step 1: See What Was Done Before

```bash
# Quick overview of recent activity
/query-history --limit 20

# See what happened on a specific project
/query-history --tag platform-design --limit 10

# See past decisions
/query-history --action design_decision

# See failures and issues
/query-history --failed
```

### Step 2: Continue Where You Left Off

```bash
# Continue a design system project
/design-system "Continue implementing the HFT system" --project hft-system

# Continue a specific feature
/start-feature "Continue the VPC redesign" --project platform-design

# Or just tell me what you want to do
"Continue working on the EKS Karpenter setup from yesterday"
```

**How it works:**
1. Agents read `project/PROJECT_HISTORY.md` on startup
2. They see what was done, what's pending, what failed
3. They pick up from where the last session ended
4. No context is lost between sessions

### Step 3: Check Active Task Locks

```bash
# See what tasks are currently claimed
ls project/.locks/

# See active tasks with details
for f in project/.locks/*.lock; do cat "$f"; done

# Clean up stale locks from crashed sessions
find project/.locks/ -name "*.lock" -mmin +1440 -delete
```

---

## 4. Using Agent Teams

### What Are Agent Teams?

Agent teams are multiple Claude Code sessions running in parallel, each in its own context window. They communicate directly with each other through messaging, coordinate through a shared task list, and self-manage their work.

### Agent Teams vs Subagents

| Feature | Agent Team | Subagent |
|---------|-----------|----------|
| **Persistence** | Runs until shutdown | Dies when done |
| **Communication** | Messages any teammate | Reports to caller only |
| **Task coordination** | Shared task list | Caller manages |
| **Visibility** | tmux split panes | Hidden |
| **Cost** | Higher (multiple contexts) | Lower |
| **Best for** | Complex, multi-role work | Quick, focused tasks |

### How to Interact with Agent Teams

#### In tmux mode (default):
- Each teammate gets its own pane
- **Click into a pane** to interact with that teammate
- You can see all agents working simultaneously
- Each teammate has a full Claude Code session

#### In in-process mode:
- `Shift+Up/Down` — select a teammate
- `Enter` — view a teammate's session
- `Escape` — interrupt a teammate's current turn
- `Ctrl+T` — toggle the shared task list

#### Talking to teammates directly:
You can message any teammate without going through the Lead:
```
# Select the terraform engineer pane (click or Shift+Down)
"Add lifecycle ignore_changes for the EBS volumes"
```

#### Monitoring progress:
- Watch each pane for activity
- `Ctrl+T` to see the shared task list
- Ask the Lead: "What's the current status?"

### Team Lifecycle

```
1. You invoke /infra-team or /design-system
2. Lead creates team → spawns teammates
3. Teammates get their own panes
4. Shared task list created with dependencies
5. Teammates claim tasks → work → complete → claim next
6. Lead approves plans, synthesizes results
7. You approve human checkpoints (terraform apply)
8. Team delivers PR
9. Lead cleans up team resources
```

### Delegate Mode

**Strongly recommended** for infrastructure teams.

After the team spawns, the Lead enters delegate mode:
- ✅ Can: spawn, message, manage tasks, approve plans
- ❌ Cannot: write files, run commands, implement code

This prevents the Lead from "doing the work itself" instead of delegating.

**To enable:** Press `Shift+Tab` after team creation, or tell the lead:
```
"Enter delegate mode — only coordinate, don't implement"
```

### Plan Approval Workflow

Implementers (Architect, Terraform, DevOps) start in **plan mode**:

1. Teammate explores codebase, researches approach
2. Teammate submits plan to Lead
3. Lead evaluates against criteria:
   - Security considered?
   - Tests planned?
   - Cost-conscious?
   - Rollback plan?
   - Best practices followed?
4. If approved → teammate exits plan mode, implements
5. If rejected → teammate revises based on feedback

**You can influence approval criteria:**
```
"Only approve plans that include Checkov scanning and unit tests"
"Reject any plan that uses t2 instances instead of t3"
```

---

## 5. Infrastructure Team

### What is the Infrastructure Team?

A pre-configured agent team of 7 specialists for infrastructure work. Defined in `.claude/agents/teams/infra-team.md`.

### Roles

| Teammate | Does What |
|----------|----------|
| **Lead** | Coordinates everything (delegate mode) |
| **Architect** | Designs system architecture |
| **Terraform Engineer** | Writes Terraform/Terragrunt modules + tests |
| **DevOps Engineer** | Writes K8s manifests, Helm, ArgoCD, CI/CD |
| **Security Reviewer** | CIS compliance, IAM, encryption review |
| **Cost Analyst** | Cost estimation, right-sizing |
| **Validator** | Post-deploy health checks |
| **Best Practices** | Standards enforcement |

### How to Launch

```bash
# Basic
/infra-team "Design VPC architecture with Transit Gateway for multi-account"

# With project context
/infra-team "Add Karpenter auto-scaling to EKS" --project platform-design

# With environment target
/infra-team "Create DR environment" --env prod --project snips
```

### Task Flow

```
Design ──► Security Review ──► Cost Estimate
                │                    │
                ▼                    ▼
         Both must pass before implementation
                │
                ▼
        Implement (Terraform + K8s)
                │
                ▼
        Security + Best Practices review code
                │
                ▼
        terraform plan + validate
                │
                ▼
        terraform apply (dev) ← YOU APPROVE
                │
                ▼
        Validate deployment
                │
                ▼
        Promote to staging ← YOU APPROVE
                │
                ▼
        Commit + PR
```

### Quality Gates

Every deliverable must pass:

| # | Gate | Reviewer |
|---|------|----------|
| 1 | Architecture design reviewed | Security |
| 2 | Cost within budget | Cost Analyst |
| 3 | terraform fmt + validate | Terraform Engineer |
| 4 | Checkov/tfsec security scan | Security |
| 5 | Best practices compliance | Best Practices |
| 6 | terraform plan clean | Terraform Engineer |
| 7 | Post-apply health check | Validator |
| 8 | Deployment functional | Validator |

### What You Get at the End

```
project/{name}/
├── docs/architecture/        # Design docs + ADRs
├── terraform/modules/        # Tested Terraform modules
├── terraform/environments/   # Per-env configuration
├── kubernetes/               # K8s manifests
├── security/review-reports/  # Security review results
└── validation/reports/       # Deployment validation
```

Plus: Feature branch, PR, updated project history.

---

## 6. System Design Workflow

### /design-system is Your Main Command

It's the "do everything" command for infrastructure:

```bash
/design-system "High-frequency trading system on AWS with:
  - Ultra-low-latency networking (DPDK, placement groups)
  - FPGA acceleration for order matching
  - Multi-AZ active-active with sub-ms failover
  - Market data ingestion pipeline
  - Time sync via PTP"
```

### Complete Lifecycle

```
PHASE 1: DESIGN                    PHASE 2: IMPLEMENT
┌─────────────────────┐            ┌──────────────────────┐
│ Architect designs    │            │ Terraform writes IaC │
│ Security reviews     │    ──►     │ DevOps writes K8s    │
│ Cost estimates       │            │ Security reviews code│
│ Lead approves        │            │ Practices validates  │
└─────────────────────┘            └──────────────────────┘
                                            │
PHASE 3: TEST                      PHASE 4: DEPLOY
┌─────────────────────┐            ┌──────────────────────┐
│ terraform validate   │            │ terraform apply (dev)│
│ Checkov scan         │    ──►     │ ⚠️ Human approval     │
│ terraform plan       │            │ Validate deployment  │
│ Unit tests           │            │ Health checks        │
└─────────────────────┘            └──────────────────────┘
                                            │
PHASE 5: PROMOTE                   PHASE 6: DELIVER
┌─────────────────────┐            ┌──────────────────────┐
│ Promote to staging   │            │ Create feature branch│
│ Full validation      │    ──►     │ Commit all changes   │
│ ⚠️ Human for prod     │            │ Create Pull Request  │
│ Final health check   │            │ Update history       │
└─────────────────────┘            └──────────────────────┘
```

### Arguments

```bash
/design-system "description"           # Basic
/design-system "desc" --project NAME   # Into specific project dir
/design-system "desc" --cloud aws      # Target cloud (default: aws)
/design-system "desc" --budget 5000    # Monthly budget cap
/design-system "desc" --skip-deploy    # Stop after code review
/design-system "desc" --env-only dev   # Only deploy to dev
```

### Examples

```bash
# New system from scratch
/design-system "Event-driven microservices platform with EKS, SQS, and DynamoDB"

# Evolve existing system
/design-system "Add monitoring and alerting to platform" --project platform-design

# Migration
/design-system "Migrate from ECS to EKS with zero downtime" --project snips

# DR setup
/design-system "Create disaster recovery in us-west-2" --project opsfleet
```

---

## 7. Competing Hypothesis Investigation

### When to Use

When something is broken and you don't know why:

```bash
/investigate "EKS pods are OOMKilled after 2 hours of running"
/investigate "terraform plan shows 15 resources to recreate unexpectedly"
/investigate "API latency increased 3x after last deployment"
/investigate "Intermittent 503 errors from production ALB"
```

### How It Works

1. Lead generates 3-5 competing hypotheses
2. One agent per hypothesis investigates in parallel
3. Agents message each other to challenge findings
4. The theory that survives adversarial debate wins
5. Lead synthesizes root cause + action plan

### Why This Is Better Than Single-Agent Debug

**Single agent:** Finds one plausible explanation, stops looking (anchoring bias)
**Competing agents:** Each tries to disprove the others. The surviving theory is much more likely to be correct.

### Example

```
You: /investigate "EKS pods keep getting OOMKilled"

Lead generates hypotheses:
  H1: Memory leak in application code
  H2: Insufficient resource limits/requests
  H3: Sidecar container consuming memory
  H4: Node-level DaemonSet pressure

4 agents spawn and investigate in parallel...

Agent 1 (H1): "Found Go goroutine leak in handler.go line 142"
Agent 2 (H2): "Limits are set correctly at 512Mi, but actual usage hits 800Mi"
Agent 3 (H3): "Istio sidecar using only 30Mi — not the cause"
Agent 4 (H4): "Node has 2Gi free — not node pressure"

Agent 2 → Agent 1: "Your goroutine leak explains why usage exceeds limits"
Agent 3 → Agent 1: "Confirmed — the leak is consistent with OOM timeline"

Lead synthesizes:
  Root cause: Goroutine leak in handler.go line 142
  Fix: Close goroutine after HTTP response
  Prevention: Add goroutine count metric + alert
```

### Arguments

```bash
/investigate "description"                  # Default 3 hypotheses
/investigate "description" --hypotheses 5   # More hypotheses
/investigate "description" --adversarial    # Enable debate (default)
```

---

## 8. Project History & Memory

### How the Memory System Works

Every agent follows two mandatory protocols:

**On startup (before doing any work):**
1. Read `project/PROJECT_HISTORY.md`
2. Query relevant entries from `project/project_history.json`
3. Understand past decisions, avoid contradictions

**On shutdown (before returning results):**
1. Write markdown entry to `PROJECT_HISTORY.md`
2. Write JSON entry to `project_history.json`
3. Include: what was done, files changed, outcome, tags

### Query History

```bash
# Recent activity
/query-history --limit 20

# By project
/query-history --tag hft-system

# By agent
/query-history --agent terraform-engineer

# By action type
/query-history --action design_decision

# Past failures
/query-history --failed

# Changes to specific files
/query-history --file terraform/modules/vpc/main.tf
```

### Why This Matters

- **No duplicate work**: Agents see what was already done
- **Consistent decisions**: Past architecture decisions are respected
- **Learning from failures**: Past errors inform current approach
- **Cross-session continuity**: Pick up where you left off

### Manual History Entry

```bash
/log-activity --agent manual --action-type implementation \
  --description "Manually updated VPC CIDR ranges" \
  --files "terraform/modules/vpc/variables.tf" \
  --tags "infrastructure,vpc,manual"
```

---

## 9. Commands Reference

### Team Commands

| Command | Description |
|---------|------------|
| `/infra-team "task"` | Launch infrastructure agent team |
| `/design-system "desc"` | Full lifecycle: design → deploy → PR |
| `/investigate "problem"` | Competing hypothesis debugging |

### Project Commands

| Command | Description |
|---------|------------|
| `/project` | Initialize new project |
| `/project-init` | Full project setup |
| `/project-status` | Show current status |
| `/start-feature "name"` | Start feature with orchestration |
| `/create-agent` | Create new specialized agent |
| `/manage-worktrees` | Git worktree management |

### Infrastructure Commands

| Command | Description |
|---------|------------|
| `/blast-radius path` | Analyze terraform change impact |
| `/cost-estimate path` | Estimate monthly cost changes |
| `/validate-deployment app` | Post-deploy health checks |
| `/promote-environment dev staging` | Promote between environments |
| `/terraform-migration` | Migrate CloudFormation → Terraform |

### History Commands

| Command | Description |
|---------|------------|
| `/query-history` | Search project history |
| `/log-activity` | Add manual history entry |

---

## 10. Troubleshooting

### Agent team not spawning

**Cause:** Feature flag not enabled.
**Fix:** Check `.claude/settings.json` has `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` in the `env` block.

### tmux panes not appearing

**Cause:** tmux not installed or not in PATH.
**Fix:**
```bash
brew install tmux        # macOS
which tmux               # Verify it's found
```

**Alternative:** Use in-process mode:
```bash
claude --teammate-mode in-process
```

### Lead implementing instead of delegating

**Cause:** Delegate mode not enabled.
**Fix:** Press `Shift+Tab` after team creation, or say:
```
"Enter delegate mode. Only coordinate, never implement."
```

### Teammates stopping on errors

**Fix:** Click into the teammate's pane and give additional instructions:
```
"Retry the terraform validate — ignore the deprecated warning"
```

Or ask the Lead to spawn a replacement:
```
"The terraform engineer is stuck. Spawn a replacement."
```

### Stale task locks

**Cause:** Previous session crashed without cleanup.
**Fix:**
```bash
# Remove locks older than 24 hours
find project/.locks/ -name "*.lock" -mmin +1440 -delete
```

### History files missing

**Cause:** First session or files were deleted.
**Fix:** They're auto-created by the startup protocol, or manually:
```bash
mkdir -p project
echo "# Project History" > project/PROJECT_HISTORY.md
echo '{"project": "multi-agent-squad", "entries": []}' > project/project_history.json
```

### Too many permission prompts from teammates

**Fix:** Pre-approve common operations in `.claude/settings.local.json`:
```json
{
  "permissions": {
    "allow": [
      "Bash(terraform:*)",
      "Bash(kubectl:*)",
      "Bash(aws:*)"
    ]
  }
}
```

### Orphaned tmux sessions

```bash
# List all tmux sessions
tmux ls

# Kill orphaned session
tmux kill-session -t <session-name>
```

---

## 11. Advanced Patterns

### Pattern 1: Competing Implementations

Spawn N agents implementing the same thing independently, pick the best:

```bash
# Create separate worktrees for each approach
/manage-worktrees create vpc-approach-a
/manage-worktrees create vpc-approach-b
/manage-worktrees create vpc-approach-c

# Assign different agents to each worktree
# Compare results, pick the best
```

### Pattern 2: Oracle-Based Testing

For large infrastructure changes, use a reference implementation:

1. Deploy known-good configuration (GCC equivalent)
2. Apply changes to a subset of resources
3. If failures, bisect to find which change caused it
4. Repeat until root cause is identified

### Pattern 3: Self-Organizing Swarm

Instead of explicit task assignment, let agents self-organize:

```
"Create a team of 5 agents. Create 20 terraform modules as tasks.
Let agents claim and complete tasks on their own.
No explicit assignment — whoever finishes first picks up the next one."
```

This creates natural load-balancing: fast agents do more work.

### Pattern 4: Progressive Enhancement

Start simple, add complexity through reviews:

```
Phase 1: Basic implementation (Terraform Engineer alone)
Phase 2: Security hardens it (Security Reviewer)
Phase 3: Cost optimizes it (Cost Analyst)
Phase 4: Best practices polish (Best Practices Validator)
```

Each phase improves the previous one, like code review rounds.

### Pattern 5: Cross-Project Coordination

Use worktrees to coordinate changes across multiple projects:

```bash
/manage-worktrees create-feature vpc-redesign platform-design snips opsfleet

# Each repo gets a worktree
# Agents work in parallel across repos
# PRs created for each repo
# Synchronized merge when all pass
```

### Pattern 6: Resume from Any Point

The history system allows resuming at any stage:

```bash
# Check where we stopped
/query-history --tag hft-system --limit 5

# Last entry says: "Design approved, implementation started"
# Continue from implementation phase
/design-system "Continue HFT system — skip design, start implementation" --project hft-system
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                 MULTI-AGENT SQUAD                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  NEW SYSTEM:    /design-system "what you want"           │
│  INFRA TASK:    /infra-team "specific task"              │
│  DEBUG:         /investigate "what's broken"             │
│                                                          │
│  CHECK STATUS:  /project-status                          │
│  SEE HISTORY:   /query-history --limit 20                │
│  CONTINUE:      /query-history --tag project-name        │
│                                                          │
│  BEFORE APPLY:  /blast-radius path/to/terraform          │
│                 /cost-estimate path/to/terraform          │
│  AFTER APPLY:   /validate-deployment app-name            │
│  PROMOTE:       /promote-environment dev staging         │
│                                                          │
│  TEAM CONTROLS:                                          │
│    Shift+Tab    Toggle delegate mode                     │
│    Shift+Up/Down  Select teammate (in-process)           │
│    Ctrl+T       Toggle task list                         │
│    Click pane   Interact with teammate (tmux)            │
│                                                          │
│  HUMAN CHECKPOINTS (you must approve):                   │
│    ⚠️ Design approval                                     │
│    ⚠️ Implementation plan approval                        │
│    ⚠️ terraform apply                                     │
│    ⚠️ Production promotion                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```
