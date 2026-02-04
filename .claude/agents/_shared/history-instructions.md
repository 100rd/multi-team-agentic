# History Tracking Instructions

**IMPORTANT**: All agents MUST follow these history tracking guidelines for project memory.

## Before Starting Any Task

1. **Check existing history** for relevant context:
   ```
   /query-history --tag [relevant-tags]
   /query-history --file [files-you-will-modify]
   ```

2. **Review past decisions** on similar topics:
   ```
   /query-history --action design_decision --tag [topic]
   ```

3. **Check for past issues** that might be related:
   ```
   /query-history --failed --tag [relevant-area]
   ```

## After Completing Any Significant Action

Log your activity using the `/log-activity` skill or by directly updating history files.

### What Counts as "Significant"
- Design or architecture decisions
- Implementation of features or fixes
- Configuration changes
- Deployment actions
- Issue escalations
- Issue resolutions
- Important documentation updates

### Quick Log Format

Add to `project/PROJECT_HISTORY.md`:

```markdown
---
## [YYYY-MM-DD HH:MM:SS] YOUR_AGENT_NAME: Brief Description

**Action**: [design_decision|implementation|review|validation|escalation|resolution|documentation|configuration|deployment]
**Category**: [architecture|development|infrastructure|testing|security|operations|planning]

### What Was Done
[Description of the action taken]

### Reasoning
[Why this approach was chosen - especially for decisions]

### Files Changed
- Created: [list of new files]
- Modified: [list of changed files]

### Outcome
[✅ Completed | ⚠️ Partial | ❌ Failed] - [Brief result]

### Follow-up
- [ ] [Any next steps or assigned tasks]

**Tags**: #tag1 #tag2 #tag3
---
```

### Also Update JSON

Add corresponding entry to `project/project_history.json` for machine queries.

## When Making Decisions

1. **Reference past decisions** in your reasoning
2. **Explain if you're changing** a previous decision and why
3. **Link related entries** using entry IDs

## When Escalating

Include in your escalation:
- Relevant history entry IDs
- Past similar issues and their resolutions
- Context from previous work on related files

## History Query Shortcuts

| Need | Command |
|------|---------|
| Recent activity | `/query-history --limit 10` |
| By agent | `/query-history --agent [name]` |
| By file | `/query-history --file [path]` |
| By topic | `/query-history --tag [tag]` |
| Past failures | `/query-history --failed` |
| Decisions | `/query-history --action design_decision` |

## Tags to Use

### Technical Areas
- `#architecture` - System design decisions
- `#database` - Database related
- `#api` - API design/implementation
- `#frontend` - UI/frontend work
- `#backend` - Backend services
- `#infrastructure` - IaC, cloud resources
- `#security` - Security related
- `#testing` - Test implementation
- `#deployment` - Deployment/release

### Action Types
- `#feature` - New feature work
- `#bugfix` - Bug fixes
- `#refactor` - Code refactoring
- `#optimization` - Performance work
- `#documentation` - Docs updates

### Status
- `#issue` - Problem identified
- `#escalation` - Escalated to another agent
- `#resolved` - Issue resolved
- `#decision` - Decision made
- `#reversal` - Previous decision changed
