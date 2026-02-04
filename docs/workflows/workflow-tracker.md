# Workflow Status Tracker

This document explains how to track and monitor workflow progress throughout the development lifecycle.

## Workflow States

Each workflow can be in one of these states:
- **Not Started** - Workflow hasn't begun
- **In Progress** - Currently executing steps
- **Blocked** - Waiting on something
- **Complete** - All steps finished
- **Paused** - Temporarily stopped

## PROJECT_STATUS.md Structure

The PROJECT_STATUS.md file tracks all workflow states:

```markdown
# Project Status

## Current Workflow: [Workflow Name]
- State: In Progress
- Current Step: Step 4 - Task Breakdown
- Started: [Date]
- Blocked: No

## Completed Workflows
1. ✅ Project Initialization (2024-01-15)
2. ✅ PRD Creation - User Auth (2024-01-16)

## Active Features
| Feature | PRD | Tasks | Progress | Status |
|---------|-----|-------|----------|--------|
| User Auth | ✅ | 12 | 8/12 (67%) | In Dev |
| Payment | ✅ | 0 | 0% | Planning |

## Task Tracking
### In Progress
- [ ] Backend: Implement JWT tokens (@backend-engineer)
- [ ] Frontend: Create login form (@frontend-engineer)

### Completed Today
- [x] Database: User schema created
- [x] API: Auth endpoints designed

### Blocked
- [ ] Payment: Waiting for Stripe API keys

## Next Steps
1. Complete JWT implementation
2. Begin frontend integration
3. Set up testing environment
```

## Automated Tracking Hooks

Create hooks to automatically update status:

```toml
# .claude/hooks/project-[name]-tracking.toml

# Track task completion
[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Edit"
file_paths = ["project/docs/tasks/*.md"]
command = '''
echo "📊 Updating task progress..."
# Count completed tasks and update PROJECT_STATUS.md
'''

# Daily status snapshot
[[hooks]]
event = "Notification"
[hooks.matcher]
time = "17:00"
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
command = '''
echo "📸 Daily Status Snapshot"
# Generate status summary
'''
```

## Workflow Transition Tracking

When moving between workflows:

### 1. Close Current Workflow
```markdown
## Completed Workflows
- ✅ [Workflow Name] - Completed [Date]
  - Duration: X days
  - Output: [What was produced]
```

### 2. Start New Workflow
```markdown
## Current Workflow: [New Workflow]
- State: In Progress
- Current Step: Step 1
- Started: [Date]
- Previous: [Previous Workflow]
```

## Progress Queries

Users can check progress with:

### Overall Status
```
/project-status
```

### Specific Workflow
```
/workflow-status --name "Feature Development"
```

### Task Progress
```
/task-status --feature "User Auth"
```

## Visual Progress Indicators

Use these in status updates:
- ⬜ Not started
- 🟦 In progress
- ✅ Complete
- ⚠️ Blocked
- ⏸️ Paused

### Progress Bars
```
Feature Progress: ████████░░ 80%
Sprint Progress:  ██████░░░░ 60%
```

## Workflow Dependencies

Track workflow dependencies:

```markdown
## Workflow Dependencies
- Feature Development → REQUIRES → PRD Creation ✅
- Deployment → REQUIRES → Testing Complete ⬜
- Sprint 2 → REQUIRES → Sprint 1 Complete 🟦
```

## Status Update Triggers

Update PROJECT_STATUS.md when:
1. Starting a new workflow
2. Completing a workflow step
3. Encountering a blocker
4. Completing tasks
5. Daily at end of work
6. Sprint boundaries

## Historical Tracking

Maintain history in:
```
project/docs/history/
├── sprint-1-summary.md
├── sprint-2-summary.md
└── feature-completions.md
```

## Metrics to Track

### Development Velocity
- Tasks completed per day
- Average task completion time
- Blocker frequency
- Workflow duration

### Quality Metrics
- Test coverage trend
- Bug discovery rate
- Review turnaround time
- Deployment frequency

## Workflow Modification Log

Track when workflows are customized:

```markdown
## Workflow Modifications
- [Date]: Modified Feature Development workflow
  - Added: Security review step
  - Reason: Compliance requirement
  - Modified by: User request
```