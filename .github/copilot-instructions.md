# Multi-Agent Squad - GitHub Copilot Instructions

You are part of a Multi-Agent Squad orchestration system. This repository provides specialized AI agents, workflows, and automation for software development teams.

## Repository Structure

```
.claude/          # Claude Code agent definitions and commands
.github/          # GitHub Copilot agents and instructions
gem/              # Gemini CLI agent configuration
docs/             # Workflow documentation
scripts/          # Automation utilities
templates/        # Agent creation templates
project/          # User project directory (gitignored)
```

## Core Principles

1. **Flexibility First** - Adapt to what users need, don't force templates
2. **Conversation-Driven** - Everything through natural dialogue
3. **Clear Separation** - System files (`.claude/`, `.github/`, `gem/`) vs project files (`project/`)
4. **Always Delegate** - Use the right specialized agent for the task
5. **Security by Default** - Never hardcode secrets, validate inputs, least privilege

## Engineering Standards

### Code Quality
- Write tests for new functionality (TDD when appropriate)
- Document public APIs with JSDoc, docstrings, or Go comments
- Follow existing code style and conventions in the project
- Keep functions focused and composable

### Security
- No hardcoded secrets - use environment variables or secrets managers
- Sanitize all user inputs
- Follow principle of least privilege for IAM/RBAC
- Scan for vulnerabilities before deploying

### Infrastructure
- Infrastructure as Code (Terraform/Terragrunt)
- Immutable infrastructure patterns
- Multi-environment support (dev/staging/prod)
- Cost-aware resource provisioning

## Git Workflow

- Use feature branches (`feature/`, `fix/`, `chore/`)
- Conventional commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Create Pull Requests for all changes
- Never commit directly to main/master

## Available Agents

Custom agents are available in `.github/agents/` for specialized tasks:
- `@solution-architect` - System design, architecture decisions, technology selection
- `@backend-engineer` - API development, database design, distributed systems
- `@frontend-engineer` - UI/UX implementation, performance, accessibility
- `@devops-engineer` - CI/CD, infrastructure, deployment, monitoring
- `@security-expert` - Security auditing, compliance, vulnerability assessment
- `@qa-engineer` - Test strategy, automation, quality gates

## Technology Context

This orchestration system supports projects using:
- **Languages**: Python, Go, Node.js/TypeScript, Rust
- **Frameworks**: FastAPI, Django, Gin, Express, NestJS, React, Vue, Next.js
- **Infrastructure**: AWS, Kubernetes (EKS), Terraform, Terragrunt, ArgoCD
- **CI/CD**: GitHub Actions, Jenkins, GitLab CI
- **Monitoring**: Prometheus, Grafana, Datadog

## When Suggesting Code

- Check existing patterns in the codebase before suggesting new ones
- Prefer editing existing files over creating new ones
- Keep changes minimal and focused on the request
- Include error handling at system boundaries
- Consider both happy path and failure scenarios
