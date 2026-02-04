---
name: log-activity
description: Log an agent activity to project history (both markdown and JSON formats)
args: "<agent> <action-type> <description> [--files <files>] [--tags <tags>]"
---

# Log Activity Skill

This skill logs agent activities to project history in both human-readable (markdown) and machine-parseable (JSON) formats.

## Arguments
- `agent`: The agent name (e.g., solution-architect, devops-engineer)
- `action-type`: Type of action (design_decision, implementation, review, validation, escalation, resolution, documentation, configuration, deployment)
- `description`: Brief description of the action
- `--files`: Comma-separated list of files created/modified
- `--tags`: Comma-separated tags for categorization

## Workflow

### Step 1: Ensure History Files Exist

Check if project history files exist, create if needed:

```bash
# Check for project directory
if [ ! -d "project" ]; then
  mkdir -p project
fi

# Check for history files
if [ ! -f "project/PROJECT_HISTORY.md" ]; then
  # Create initial markdown history
  cat > project/PROJECT_HISTORY.md << 'EOF'
# Project Activity History

This file tracks all agent activities, decisions, and changes throughout the project lifecycle.

## How to Read This Log
- Entries are in reverse chronological order (newest first)
- Each entry includes: timestamp, agent, action, details, and outcome
- Use tags to filter related entries
- Reference entry IDs for linking related activities

---

EOF
fi

if [ ! -f "project/project_history.json" ]; then
  # Create initial JSON history
  cat > project/project_history.json << 'EOF'
{
  "version": "1.0",
  "project": "",
  "created_at": "",
  "updated_at": "",
  "entries": []
}
EOF
fi
```

### Step 2: Generate Entry ID and Timestamp

```bash
# Generate UUID-like ID
ENTRY_ID=$(date +%s)-$(echo $RANDOM | md5sum | head -c 8)

# ISO timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
HUMAN_TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
```

### Step 3: Gather Activity Details

Prompt for or extract:
1. **Action details**: What was done and why
2. **Context**: What triggered this action
3. **Files changed**: Created, modified, deleted files
4. **Outcome**: Result of the action
5. **Follow-up**: Any next steps needed
6. **Tags**: Categorization tags

### Step 4: Write Markdown Entry

Prepend to PROJECT_HISTORY.md (after header):

```markdown
---
## [$HUMAN_TIMESTAMP] $AGENT: $DESCRIPTION

**ID**: $ENTRY_ID
**Action**: $ACTION_TYPE
**Category**: $CATEGORY

### Context
$CONTEXT_DESCRIPTION

### What Was Done
$ACTION_DETAILS

### Reasoning
$REASONING (if applicable)

### Files Changed
- Created: $CREATED_FILES
- Modified: $MODIFIED_FILES
- Deleted: $DELETED_FILES

### Outcome
$OUTCOME_STATUS - $OUTCOME_DESCRIPTION

### Follow-up Actions
$FOLLOWUP_ACTIONS (if any)

**Tags**: $TAGS

---
```

### Step 5: Append JSON Entry

Add to project_history.json entries array:

```json
{
  "id": "$ENTRY_ID",
  "timestamp": "$TIMESTAMP",
  "agent": {
    "name": "$AGENT",
    "type": "$AGENT_TYPE"
  },
  "action": {
    "type": "$ACTION_TYPE",
    "description": "$DESCRIPTION",
    "category": "$CATEGORY"
  },
  "context": {
    "task": "$TASK",
    "triggered_by": "$TRIGGERED_BY",
    "related_entries": []
  },
  "details": {
    "what_was_done": "$ACTION_DETAILS",
    "reasoning": "$REASONING"
  },
  "files": {
    "created": [$CREATED_FILES],
    "modified": [$MODIFIED_FILES],
    "deleted": [$DELETED_FILES]
  },
  "outcome": {
    "status": "$STATUS",
    "result": "$RESULT",
    "follow_up_actions": [$FOLLOWUP]
  },
  "tags": [$TAGS]
}
```

### Step 6: Update JSON Metadata

```bash
# Update the updated_at timestamp in JSON
jq '.updated_at = "'$TIMESTAMP'"' project/project_history.json > tmp.json && mv tmp.json project/project_history.json
```

### Step 7: Confirm Logging

Output confirmation:
```
✅ Activity logged successfully

Entry ID: $ENTRY_ID
Agent: $AGENT
Action: $ACTION_TYPE
Time: $HUMAN_TIMESTAMP

Files updated:
- project/PROJECT_HISTORY.md
- project/project_history.json
```

## Quick Log Examples

### Design Decision
```
/log-activity solution-architect design_decision "Selected PostgreSQL for user data" --files "docs/adr/001-db.md" --tags "database,architecture"
```

### Implementation
```
/log-activity backend-engineer implementation "Created user authentication service" --files "src/auth/service.ts,src/auth/types.ts" --tags "auth,feature"
```

### Escalation
```
/log-activity qa-engineer escalation "Deployment validation failed - pods crashlooping" --tags "deployment,issue,escalation"
```

### Resolution
```
/log-activity devops-engineer resolution "Fixed memory limits causing OOM kills" --files "k8s/deployment.yaml" --tags "deployment,bugfix"
```

## Integration Notes

This skill should be called by agents after completing significant actions. The Prime Orchestrator may also call this to log orchestration decisions.

For automatic logging, see the PostToolUse hooks in settings.json that can trigger logging for certain actions.
