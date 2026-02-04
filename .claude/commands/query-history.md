---
name: query-history
description: Query project history to find past actions, decisions, and context
args: "[--agent <name>] [--action <type>] [--file <path>] [--tag <tag>] [--since <date>] [--failed]"
---

# Query History Skill

This skill queries the project history to find relevant past actions, decisions, and context. Use this before starting work to understand what's been done and why.

## Arguments
- `--agent <name>`: Filter by agent name (e.g., solution-architect)
- `--action <type>`: Filter by action type (design_decision, implementation, escalation, etc.)
- `--file <path>`: Find all actions related to a specific file
- `--tag <tag>`: Filter by tag (e.g., database, security)
- `--since <date>`: Only entries after this date (YYYY-MM-DD)
- `--failed`: Only show failed/escalated entries
- `--limit <n>`: Limit number of results (default: 10)
- No args: Show recent activity summary

## Query Workflow

### Step 1: Verify History Files Exist

```bash
if [ ! -f "project/project_history.json" ]; then
  echo "⚠️ No project history found. Run /log-activity to start tracking."
  exit 1
fi
```

### Step 2: Execute Query

#### Query by Agent
```bash
jq '[.entries[] | select(.agent.name == "'"$AGENT"'")] | sort_by(.timestamp) | reverse | .[:'"$LIMIT"']' project/project_history.json
```

#### Query by Action Type
```bash
jq '[.entries[] | select(.action.type == "'"$ACTION_TYPE"'")] | sort_by(.timestamp) | reverse | .[:'"$LIMIT"']' project/project_history.json
```

#### Query by File
```bash
jq '[.entries[] | select(
  (.files.created[]? | contains("'"$FILE"'")) or
  (.files.modified[]? | contains("'"$FILE"'")) or
  (.files.deleted[]? | contains("'"$FILE"'"))
)] | sort_by(.timestamp) | reverse' project/project_history.json
```

#### Query by Tag
```bash
jq '[.entries[] | select(.tags[]? | contains("'"$TAG"'"))] | sort_by(.timestamp) | reverse | .[:'"$LIMIT"']' project/project_history.json
```

#### Query by Date Range
```bash
jq '[.entries[] | select(.timestamp >= "'"$SINCE"'")] | sort_by(.timestamp) | reverse | .[:'"$LIMIT"']' project/project_history.json
```

#### Query Failed/Escalated
```bash
jq '[.entries[] | select(.outcome.status == "failed" or .action.type == "escalation")] | sort_by(.timestamp) | reverse | .[:'"$LIMIT"']' project/project_history.json
```

#### Combined Query
```bash
jq '[.entries[] | select(
  (.agent.name == "'"$AGENT"'" or "'"$AGENT"'" == "") and
  (.action.type == "'"$ACTION_TYPE"'" or "'"$ACTION_TYPE"'" == "") and
  (.timestamp >= "'"$SINCE"'" or "'"$SINCE"'" == "")
)] | sort_by(.timestamp) | reverse | .[:'"$LIMIT"']' project/project_history.json
```

### Step 3: Format Results

Output in readable format:

```markdown
# History Query Results

**Query**: [query parameters]
**Found**: X entries

---

## [1] 2024-01-15 10:30:00 - solution-architect

**Action**: design_decision
**Description**: Selected PostgreSQL for user data

### Details
Relational data with complex queries, ACID compliance needed

### Files
- Modified: docs/adr/001-db.md

### Outcome
✅ Completed

### Tags
#database #architecture

---

## [2] 2024-01-14 15:45:00 - devops-engineer
...
```

## Common Queries

### "What decisions were made about X?"
```
/query-history --tag database
/query-history --tag authentication
/query-history --tag architecture
```

### "What has agent X done recently?"
```
/query-history --agent solution-architect --limit 5
/query-history --agent devops-engineer --since 2024-01-01
```

### "What happened to this file?"
```
/query-history --file src/auth/service.ts
/query-history --file terraform/main.tf
```

### "What issues have occurred?"
```
/query-history --failed
/query-history --action escalation
/query-history --tag issue
```

### "What was done last week?"
```
/query-history --since 2024-01-08 --limit 20
```

### "Show me all deployments"
```
/query-history --action deployment
/query-history --tag deployment
```

## Use Cases for Agents

### Before Starting New Work
```
# Check what's been done on this feature
/query-history --tag user-auth

# See if similar work was done before
/query-history --action implementation --tag api

# Check for related past issues
/query-history --failed --tag authentication
```

### When Making Decisions
```
# Review past architectural decisions
/query-history --action design_decision --agent solution-architect

# See why previous choices were made
/query-history --tag database --action design_decision
```

### When Debugging Issues
```
# What changed recently?
/query-history --since 2024-01-15 --action implementation

# What deployments happened?
/query-history --action deployment --since 2024-01-15

# Any related past issues?
/query-history --failed --tag payments
```

### Before Code Review
```
# Understand the context
/query-history --file src/payments/processor.ts

# See related decisions
/query-history --tag payments --action design_decision
```

## Integration with Agents

All agents should query history:

1. **At task start**: Understand context and past work
2. **Before decisions**: Check if similar decisions were made
3. **When escalating**: Include relevant history in escalation
4. **After completion**: Reference history in documentation

### Example Agent Usage

```markdown
## Agent Prompt Addition

Before starting this task:
1. Run `/query-history --tag [relevant-tag]` to understand past work
2. Run `/query-history --file [main-file]` to see file history
3. Check `/query-history --failed --tag [relevant-tag]` for past issues

Reference relevant history entries in your decisions.
```

## Output Formats

### Summary (default)
Brief list of entries with key info

### Detailed (--detailed)
Full entry content including all fields

### JSON (--json)
Raw JSON output for programmatic use

### IDs Only (--ids)
Just entry IDs for reference
