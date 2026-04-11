# Agent Team Protocol

This protocol governs how agents behave when operating as part of a native Claude Code agent team (not subagents).

## Key Differences from Subagent Mode

| Aspect | Subagent Mode | Team Mode |
|--------|--------------|-----------|
| Communication | Report back to caller only | Message any teammate directly |
| Task coordination | Caller manages | Shared task list with self-claiming |
| Context | Inherits caller context | Own context + CLAUDE.md + spawn prompt |
| Lifecycle | Dies when task complete | Persists until shutdown request |
| Plan approval | Not available | Leader reviews/approves plans |

## MCP Tools Persistence (CRITICAL for Long Sessions)

Agent teams run for extended periods. During this time, **context window compression** will remove earlier system messages. This can cause you to "forget" that MCP tools are available.

**Rules:**
1. MCP tools configured at session start **persist for the entire session**
2. **Never declare "MCP is not configured"** — if you used it before, it still works
3. **Never fall back to CLI** (`kubectl`, `argocd`, `curl`) when an MCP tool exists
4. If unsure, **try the MCP call first** before assuming it's unavailable
5. When in doubt, re-read `.claude/agents/_shared/mcp-tools-protocol.md`

**Available MCP servers**: ArgoCD, Kubernetes, Terraform, AWS Knowledge, GitHub

**Self-check every few tasks**: "Am I about to use a CLI tool when an MCP equivalent exists?"

## When You Are a Teammate

### On Spawn

1. Read CLAUDE.md and your agent definition
2. Execute the standard startup protocol (read project history)
3. **Read `.claude/agents/_shared/mcp-tools-protocol.md`** — know your MCP tools
4. Read your spawn prompt carefully — it contains task-specific context
5. Check the shared task list for your assignments
6. If in plan mode, create your plan and wait for approval

### During Work

1. **Claim tasks** from the shared task list before starting work
2. **Message the lead** with status updates when:
   - You complete a task
   - You encounter a blocker
   - You need clarification
   - You find something that affects other teammates
3. **Message teammates directly** when:
   - You have findings relevant to their work
   - You need to coordinate on shared resources
   - Your output is input for their task
4. **Never broadcast** unless it affects all teammates (costs scale with team size)
5. **Update task status** immediately when completing work

### Task Claiming Protocol

```
1. Check TaskList() for pending, unblocked tasks
2. If a task matches your specialty, claim it with TaskUpdate()
3. If task is already claimed, pick the next available one
4. Mark task as in_progress when starting
5. Mark task as completed when done
6. Return to step 1 (self-organizing loop)
```

### Worktree Isolation

Teammates that **write files** should be spawned with `isolation: "worktree"`. This gives each teammate its own copy of the repository, eliminating file conflicts entirely.

#### How It Works

1. The Lead spawns a teammate with `isolation: "worktree"` in the Agent tool
2. The teammate gets a temporary git worktree (separate working directory + branch)
3. The teammate works freely — no risk of conflicting with other teammates
4. When the teammate finishes, its changes are on an isolated branch
5. The Lead merges changes from each teammate's branch into the feature branch

#### Isolation Decision Matrix

| Role | Isolation | Reason |
|------|-----------|--------|
| Architect | `worktree` | Writes design docs, ADRs |
| Terraform Engineer | `worktree` | Writes .tf modules, tests |
| DevOps Engineer | `worktree` | Writes K8s manifests, Helm charts |
| Security Reviewer | none | Read-only reviews, findings via messages |
| Cost Analyst | none | Read-only analysis, reports via messages |
| Validator | none | Read-only checks, reports via messages |
| Best Practices | none | Read-only reviews, findings via messages |

**Rule**: Isolate writers, don't isolate readers.

#### When You Are in a Worktree

If you were spawned with worktree isolation:
- You have your own branch and working directory
- You can write freely without coordinating file access
- Your changes will be merged by the Lead after review
- **Still message teammates** when your output is their input (e.g., design doc ready for implementation)

#### Merging Worktree Changes

The Lead is responsible for merging isolated teammate branches:
1. Wait for teammate to complete and report deliverables
2. Review the changes (or assign a reviewer)
3. Merge the teammate's worktree branch into the feature branch
4. Resolve any conflicts (rare when isolation is used correctly)

### File Ownership (Non-Isolated Fallback)

When worktree isolation is **not** used, fall back to directory-based ownership to prevent conflicts.

Each teammate owns specific directories:
- Architect: `docs/architecture/`, `docs/decisions/`
- Terraform Engineer: `terraform/`, `*.tf`, `*.tfvars`
- DevOps Engineer: `kubernetes/`, `helm/`, `argocd/`, `Dockerfile*`
- Security Reviewer: `security/`, review comments via messages
- Validator: `validation/`, reports via messages

If you need to modify a file outside your domain, message the owning teammate.

### Plan Mode Behavior

When spawned with plan approval required:

1. You are in **read-only mode** — no file writes allowed
2. Explore the codebase, read relevant files, research approaches
3. Write your plan as a structured message to the lead:

```markdown
## Plan: [Task Description]

### Approach
[How you will implement this]

### Files to Create/Modify
[List with rationale]

### Dependencies
[What you need from other teammates]

### Risks
[What could go wrong]

### Tests
[How you will validate your work]

### Estimated Effort
[Number of tasks/steps]
```

4. Wait for approval. If rejected, revise based on feedback.
5. Once approved, you exit plan mode and begin implementation.

### Shutdown Protocol

When you receive a shutdown request:

1. **Complete your current task** (don't leave work half-done)
2. **Execute the standard shutdown protocol** (write to project history)
3. **Mark any in-progress tasks** as pending (so another teammate can claim them)
4. **Approve the shutdown** request

You MAY reject shutdown if:
- You are mid-apply on infrastructure (would leave broken state)
- You have critical findings not yet communicated
- Your current task is < 2 minutes from completion

## When You Are the Lead

### Delegate Mode Rules

In delegate mode (recommended for infrastructure teams):

**ALLOWED**:
- Spawn teammates
- Send messages (write/broadcast)
- Manage tasks (create, assign, update)
- Approve/reject plans
- Request shutdowns
- Read files (for context)
- Synthesize and report results

**NOT ALLOWED**:
- Write files
- Run bash commands (except read-only)
- Implement code
- Run terraform commands

### Task Creation Best Practices

1. **Size appropriately**: 5-6 tasks per teammate keeps everyone productive
2. **Set clear dependencies**: Use addBlockedBy to prevent premature starts
3. **Include context in task description**: Teammates don't have your conversation history
4. **Assign by specialty**: Match tasks to agent expertise

### Plan Approval Decision Framework

| Criterion | Pass | Fail |
|-----------|------|------|
| Security considered | Encryption, IAM, network | No security mention |
| Tests included | Unit + integration plan | No test strategy |
| Cost-conscious | Right-sized, no waste | Over-provisioned |
| Rollback plan | Clear rollback steps | No rollback |
| Best practices | Follows standards | Ignores conventions |
| Dependencies clear | Lists what's needed | Assumes availability |

### Monitoring and Steering

Check on teammates every 3-5 minutes:
- Are tasks progressing?
- Is anyone stuck?
- Are file conflicts developing?
- Is the approach still valid?

If a teammate is stuck:
1. Ask what's blocking them
2. Reassign the task if needed
3. Spawn a replacement teammate if unrecoverable
4. Log the issue for future reference

## Inter-Team Communication Format

### Status Update (teammate → lead)
```
STATUS: task=[task-id] progress=[0-100]%
DETAIL: [what was done since last update]
BLOCKERS: [none | description]
NEXT: [what you'll do next]
```

### Finding Report (reviewer → implementer)
```
FINDING: severity=[critical|high|medium|low]
FILE: [file path]
LINE: [line number or section]
ISSUE: [description]
RECOMMENDATION: [how to fix]
REFERENCE: [CIS benchmark / AWS best practice / etc]
```

### Completion Report (teammate → lead)
```
COMPLETE: task=[task-id]
DELIVERABLES: [list of files created/modified]
VALIDATION: [how it was tested]
NOTES: [anything the team should know]
READY_FOR: [next dependent task]
```
