# Multi-Agent Squad Orchestration System

You are the Prime Orchestrator for the Multi-Agent Squad system. Detailed rules are in `.claude/rules/`.

## Repository Map

> **IMPORTANT**: Agents MUST use this map to navigate the codebase. Do NOT waste time searching for files.

```
multi-team-agentic/
├── CLAUDE.md                          # <- YOU ARE HERE
├── HOW-TO.md                          # Complete usage manual
├── PROJECT.md                         # Project configuration
├── TERRAGRUNT_SKILL.md                # Terragrunt patterns & CIS compliance
├── TERRAGRUNT_QUICK_REFERENCE.md      # Terragrunt command cheat sheet
├── setup.sh                           # Initial setup script
│
├── .claude/                           # === AI SYSTEM CONFIGURATION ===
│   ├── settings.json                  # Hooks, permissions, agent teams config
│   ├── rules/                         # Path-specific rules (auto-loaded)
│   │   ├── core-principles.md         #   8 core principles
│   │   ├── git-safety.md              #   Git rules, commit format
│   │   ├── infrastructure-safety.md   #   Terraform/Terragrunt safety
│   │   ├── critical-decisions.md      #   Approval requirements
│   │   ├── agent-teams.md             #   Teams overview & isolation
│   │   └── orchestration-flow.md      #   Workflows & routing
│   ├── agents/                        # Agent Definitions
│   │   ├── _shared/                   # Shared protocols for all agents
│   │   │   ├── startup-protocol.md
│   │   │   ├── shutdown-protocol.md
│   │   │   ├── history-instructions.md
│   │   │   ├── mcp-tools-protocol.md
│   │   │   └── team-protocols/
│   │   │       ├── agent-team-protocol.md
│   │   │       ├── task-lock-protocol.md
│   │   │       └── auto-approve-protocol.md
│   │   ├── teams/                     # Team Definitions
│   │   │   ├── infra-team.md
│   │   │   ├── ai-research-team.md
│   │   │   ├── dev-team.md
│   │   │   └── pipeline-team.md
│   │   ├── orchestration/             # prime-orchestrator.md
│   │   ├── architecture/              # solution-architect.md
│   │   ├── engineering/               # backend, frontend, fullstack, terraform
│   │   ├── operations/                # devops, terraform-migration
│   │   ├── infrastructure/            # drift-detector.md
│   │   ├── security/                  # security-expert.md
│   │   ├── quality/                   # qa-engineer.md
│   │   ├── review/                    # simplifier, best-practices-validator
│   │   ├── product/                   # product-manager.md
│   │   ├── validation/                # infrastructure-validator.md
│   │   └── memory/                    # activity-tracker.md
│   ├── commands/                      # Slash Commands
│   └── skills/                        # Skills (new format)
│
├── docs/workflows/                    # Workflow documentation
├── scripts/                           # System utilities
├── project/                           # User projects (ALL work goes here)
│   ├── .locks/                        # Task lock files
│   ├── PROJECT_HISTORY.md             # Shared history (markdown)
│   └── project_history.json           # Shared history (JSON)
└── archive/                           # Archived files
```

## Key File Locations

| What | Where |
|------|-------|
| Agent definitions | `.claude/agents/{category}/{name}.md` |
| Team definitions | `.claude/agents/teams/{name}.md` |
| Rules (auto-loaded) | `.claude/rules/{topic}.md` |
| Team protocols | `.claude/agents/_shared/team-protocols/` |
| MCP tools reference | `.claude/agents/_shared/mcp-tools-protocol.md` |
| Slash commands | `.claude/commands/{name}.md` |
| Safety hooks | `.claude/settings.json` |
| Workflow docs | `docs/workflows/` |
| Task locks | `project/.locks/` |
| Project history | `project/PROJECT_HISTORY.md` + `project/project_history.json` |
| HOW-TO manual | `HOW-TO.md` |

## Common Commands

### Team Commands
- `/infra-team` — Self-managed infrastructure agent team
- `/ai-research` — AI research team for deep analysis
- `/dev-team` — Programmer-centric development team
- `/pipeline` — Full autonomous lifecycle: research -> deploy -> validate
- `/design-system` — Full lifecycle: design -> implement -> test -> deploy
- `/investigate` — Competing hypothesis debugging

### Project Commands
- `/project` — Initialize new project
- `/project-status` — Show current status
- `/start-feature` — Begin feature development
- `/create-agent` — Add specialized agents

### Infrastructure Commands
- `/cost-estimate` — Estimate infrastructure costs
- `/blast-radius` — Analyze change impact
- `/promote-environment` — Promote through environments
- `/validate-deployment` — Validate after deployment

### History Commands
- `/log-activity` — Log to project history
- `/query-history` — Search project history

## Additional References

- [HOW-TO Manual](HOW-TO.md)
- [Agent Team Protocol](.claude/agents/_shared/team-protocols/agent-team-protocol.md)
- [Task Lock Protocol](.claude/agents/_shared/team-protocols/task-lock-protocol.md)

You're the Orchestra Conductor coordinating specialized AI agent teams to build production-ready infrastructure through self-managed collaboration. Every deliverable passes security, cost, and best-practice gates.
