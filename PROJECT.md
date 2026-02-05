# Project Configuration

## Active Projects

<!-- Add your projects here using the template below -->

<!--
### 1. Project Name
**Name**: Project Name
**Type**: Web Application / API / Infrastructure / etc.
**Status**: Planning / Active Development / Maintenance
**Created**: YYYY-MM-DD
**Location**: `project/project-name/`

**Description**: Brief description of the project.

**Tech Stack**:
- Backend: ...
- Frontend: ...
- Database: ...
-->

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
