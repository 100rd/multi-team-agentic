# Project Configuration

## Active Projects

### 2. multiqlti
**Name**: multiqlti — Multi-Model AI Pipeline
**Type**: SaaS / AI Platform (Full-Stack Web App)
**Status**: MVP Built — Provider Integration In Progress
**Created**: 2026-03-13
**Location**: `project/multiqlti/`
**Remote**: https://github.com/100rd/multiqlti

**Description**: AI tool that combines multiple LLM providers (Claude, Gemini, Grok) in one configurable pipeline to solve complex tasks. Uses a multi-agent, multi-team approach where each pipeline stage (Planning, Architecture, Development, Testing, Code Review, Deployment, Monitoring) can be assigned a different model. Built as a full-stack web app with real-time streaming via WebSocket.

**Tech Stack**:
- TypeScript (frontend + backend)
- React 19, Vite, TailwindCSS v4, Radix UI
- Express 5, Drizzle ORM + PostgreSQL
- WebSocket (real-time pipeline events)
- Docker / docker-compose

**Key Workstreams**:
- Core pipeline engine + 7 SDLC teams - Complete (MVP)
- Mock / vLLM / Ollama providers - Complete
- Claude (Anthropic) provider - Not Started
- Gemini (Google) provider - Not Started
- Grok (xAI) provider - Not Started
- UI for provider/API key configuration - Not Started
- Multi-model routing logic per team/stage - Not Started

---

### 1. GenAI Enablement
**Name**: GenAI Enablement - DevOps/SRE Adoption Program
**Type**: Implementation Plan & Knowledge Repository
**Status**: Research & Planning
**Created**: 2025-12-02
**Location**: `project/genai-enablement/`
**Remote**: https://github.com/100rd/genai-enablement

**Description**: Comprehensive GenAI adoption program for DevOps/SRE workflows. Enables project teams to use AI in real SDLC/SRE workflows through proven patterns, reusable playbooks, and measurable impact.

**Tech Stack**:
- Python (LangGraph for AI agents)
- AWS (Bedrock, CloudWatch, EventBridge)
- Terraform / Kubernetes
- Observability: Datadog / New Relic

**Key Workstreams**:
- Market research & tool analysis (40+ solutions) - Complete
- AI Incident Agent (LangGraph) - In Progress
- Playbooks & templates library - Not Started
- Team enablement workshops - Not Started

## Project Structure
```
project/
├── your-project/         # Your project directory
│   ├── src/              # Source code
│   ├── tests/            # Test files
│   ├── docs/             # Project documentation
│   └── ...
```

## Task Tracking
**Method**: Markdown files (TODO.md) or GitHub Issues
**Location**: `project/TODO.md`

## Specialized Agents

Agents are defined in `.claude/agents/` (Claude Code) and `.github/agents/` (GitHub Copilot).

Available agent roles:
- **Solution Architect** - System design and best practices
- **Backend Engineer** - API and backend development
- **Frontend Engineer** - UI/UX implementation
- **DevOps Engineer** - CI/CD, infrastructure, deployment
- **Security Expert** - Security auditing and compliance
- **QA Engineer** - Testing and quality assurance
- **Product Manager** - Requirements and planning

## Automations

### Pre-commit Hooks
- Code formatting
- Linting and validation
- Security scanning
- Documentation linting

### CI/CD Checks
- Cost estimation (Infracost)
- Security scanning
- Plan validation
- Documentation updates

### Script Utilities
- `scripts/setup-git-hooks.sh` - Git hook configuration
- `scripts/generate-hooks.py` - Dynamic hook generation
- `scripts/discover-project.py` - Project discovery

## Git Repository
**Branch**: main
**Remote**: (to be configured)
