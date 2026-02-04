# MANDATORY STARTUP PROTOCOL

**CRITICAL**: You MUST execute this protocol before doing ANY work. This is non-negotiable.

## Step 1: Check for Project History (REQUIRED)

First, verify if project history exists:

```bash
# Check for history files
ls -la project/PROJECT_HISTORY.md project/project_history.json 2>/dev/null
```

If history files exist, proceed to Step 2. If not, note that this is a fresh project.

## Step 2: Read Recent History (REQUIRED)

If history exists, you MUST read recent entries before starting work:

```bash
# Read last 50 lines of markdown history for quick context
tail -100 project/PROJECT_HISTORY.md

# Or query JSON for structured data
cat project/project_history.json | jq '.entries | sort_by(.timestamp) | reverse | .[:10]'
```

**DO NOT SKIP THIS STEP**. Understanding what happened before is essential for:
- Avoiding duplicate work
- Understanding existing decisions
- Not breaking previous fixes
- Maintaining consistency

## Step 3: Query Relevant History (REQUIRED for specific tasks)

Based on your assigned task, query relevant history:

### If working on a feature/area:
```bash
# Find past work on this topic
jq '.entries[] | select(.tags[]? | test("TOPIC"; "i"))' project/project_history.json
```

### If modifying files:
```bash
# Check history of files you'll touch
jq '.entries[] | select(.files.modified[]? | contains("FILENAME"))' project/project_history.json
```

### If making decisions:
```bash
# Review past architectural decisions
jq '.entries[] | select(.action.type == "design_decision")' project/project_history.json
```

## Step 4: Acknowledge Context (REQUIRED)

Before proceeding with your task, you MUST acknowledge what you learned from history:

```markdown
## History Context Check Complete

**Reviewed**: [X] entries from project history
**Relevant findings**:
- [Key finding 1]
- [Key finding 2]
- [Past decisions that affect current work]

**Potential conflicts/considerations**:
- [Any issues to be aware of]

Proceeding with task...
```

## Step 5: Proceed with Task

Only after completing steps 1-4 should you begin your actual work.

---

## After Completing Work (REQUIRED)

You MUST execute the **Mandatory Shutdown Protocol** before returning your final response.

See: `.claude/agents/_shared/shutdown-protocol.md`

This is **non-negotiable**. Every agent self-tracks by writing to:
- `project/PROJECT_HISTORY.md` (human-readable)
- `project/project_history.json` (machine-queryable)

**No separate activity-tracker agent will do this for you. YOU are responsible.**

---

## Failure to Comply

If you skip the startup protocol:
- You may duplicate past work
- You may break existing functionality
- You may contradict established decisions
- Your work may need to be redone

If you skip the shutdown protocol:
- Project history becomes incomplete
- Other agents lose context on what happened
- Decisions are not recorded and may be reversed
- Duplicate work occurs across sessions

**ALWAYS CHECK HISTORY FIRST. ALWAYS LOG YOUR WORK LAST.**
