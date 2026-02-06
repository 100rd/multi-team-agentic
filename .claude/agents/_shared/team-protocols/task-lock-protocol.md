# Task Lock Protocol

Prevents duplicate work when multiple agents operate in parallel, whether in agent team mode or subagent mode.

## Lock Directory

```
project/.locks/
├── {task-id}.lock          # Active task locks
├── {task-id}.done          # Completed task markers
└── {task-id}.failed        # Failed task markers
```

## Lock File Format

```json
{
  "task_id": "design-vpc-module",
  "agent": "terraform-engineer",
  "claimed_at": "2026-02-06T10:30:00Z",
  "expires_at": "2026-02-06T11:30:00Z",
  "description": "Design and implement VPC Terraform module"
}
```

## Protocol

### Claiming a Task

```bash
TASK_ID="design-vpc-module"
AGENT_NAME="terraform-engineer"
LOCK_FILE="project/.locks/${TASK_ID}.lock"

# Check if already claimed or done
if [ -f "$LOCK_FILE" ]; then
  echo "LOCK_EXISTS: task=$TASK_ID $(cat $LOCK_FILE | python3 -c 'import sys,json; d=json.load(sys.stdin); print(f\"agent={d[\"agent\"]} claimed={d[\"claimed_at\"]}\")')"
  # Check if expired (1 hour timeout)
  CLAIMED=$(cat "$LOCK_FILE" | python3 -c 'import sys,json; print(json.load(sys.stdin)["claimed_at"])')
  if python3 -c "from datetime import datetime, timezone; c=datetime.fromisoformat('$CLAIMED'.replace('Z','+00:00')); print('EXPIRED' if (datetime.now(timezone.utc)-c).seconds > 3600 else 'ACTIVE')"; then
    echo "Lock expired, reclaiming..."
  else
    echo "Task already claimed by another agent. Pick a different task."
    exit 1
  fi
fi

if [ -f "project/.locks/${TASK_ID}.done" ]; then
  echo "TASK_ALREADY_DONE: task=$TASK_ID"
  exit 0
fi

# Claim the task
cat > "$LOCK_FILE" << EOF
{
  "task_id": "$TASK_ID",
  "agent": "$AGENT_NAME",
  "claimed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "expires_at": "$(date -u -v+1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '+1 hour' +%Y-%m-%dT%H:%M:%SZ)",
  "description": "Task description here"
}
EOF

echo "LOCK_ACQUIRED: task=$TASK_ID agent=$AGENT_NAME"
```

### Completing a Task

```bash
TASK_ID="design-vpc-module"

# Move lock to done
mv "project/.locks/${TASK_ID}.lock" "project/.locks/${TASK_ID}.done"

# Update done file with completion info
python3 -c "
import json, sys
from datetime import datetime, timezone
with open('project/.locks/${TASK_ID}.done') as f:
    d = json.load(f)
d['completed_at'] = datetime.now(timezone.utc).isoformat()
d['status'] = 'completed'
with open('project/.locks/${TASK_ID}.done', 'w') as f:
    json.dump(d, f, indent=2)
"

echo "TASK_COMPLETE: task=$TASK_ID"
```

### Failing a Task

```bash
TASK_ID="design-vpc-module"
REASON="terraform validate failed with 3 errors"

# Move lock to failed
mv "project/.locks/${TASK_ID}.lock" "project/.locks/${TASK_ID}.failed"

# Update with failure info
python3 -c "
import json
from datetime import datetime, timezone
with open('project/.locks/${TASK_ID}.failed') as f:
    d = json.load(f)
d['failed_at'] = datetime.now(timezone.utc).isoformat()
d['status'] = 'failed'
d['reason'] = '$REASON'
with open('project/.locks/${TASK_ID}.failed', 'w') as f:
    json.dump(d, f, indent=2)
"

echo "TASK_FAILED: task=$TASK_ID reason=$REASON"
```

### Querying Task Status

```bash
# List all active locks
echo "=== Active Tasks ==="
for f in project/.locks/*.lock 2>/dev/null; do
  [ -f "$f" ] && python3 -c "import json; d=json.load(open('$f')); print(f\"  {d['task_id']}: {d['agent']} (since {d['claimed_at']})\")"
done

# List completed tasks
echo "=== Completed Tasks ==="
for f in project/.locks/*.done 2>/dev/null; do
  [ -f "$f" ] && python3 -c "import json; d=json.load(open('$f')); print(f\"  {d['task_id']}: {d['agent']} (completed {d.get('completed_at','unknown')})\")"
done

# List failed tasks
echo "=== Failed Tasks ==="
for f in project/.locks/*.failed 2>/dev/null; do
  [ -f "$f" ] && python3 -c "import json; d=json.load(open('$f')); print(f\"  {d['task_id']}: {d['agent']} - {d.get('reason','unknown')}\")"
done
```

## Heartbeat Extension

For long-running tasks (e.g., terraform apply), extend the lock:

```bash
# Extend lock by 1 hour
python3 -c "
import json
from datetime import datetime, timezone, timedelta
with open('project/.locks/${TASK_ID}.lock') as f:
    d = json.load(f)
d['expires_at'] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
d['heartbeat'] = datetime.now(timezone.utc).isoformat()
with open('project/.locks/${TASK_ID}.lock', 'w') as f:
    json.dump(d, f, indent=2)
"
```

## Cleanup

After a session completes, clean up locks:

```bash
# Remove all locks older than 24 hours
find project/.locks/ -name "*.lock" -mmin +1440 -delete

# Archive completed tasks
mkdir -p project/.locks/archive
mv project/.locks/*.done project/.locks/archive/ 2>/dev/null
mv project/.locks/*.failed project/.locks/archive/ 2>/dev/null
```

## Integration with Agent Teams

When using native agent teams (TeammateTool), the shared task list handles coordination. This lock protocol is a **fallback** for:
- Subagent mode (no shared task list)
- Cross-session coordination
- Manual parallel sessions via git worktrees
- Hybrid mode (some agents in team, some as subagents)
