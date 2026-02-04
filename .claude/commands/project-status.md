---
name: project-status
description: View comprehensive status of all active features, worktrees, agents, and GitHub issues
---

# Project Status Command

Get a complete overview of your project's current state across all repositories and active features.

## What This Command Shows

1. **Active Features** - All features in development
2. **Worktree Status** - State of each worktree
3. **Agent Assignments** - Who's working on what
4. **GitHub Issues** - Linked issues and PRs
5. **Blockers** - What's holding up progress
6. **Recent Completions** - What was finished recently

## Usage

- `/project-status`
- "Show me the project status"
- "What's the current state?"
- "Status report"

## Status Report Format

```markdown
# Multi-Agent Squad Status Report
Generated: 2024-01-20 14:30 UTC

## 📊 Overview
- Active Features: 3
- Active Worktrees: 7
- Assigned Agents: 5
- Open PRs: 2
- Blocked Items: 1

## 🚀 Active Features

### Feature: user-authentication
**GitHub Issue**: #47 (In Progress)
**Priority**: High
**Started**: 2 days ago

**Worktrees**:
- ✅ backend/feature-user-authentication (90% complete)
  - 15 commits ahead
  - Last commit: "Add JWT token validation"
  - Assigned: Backend Developer Agent
  
- 🔄 frontend/feature-user-authentication (60% complete)
  - 8 commits ahead
  - Last commit: "Implement login form"
  - Assigned: Frontend Developer Agent
  
- 🔄 mobile/feature-user-authentication (40% complete)
  - 5 commits ahead
  - Last commit: "Add biometric auth"
  - Assigned: Mobile Developer Agent

**Next Steps**: Frontend needs to integrate with backend API

### Feature: payment-integration
**GitHub Issue**: #48 (In Progress)
**Priority**: High
**Started**: Today

**Worktrees**:
- 🔄 backend/feature-payment-integration (20% complete)
  - 3 commits ahead
  - Assigned: Backend Developer Agent
  
**Blockers**: ⚠️ Waiting for Stripe API credentials

## 🔍 Pull Requests

### Open PRs
1. **#152** - feat: Add user authentication (backend)
   - Status: In Review
   - Reviewers: @senior-engineer
   - Checks: ✅ All passing

2. **#153** - feat: Login UI components
   - Status: Draft
   - Reviewers: Not assigned yet
   - Checks: 🔄 Running

## ⚠️ Blockers & Issues

1. **Payment Integration** - Missing Stripe API credentials
   - Impact: Backend development blocked
   - Action: Contact DevOps for credentials
   - Assigned: @orchestrator

## ✅ Recently Completed

- **Feature: search-optimization** (Completed yesterday)
  - Merged PRs: #149, #150, #151
  - Issue #45 closed
  
- **Bug: memory-leak-fix** (Completed 2 days ago)
  - Merged PR: #148
  - Issue #44 closed

## 👥 Agent Activity

| Agent | Current Task | Status |
|-------|-------------|--------|
| Backend Developer | Payment API endpoints | Active |
| Frontend Developer | Auth UI polish | Active |
| Mobile Developer | Biometric integration | Active |
| QA Engineer | Testing auth flows | Scheduled |
| DevOps Engineer | Setting up Stripe | Requested |

## 📈 Velocity Metrics

- Features completed this week: 2
- Average feature cycle time: 4.5 days
- PR review time: 6 hours average
- Test coverage: 87% (+2% this week)
```

## Filtering Options

You can filter the status report:
- `/project-status --feature=auth` - Specific feature
- `/project-status --repo=backend` - Specific repository
- `/project-status --assigned=backend-dev` - By agent
- `/project-status --blocked` - Only blocked items

## Quick Actions

From the status report, you can:
1. **Unblock** - Address blockers immediately
2. **Reassign** - Move agents to critical tasks
3. **Escalate** - Flag delays to stakeholders
4. **Clean up** - Remove completed worktrees

## Status Indicators

- ✅ Complete
- 🔄 In Progress
- ⚠️ Blocked
- 🆕 New/Not Started
- 🔴 Critical/Overdue
- 🟡 At Risk
- 🟢 On Track

## Integration with GitHub

If GitHub integration is enabled:
- Real-time issue status
- PR review status
- Automated status updates
- Project board synchronization

## Export Options

- `/project-status --export=markdown` - Save to file
- `/project-status --export=json` - Machine readable
- `/project-status --email` - Send status email