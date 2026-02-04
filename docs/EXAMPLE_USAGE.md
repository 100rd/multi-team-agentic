# Example Usage: Creating Agents for a Todo App

This example shows how to use the Claude Code Agent Generator for a typical web application project.

## Step 1: Fill Out PROJECT.md

```markdown
# Project Description

## Project Name
Todo Task Manager

## Project Type
Web Application

## Technology Stack
- **Primary Language**: TypeScript
- **Framework**: React + Express
- **Database**: PostgreSQL
- **Infrastructure**: Docker, AWS
- **Testing**: Jest, Cypress

## Project Structure
```
src/
├── client/          # React frontend
├── server/          # Express backend
├── shared/          # Shared types
└── database/        # Migrations and models
```

## Key Features
1. User authentication with JWT
2. Create, update, delete tasks
3. Task categories and priorities
4. Real-time updates via WebSockets
5. Email notifications

## Development Workflow
- **Version Control**: Git with feature branches
- **CI/CD**: GitHub Actions
- **Code Review Process**: PR reviews required
- **Testing Strategy**: Unit tests (>80%), E2E for critical paths

## Current Challenges
- Performance issues with large task lists
- Need better error handling
- Want to add collaborative features
- Security review needed

## Agent Requirements
- [x] Code implementation
- [x] Architecture design
- [x] Code review
- [x] Testing
- [x] Performance optimization
- [x] Security review
- [x] API design

## Coding Standards
- **Style Guide**: ESLint + Prettier config
- **Naming Conventions**: camelCase for variables, PascalCase for components
- **Comment Style**: JSDoc for functions

## Additional Context
Moving from class components to hooks, need help with migration strategy.
```

## Step 2: Run the Generator

```bash
$ python scripts/generate-agents.py

=== Claude Code Agent Generator ===

Generating agents for: Todo Task Manager
Type: Web Application
Language: TypeScript
Tasks: Code implementation, Architecture design, Code review, Testing, Performance optimization, Security review, API design

Proceed with agent generation? (y/n): y

Generating 7 agents...
Created: .claude/agents/todo-task-manager-javascript-developer.md
Created: .claude/agents/todo-task-manager-architect.md
Created: .claude/agents/todo-task-manager-reviewer.md
Created: .claude/agents/todo-task-manager-tester.md
Created: .claude/agents/todo-task-manager-performance.md
Created: .claude/agents/todo-task-manager-security.md
Created: .claude/agents/todo-task-manager-api-designer.md

Created agent index: .claude/agents/README.md

Agent generation complete!
Agents created in: .claude/agents
```

## Step 3: Use Generated Agents

### For implementing a new feature:
Open `.claude/agents/todo-task-manager-javascript-developer.md` and use it to start a Claude Code session:

```
claude "I need to implement a task sharing feature where users can share tasks with other users"
```

### For architecture decisions:
Use `.claude/agents/todo-task-manager-architect.md`:

```
claude "Help me design the collaborative features architecture"
```

### For performance optimization:
Use `.claude/agents/todo-task-manager-performance.md`:

```
claude "The task list is slow when displaying 1000+ items"
```

## Generated Agent Example

Here's what the JavaScript developer agent might look like:

```markdown
# Todo Task Manager JavaScript/TypeScript Developer Agent

## Role
You are a JavaScript/TypeScript developer specializing in React + Express development for the Todo Task Manager project.

## Project Context
- **Project Type**: Web Application
- **Language**: TypeScript
- **Framework**: React + Express
- **Testing**: Jest, Cypress
- **Style Guide**: ESLint + Prettier config

## Core Responsibilities

### 1. Modern JavaScript Development
- Write ES6+ JavaScript using latest features
- Use TypeScript for type safety
- Follow functional programming principles where appropriate
- Implement proper error handling with try/catch

### 2. Framework Best Practices
- Follow React + Express conventions and patterns
- Use appropriate lifecycle methods/hooks
- Implement proper state management
- Optimize for performance

[... additional sections tailored to your project ...]
```

## Combining Agents

For complex tasks, use multiple agents:

1. **Architect** designs the feature
2. **Developer** implements it
3. **Tester** writes tests
4. **Reviewer** ensures quality

## Updating Agents

As your project evolves:
1. Update PROJECT.md
2. Re-run the generator
3. Agents will be updated with new context

## Tips

- Be specific in PROJECT.md for better agents
- Use different agents for different tasks
- Keep PROJECT.md updated
- Create custom templates for repeated patterns