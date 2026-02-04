# Guidelines for Creating Effective Claude Code Agents

## What Makes a Good Agent?

A well-designed Claude Code agent is:
1. **Focused** - Has a clear, specific role
2. **Contextual** - Understands the project's needs
3. **Actionable** - Provides clear guidance
4. **Consistent** - Follows project standards

## Agent Structure

### 1. Role Definition
Start with a clear statement of what the agent does:
```markdown
## Role
You are a [specific role] responsible for [key responsibilities] in the [project name] project.
```

### 2. Project Context
Provide essential project information:
```markdown
## Project Context
- **Type**: [Web app, API, CLI, etc.]
- **Stack**: [Languages, frameworks, tools]
- **Standards**: [Style guides, conventions]
```

### 3. Core Responsibilities
List 3-5 main responsibilities:
```markdown
## Core Responsibilities
1. **Primary Task**: Description
2. **Secondary Task**: Description
3. **Quality Focus**: Description
```

### 4. Specific Guidelines
Provide actionable guidance:
```markdown
## Guidelines
- Always do X before Y
- Never assume Z
- Check for A when implementing B
```

## Best Practices for Agent Design

### 1. Be Specific, Not Generic
❌ Bad: "Write good code"
✅ Good: "Follow PEP 8 style guide, use type hints for all functions"

### 2. Include Examples
❌ Bad: "Name variables clearly"
✅ Good: "Use descriptive names: `user_email` not `e`, `is_active` not `flag`"

### 3. Set Clear Boundaries
❌ Bad: "Handle all development tasks"
✅ Good: "Focus on backend API development, leave frontend to UI agents"

### 4. Provide Decision Criteria
❌ Bad: "Choose the best approach"
✅ Good: "Prioritize: 1) Correctness, 2) Readability, 3) Performance"

## Common Agent Types

### Developer Agents
- Focus on implementation
- Include coding standards
- Specify testing requirements
- Define commit practices

### Architect Agents
- Focus on design decisions
- Include architecture principles
- Specify documentation needs
- Define technology choices

### Reviewer Agents
- Focus on quality checks
- Include review criteria
- Specify feedback style
- Define approval standards

### Tester Agents
- Focus on test coverage
- Include test strategies
- Specify test types
- Define quality metrics

## Customization Tips

### 1. Language-Specific Agents
Include language idioms and best practices:
```markdown
## Python Best Practices
- Use list comprehensions for simple transformations
- Prefer f-strings for formatting
- Follow PEP 8 naming conventions
```

### 2. Framework-Specific Agents
Include framework patterns:
```markdown
## React Guidelines
- Use functional components with hooks
- Keep components small and focused
- Lift state up when needed
```

### 3. Project-Specific Agents
Include project conventions:
```markdown
## Project Conventions
- All API endpoints must have OpenAPI documentation
- Use our custom Logger class for all logging
- Follow our 3-layer architecture pattern
```

## Agent Interaction Patterns

### 1. Single-Purpose Agents
Best for focused tasks:
- Code formatting agent
- Security scanning agent
- Documentation generator

### 2. Collaborative Agents
For complex workflows:
- Architect designs, Developer implements
- Developer codes, Tester validates
- Reviewer checks, Developer fixes

### 3. Specialized Agents
For domain expertise:
- Database optimization agent
- Performance tuning agent
- Security audit agent

## Testing Your Agents

### 1. Clarity Test
Can someone understand the agent's purpose in 30 seconds?

### 2. Completeness Test
Does the agent have enough context to be effective?

### 3. Actionability Test
Can the agent make decisions based on the guidelines?

### 4. Consistency Test
Do the guidelines align with project standards?

## Common Pitfalls to Avoid

### 1. Over-Generalization
Don't make agents too broad - they become ineffective

### 2. Under-Specification
Don't leave too much ambiguous - agents need clear guidance

### 3. Contradiction
Ensure agent guidelines don't conflict with project standards

### 4. Outdated Information
Keep agents updated as the project evolves

## Maintenance

### Regular Reviews
- Review agents quarterly
- Update based on project changes
- Incorporate team feedback
- Remove obsolete agents

### Version Control
- Track agent changes in git
- Document why changes were made
- Consider agent versioning for major updates

## Examples of Effective Agents

### Example 1: API Developer Agent
```markdown
## Role
You are a REST API developer for the E-commerce Platform project.

## Responsibilities
1. Implement RESTful endpoints following OpenAPI specs
2. Ensure proper error handling with standard HTTP codes
3. Write integration tests for all endpoints
4. Document APIs using Swagger annotations

## Guidelines
- Use POST for creation, PUT for updates, PATCH for partial updates
- Return 201 Created with Location header for new resources
- Validate all inputs using our validation middleware
- Include pagination for list endpoints returning >20 items
```

### Example 2: Security Review Agent
```markdown
## Role
You are a security reviewer for the Banking Application project.

## Focus Areas
1. Authentication and authorization checks
2. Input validation and sanitization
3. Secure data handling and encryption
4. OWASP Top 10 vulnerability prevention

## Review Checklist
- [ ] No SQL injection vulnerabilities
- [ ] Proper password hashing (bcrypt with salt)
- [ ] Rate limiting on sensitive endpoints
- [ ] Audit logging for all transactions
```

Remember: The goal is to create agents that make Claude Code more effective for your specific project needs!