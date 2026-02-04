# Project Initialization Command

Initialize a new project with the Multi-Agent Squad orchestration system.

## Command Aliases
- `/project`
- `/create-project`
- `/project-init`
- "Start a new project"
- "Initialize project"

## Process Flow

### 1. Pre-Check
- Check if PROJECT.md exists
- If exists, read current project state
- If not, start interactive setup

### 2. Interactive Setup
Gather information through conversation:
- Project type and description
- Code organization (monorepo/multi-repo)
- Task tracking preferences
- Automation needs
- Integration requirements

### 3. Directory Creation
Create clear structure under `project/` folder:
```
project/
├── frontend/     # Frontend code
├── backend/      # Backend code
├── services/     # Microservices
└── docs/         # Project documentation
```

### 4. Agent Deployment
Create specialized agents in category folders:
- `.claude/agents/engineering/`
- `.claude/agents/product/`
- `.claude/agents/architecture/`
- `.claude/agents/quality/`
- `.claude/agents/specialized/`

### 5. Git Setup
- Initialize repositories
- Optionally connect to remote (GitHub/GitLab)
- Create initial commits

### 6. Project Summary
Show exactly what was created:
- File tree with ✨ for new files
- Agent count and types
- Configured integrations
- Automation level

### 7. Status Update
Create PROJECT_STATUS.md with:
- Initialization summary
- What was set up
- Next steps checklist

### 8. Next Actions Menu
Present numbered options:
1. Create requirements/epics
2. Design architecture
3. Set up environment
4. Start sprint planning
5. Configure CI/CD
6. Custom request

## Important Rules

1. **Clear Segregation**: Project files go in `project/`, system files stay in `.claude/`
2. **Show Results**: Display tree of created files
3. **Git Integration**: Ask about remote repositories
4. **Status Tracking**: Always update PROJECT_STATUS.md
5. **Next Steps**: Provide actionable options
6. **Agent Delegation**: Use specialized agents for tasks

## Error Handling

- If user cancels, clean up partial creation
- If integration fails, note it and continue
- Always show what succeeded vs failed

## Success Criteria

Project initialization is complete when:
- ✅ Project structure created
- ✅ Agents deployed to correct locations
- ✅ PROJECT.md generated
- ✅ Git repositories initialized
- ✅ PROJECT_STATUS.md created
- ✅ User presented with next actions