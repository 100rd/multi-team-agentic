# Sprint Management Workflow

This workflow handles all agile sprint ceremonies and tracking throughout the sprint lifecycle.

## Sprint Phases

### 1. Sprint Planning
**Trigger**: "start sprint planning", "plan sprint"

#### Steps:
1. **Review Backlog**
   ```
   Show all PRDs and unassigned tasks
   Prioritize based on business value
   ```

2. **Capacity Planning**
   **"What's our team capacity for this sprint?"**
   - Frontend: [X story points]
   - Backend: [Y story points]
   - QA: [Z story points]

3. **Sprint Goal Definition**
   **"What's the main goal for this sprint?"**
   
   Document in `project/docs/sprints/sprint-[N]-plan.md`

4. **Task Selection**
   Select tasks that fit capacity
   Assign to agents
   
5. **Create Sprint Board**
   ```markdown
   # Sprint [N] Board
   
   ## Todo
   - [ ] Task 1 (M) @backend
   - [ ] Task 2 (L) @frontend
   
   ## In Progress
   
   ## In Review
   
   ## Done
   ```

### 2. Daily Standups
**Trigger**: Daily at 9 AM (if automated) or "daily standup"

#### Format:
```
📅 DAILY STANDUP - Sprint [N] Day [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend Engineer:
✅ Yesterday: Completed user schema
🎯 Today: Working on JWT implementation
⚠️ Blockers: None

Frontend Engineer:
✅ Yesterday: Set up login component
🎯 Today: Integrating with API
⚠️ Blockers: Waiting for API endpoints

QA Engineer:
✅ Yesterday: Wrote test cases
🎯 Today: Setting up test environment
⚠️ Blockers: Need test data
```

Update PROJECT_STATUS.md with standup notes.

### 3. Sprint Progress Monitoring

#### Automated Tracking
```toml
# .claude/hooks/sprint-tracking.toml
[[hooks]]
event = "Notification"
[hooks.matcher]
time = "every 4 hours"
command = '''
echo "📊 Sprint Progress Check"
# Calculate completion percentage
# Alert if behind schedule
'''
```

#### Burndown Tracking
Track daily in `project/docs/sprints/sprint-[N]-burndown.md`:
```
Day 1: 40 points remaining
Day 2: 38 points remaining  
Day 3: 34 points remaining
...
```

### 4. Mid-Sprint Check-in
**Trigger**: Middle of sprint

**"How's the sprint progressing?"**

1. Review burndown chart
2. Identify risks
3. Adjust if needed
4. Update stakeholders

### 5. Sprint Review/Demo
**Trigger**: "sprint review", end of sprint

#### Preparation:
1. **Gather Completed Work**
   List all completed features
   Prepare demo scripts

2. **Create Demo Document**
   `project/docs/sprints/sprint-[N]-demo.md`
   - Features completed
   - Demo walkthrough
   - Metrics achieved

3. **Run Demo Session**
   **"Here's what we accomplished in Sprint [N]:"**
   - Show each feature
   - Demonstrate functionality
   - Gather feedback

### 6. Sprint Retrospective
**Trigger**: After sprint review

#### Format:
**"Let's reflect on Sprint [N]:"**

1. **What went well?**
   - List positive outcomes
   - Successful practices

2. **What could improve?**
   - Challenges faced
   - Process issues

3. **Action items**
   - Specific improvements
   - Owner and timeline

Document in `project/docs/sprints/sprint-[N]-retro.md`

## Sprint Artifacts

### Created During Sprint:
```
project/docs/sprints/
├── sprint-[N]-plan.md
├── sprint-[N]-board.md
├── sprint-[N]-burndown.md
├── sprint-[N]-standups.md
├── sprint-[N]-demo.md
└── sprint-[N]-retro.md
```

## Sprint Metrics

Track these metrics:
- **Velocity**: Story points completed
- **Commitment Accuracy**: Planned vs Actual
- **Cycle Time**: Average task completion
- **Defect Rate**: Bugs found
- **Team Happiness**: Retro feedback

## Sprint Status Commands

### Check Sprint Status
```
/sprint-status
```
Shows:
- Current sprint day
- Progress percentage  
- Blocked items
- Velocity tracking

### Update Sprint Board
```
/update-sprint-board --task [ID] --status [new-status]
```

## Sprint Cadence Options

**"What's your preferred sprint length?"**
- 1 week (rapid iteration)
- 2 weeks (recommended)
- 3 weeks (complex projects)
- 4 weeks (enterprise)

## Customizing Sprint Process

Users can modify by:
1. Adjusting ceremony frequency
2. Changing status categories
3. Adding custom metrics
4. Modifying templates

## Integration with Other Workflows

- **After Sprint Planning** → Feature Development
- **During Sprint** → Daily development work
- **After Sprint** → Deploy completed features
- **Next Sprint** → Back to planning

## Success Criteria
- ✅ Sprint goal achieved
- ✅ All committed tasks complete
- ✅ Demo delivered
- ✅ Retrospective conducted
- ✅ Next sprint ready