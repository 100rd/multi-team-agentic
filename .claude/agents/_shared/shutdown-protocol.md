# MANDATORY SHUTDOWN PROTOCOL (Self-Tracking)

**CRITICAL**: You MUST execute this protocol BEFORE returning your final response. This is non-negotiable. Every agent tracks its own work — there is no separate tracker agent.

## When to Execute

Execute this protocol when:
- Your task is complete (success or failure)
- You are about to return your final response
- You've been asked to stop or hand off

**DO NOT** skip this even if:
- The task was small
- You only did research/reading
- You encountered errors and couldn't finish

## Step 1: Ensure History Files Exist

```bash
# Create history files if they don't exist
mkdir -p project
if [ ! -f project/PROJECT_HISTORY.md ]; then
  echo "# Project History" > project/PROJECT_HISTORY.md
  echo "" >> project/PROJECT_HISTORY.md
  echo "Auto-generated activity log. Newest entries at the bottom." >> project/PROJECT_HISTORY.md
  echo "" >> project/PROJECT_HISTORY.md
fi
if [ ! -f project/project_history.json ]; then
  echo '{"project": "multi-agent-squad", "entries": []}' > project/project_history.json
fi
```

## Step 2: Write Markdown Entry

Append to `project/PROJECT_HISTORY.md`:

```markdown
---
## [YYYY-MM-DD HH:MM:SS] AGENT_NAME: Brief Description

**Action**: [design_decision|implementation|review|validation|escalation|resolution|documentation|configuration|deployment|research]
**Category**: [architecture|development|infrastructure|testing|security|operations|planning]

### What Was Done
[2-3 sentences describing what you actually did]

### Reasoning
[Why this approach — especially for decisions]

### Files Changed
- Created: [list new files, or "none"]
- Modified: [list changed files, or "none"]
- Deleted: [list removed files, or "none"]

### Outcome
[✅ Completed | ⚠️ Partial | ❌ Failed] - [Brief result]

### Follow-up
- [ ] [Any next steps needed, or "None"]

**Tags**: #tag1 #tag2
---
```

## Step 3: Write JSON Entry

Append entry to `project/project_history.json` entries array:

```json
{
  "id": "YYYYMMDD-HHMMSS-agent_name",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "agent": "your-agent-type",
  "action": {
    "type": "implementation|design_decision|review|validation|etc",
    "description": "Brief description of what was done"
  },
  "context": {
    "task": "What was asked",
    "category": "architecture|development|infrastructure|etc"
  },
  "files": {
    "created": [],
    "modified": [],
    "deleted": []
  },
  "outcome": {
    "status": "completed|partial|failed",
    "summary": "Brief result"
  },
  "follow_up": [],
  "tags": ["tag1", "tag2"]
}
```

**To append JSON safely:**
```bash
# Use jq to append entry (preferred)
jq '.entries += [NEW_ENTRY]' project/project_history.json > /tmp/ph.json && mv /tmp/ph.json project/project_history.json

# Or if jq is unavailable, use python
python3 -c "
import json
with open('project/project_history.json','r') as f: d=json.load(f)
d['entries'].append(NEW_ENTRY_DICT)
with open('project/project_history.json','w') as f: json.dump(d,f,indent=2)
"
```

## Step 4: Return Response

Only after writing both entries, return your final response to the caller.

---

## Quick Self-Track Template

For speed, copy-paste and fill in:

```bash
# Get timestamp
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S')
ENTRY_ID=$(date -u '+%Y%m%d-%H%M%S')-YOUR_AGENT

# Append markdown
cat >> project/PROJECT_HISTORY.md << 'ENTRY'

---
## [TIMESTAMP] AGENT: Description

**Action**: implementation
**Category**: development

### What Was Done
[Fill in]

### Files Changed
- Modified: [files]

### Outcome
✅ Completed - [result]

**Tags**: #relevant #tags
---
ENTRY
```

---

## Failure to Comply

If you skip the shutdown protocol:
- Project history becomes incomplete
- Other agents lose context on what happened
- Decisions are not recorded and may be reversed
- Duplicate work occurs across sessions

**ALWAYS LOG YOUR WORK BEFORE FINISHING.**
