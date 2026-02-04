# PRD (Product Requirements Document) Creation Workflow

This workflow guides the creation of comprehensive Product Requirements Documents and breaks them down into actionable tasks.

## When This Workflow Starts
- User selects "Create Product Requirements Document" 
- User wants to define a new feature
- Beginning of any development work

## Workflow Steps

### Step 1: PRD Type Selection
**"What type of requirements are we documenting?"**

1️⃣ **Complete Product PRD** - Full product specification
2️⃣ **Feature PRD** - Single feature or epic  
3️⃣ **Technical Specification** - Implementation details
4️⃣ **User Story Collection** - Multiple small stories

Press 1, 2, 3, or 4:

### Step 2: Delegate to Product Manager
```
Use Task tool:
"You are the Product Manager agent. Create a PRD for [what user described].
 
Include:
1. Problem Statement
2. Goals & Success Metrics
3. User Personas
4. User Stories / Requirements
5. Acceptance Criteria
6. Dependencies
7. Timeline Estimate

Save to: project/docs/requirements/PRD-[feature-name].md"
```

### Step 3: Review PRD with User
**Show the generated PRD and ask:**

"Here's the PRD I've created. Would you like to:"

a) Approve and continue to task breakdown
b) Make modifications
c) Add more details
d) Start over

Press a, b, c, or d:

### Step 4: Task Breakdown
Once PRD is approved:

**"Let's break this down into development tasks."**

Delegate to Product Manager + relevant engineers:
```
"Based on this PRD, create a task list with:
1. Task title and description
2. Estimated effort (S/M/L/XL)
3. Dependencies
4. Assignee (which agent)
5. Acceptance criteria

Group by:
- Backend tasks
- Frontend tasks  
- Infrastructure tasks
- Testing tasks"
```

### Step 5: Create Task Tracking

Based on user's preferred tracking system:

#### For GitHub Issues:
```bash
# Use github-integration.py to create issues
python scripts/github-integration.py create-from-prd project/docs/requirements/PRD-[name].md
```

#### For Markdown tracking:
Create `project/docs/tasks/SPRINT-[number]-TASKS.md`:
```markdown
# Sprint Tasks from PRD: [Feature Name]

## Backend Tasks
- [ ] Task 1: [Description] (Size: M) @backend-engineer
- [ ] Task 2: [Description] (Size: S) @backend-engineer

## Frontend Tasks  
- [ ] Task 3: [Description] (Size: L) @frontend-engineer

## Testing Tasks
- [ ] Task 4: [Description] (Size: M) @qa-engineer
```

### Step 6: Assign Initial Tasks
**"I'll assign the first tasks to get started:"**

Use Task tool to delegate first tasks:
```
"Backend Engineer: Please start with [Task 1 details]"
"Frontend Engineer: Please start with [Task 3 details]"
```

Update PROJECT_STATUS.md:
```markdown
## Active Development
- Feature: [Feature Name]
- PRD: project/docs/requirements/PRD-[name].md
- Total Tasks: [X]
- In Progress: [Y]
- Completed: [Z]
```

### Step 7: Set Up Progress Tracking
Create monitoring hooks if requested:

```toml
# In .claude/hooks/project-[name]-progress.toml
[[hooks]]
event = "Notification"
[hooks.matcher]
time = "every 2 hours"
command = '''
echo "📊 Progress Check for [Feature Name]"
cat project/docs/tasks/SPRINT-*-TASKS.md | grep -c "\\[x\\]"
'''
```

### Step 8: Next Actions
**"PRD and tasks are ready! What's next?"**

1️⃣ **Start development** → Go to `feature-development.md`
2️⃣ **Review architecture** → Have architect review PRD
3️⃣ **Set up environment** → Ensure dev environment ready
4️⃣ **Create another PRD** → Repeat this workflow
5️⃣ **View task board** → Show current tasks

## Success Criteria
- ✅ PRD document created and approved
- ✅ Tasks broken down with estimates
- ✅ Tasks tracked in preferred system
- ✅ Initial tasks assigned to agents
- ✅ Progress tracking set up

## Artifacts Created
- `project/docs/requirements/PRD-[name].md`
- `project/docs/tasks/SPRINT-[X]-TASKS.md` (if using markdown)
- GitHub issues (if using GitHub)
- Progress tracking hooks (if requested)