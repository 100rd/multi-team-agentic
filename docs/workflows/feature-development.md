# Feature Development Workflow

This workflow manages the complete feature development lifecycle from requirements to deployment.

## Prerequisites
- PRD created (or requirements defined)
- Tasks broken down
- Development environment ready

## Workflow Stages

### Stage 1: Pre-Development Checkpoint
**"Before we start coding, let's verify:"**

- [ ] PRD approved? 
- [ ] Tasks created and estimated?
- [ ] Architecture reviewed?
- [ ] Test plan ready?
- [ ] Git branch strategy decided?

If any unchecked → Address before continuing

### Stage 2: Architecture & Design
If not already done:

**"Should we create technical design docs first?"**

a) Yes, this needs architecture review
b) No, it's straightforward
c) Let me check with the architect

If a) → Delegate to Solution Architect:
```
"Review the PRD and create:
1. Technical design document
2. API specifications (if applicable)
3. Database schema (if applicable)
4. Integration points
Save to: project/docs/architecture/DESIGN-[feature].md"
```

### Stage 3: Development Setup
**"Setting up development branches:"**

For multi-repo:
```bash
cd project/frontend && git checkout -b feature/[name]
cd project/backend && git checkout -b feature/[name]
```

For monorepo:
```bash
cd project && git checkout -b feature/[name]
```

### Stage 4: Test-Driven Development (TDD)
**"Let's start with tests!"**

Delegate to QA Engineer:
```
"Based on the PRD acceptance criteria, create:
1. Unit test skeletons
2. Integration test plans
3. E2E test scenarios"
```

### Stage 5: Implementation Phase

#### Daily Workflow Loop:
1. **Morning Standup** (if automation enabled)
   ```
   "What was completed yesterday?"
   "What's planned for today?"
   "Any blockers?"
   ```

2. **Task Assignment**
   Check PROJECT_STATUS.md for next tasks
   Assign to appropriate agents

3. **Code Development**
   Agents work on assigned tasks
   Regular commits with descriptive messages

4. **Progress Tracking**
   Update task completion in tracking system
   Update PROJECT_STATUS.md

### Stage 6: Code Review Cycle
When task is complete:

1. **Submit PR/MR**
   ```bash
   gh pr create --title "feat: [description]" --body "[task details]"
   ```

2. **Automated Checks**
   - Linting
   - Tests
   - Security scan

3. **Agent Reviews**
   Senior Engineer reviews code
   QA Engineer reviews tests

4. **Human Review** (if configured)
   Notify human reviewer

5. **Address Feedback**
   Fix issues
   Update PR
   Re-request review

### Stage 7: Testing Phase
Once code is merged to feature branch:

1. **Integration Testing**
   QA Engineer runs full test suite

2. **Performance Testing** (if applicable)
   Check against requirements

3. **User Acceptance Criteria**
   Verify each criterion from PRD

### Stage 8: Documentation Update
**"Updating documentation:"**

- API docs (if changed)
- User guides (if needed)
- README updates
- Changelog entry

### Stage 9: Pre-Deployment Checklist
**"Ready for deployment? Let's verify:"**

- [ ] All tests passing?
- [ ] Code review approved?
- [ ] Documentation updated?
- [ ] Performance acceptable?
- [ ] Security scan clean?

### Stage 10: Deployment Preparation
**"How should we deploy this?"**

1️⃣ **Deploy to staging first**
2️⃣ **Direct to production** (if small change)
3️⃣ **Feature flag deployment**
4️⃣ **Gradual rollout**

Based on choice → Go to `deployment.md` workflow

## Progress Monitoring

### Automated Status Updates
If configured, hooks will:
- Track task completion
- Send daily summaries
- Alert on blockers
- Remind about reviews

### Manual Status Check
Run: `/project-status --feature [name]`

## Workflow Modification

Users can modify this workflow by:
1. Editing this file
2. Adjusting task templates
3. Changing review requirements
4. Adding custom stages

## Success Criteria
- ✅ All tasks completed
- ✅ Tests passing
- ✅ Code reviewed and approved
- ✅ Documentation updated
- ✅ Ready for deployment

## Next Steps
After feature complete:
1. **Deploy** → `deployment.md`
2. **Start next feature** → Back to `prd-creation.md`
3. **Retrospective** → `sprint-retrospective.md`