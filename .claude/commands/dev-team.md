---
name: dev-team
description: Launch a programmer-centric development team with fullstack engineers, architect, security engineer, QA, and DevOps — strict security, clean code, comprehensive testing
args: "<task-description> [--project NAME] [--stack node|python|go] [--frontend react|vue|next]"
---

# Development Team Command

Spawns a native Claude Code agent team built for **serious software development**. Every line of code is security-reviewed, every function is tested, every API endpoint is hardened. The Security Engineer has veto power over any merge.

## What This Command Does

1. **Creates an agent team** with the Lead in delegate mode (coordination only)
2. **Spawns 7 specialized teammates** covering architecture through deployment
3. **Enforces security-first development** — Security Engineer reviews everything with veto power
4. **Enforces clean code standards** — no `any` types, no magic numbers, no swallowed exceptions
5. **Enforces test coverage** — minimum 80% unit, integration tests for all APIs, E2E for critical paths
6. **Produces a fully tested, security-reviewed PR** with clean, production-ready code

## Team Roles

| Teammate | Agent | Mode | Responsibility |
|----------|-------|------|----------------|
| Architect | solution-architect | plan first | System design, API contracts, data models |
| Fullstack BE | senior-backend-engineer | plan first | Backend: APIs, services, DB, business logic |
| Fullstack FE | senior-frontend-engineer | plan first | Frontend: components, state, a11y, UX |
| Security | security-expert | normal | OWASP review, auth audit, dependency scan. **VETO POWER.** |
| QA | qa-engineer | normal | Test strategy, E2E, perf tests, edge cases |
| DevOps | devops-engineer | plan first | CI/CD, Docker, deployment, monitoring |

## Non-Negotiable Standards

Every piece of code from this team MUST meet:

### Security (enforced by Security Engineer)
- ALL input validated at API boundary
- ALL queries parameterized (no string concat SQL)
- ALL endpoints authenticated unless explicitly public
- ALL secrets from external managers (never hardcoded)
- ALL dependencies scanned for CVEs
- OWASP Top 10 prevention verified

### Clean Code (enforced by all engineers + Lead)
- Functions < 30 lines, single responsibility
- No `any` in TypeScript, no untyped dicts
- No dead code, no console.log in production
- Meaningful names, no magic numbers
- Organized imports, no unused dependencies

### Testing (enforced by QA Engineer)
- Unit test coverage >= 80%
- Integration tests for ALL API endpoints
- E2E tests for ALL critical user journeys
- Edge cases: null, empty, boundary, malicious input
- Performance baseline established

## Execution Flow

### Phase 1: Design (Plan Approval Required)
```
Task 1: Architecture design — API contracts, data model, components [Architect]
  → Lead reviews and approves/rejects
Task 2: Security review of design [Security Engineer]
  → Auth flow, trust boundaries, data exposure
Task 3: Test strategy [QA Engineer]
  → Test plan, coverage targets, E2E scenarios
```

### Phase 2: Implementation (Plan Approval Required)
```
Task 4: Backend implementation [Fullstack BE, plan mode]
  → APIs, services, DB, business logic, unit tests
Task 5: Frontend implementation [Fullstack FE, plan mode]
  → Components, state, routing, component tests
Task 6: Integration [Both engineers coordinate]
  → API integration, contract verification
```

### Phase 3: Review (Security Veto Gate)
```
Task 7: Security review of ALL code [Security Engineer]
  → OWASP check, dependency audit, auth verification
  → ⚠️ VETO POWER — blocks everything until fixed
Task 8: QA testing [QA Engineer]
  → Full test suite: unit, integration, E2E, performance
```

### Phase 4: Deploy + Validate
```
Task 9: CI/CD + Docker + staging deployment [DevOps]
Task 10: Staging validation [QA Engineer]
Task 11: Final security sign-off on deployed app [Security Engineer]
```

### Phase 5: Deliver
```
Task 12: Create feature branch, commit, PR [Lead]
```

## Usage Examples

```bash
# Build a fullstack application
/dev-team "User management system with auth, RBAC, CRUD, and admin dashboard"

# Build an API service
/dev-team "Real-time notification service with WebSocket, email, and push" --stack node

# Build a frontend app with existing API
/dev-team "Customer portal dashboard consuming existing REST API" --frontend next

# Extend an existing project
/dev-team "Add payment processing with Stripe to the e-commerce platform" --project ecommerce

# Build a microservice
/dev-team "Order processing microservice with event sourcing and CQRS" --stack go --project trading
```

## Team Spawn Prompt Template

The Lead will spawn each teammate with a detailed prompt including:

```
You are the {ROLE} on the development team for: {TASK_DESCRIPTION}

Project: {PROJECT_NAME}
Working directory: project/{PROJECT_NAME}/

Your responsibilities:
{ROLE_SPECIFIC_RESPONSIBILITIES}

NON-NEGOTIABLE STANDARDS (you MUST follow these):
1. Security: ALL input validated, ALL queries parameterized, ALL endpoints authenticated
2. Clean Code: Functions < 30 lines, no 'any' types, no dead code, meaningful names
3. Testing: >= 80% unit coverage, integration tests for APIs, edge cases tested
4. The Security Engineer has VETO POWER. If they block your code, fix it immediately.

Communication rules:
- Message the Lead for status updates and blockers
- Message other teammates directly for coordination
- Never edit files outside your assigned directories
- Follow the plan approval protocol before implementing

Read project history first:
cat project/PROJECT_HISTORY.md | tail -50
```

## Plan Approval Criteria

### Approve When
- API contracts are clear with request/response schemas
- Security is built into the design (auth, validation, encryption)
- Test strategy covers unit, integration, and E2E
- Clean code standards are acknowledged in the plan
- File ownership boundaries are respected
- Performance requirements are specified

### Reject When
- Missing security at ANY layer → "Add auth, validation, encryption"
- No test plan → "Include test strategy with >= 80% coverage target"
- Using `any` types → "Use strict TypeScript, define proper types"
- No error handling → "Define error strategy with safe client messages"
- Hardcoded values → "Use config/environment, no magic numbers"
- No input validation → "All API inputs must be validated at boundary"

## Security Engineer Veto Power

The Security Engineer can **block any merge** at any time. When BLOCKED:
1. ALL work on that component stops
2. The finding is shared with the relevant engineer
3. The engineer MUST fix the issue
4. The Security Engineer re-reviews
5. Only when cleared can work resume

This is non-negotiable. Security vulnerabilities in production are unacceptable.

## Integration with Existing Commands

- `/blast-radius` — before any deployment
- `/validate-deployment` — after staging deployment
- `/log-activity` — every teammate logs to project history
- `/query-history` — every teammate reads history on startup

## When the Team Finishes

1. All tasks marked complete
2. All quality gates passed (14 gates)
3. Security Engineer has given final sign-off
4. QA Engineer has validated staging deployment
5. PR created with all changes
6. Team cleanup runs
7. Project history updated by all teammates

## Arguments

- `task-description`: What to build (natural language)
- `--project NAME`: Project directory name (created under `project/`)
- `--stack node|python|go`: Backend technology stack (default: node)
- `--frontend react|vue|next`: Frontend framework (default: next)
- `--skip-deploy`: Stop after code review, don't deploy
- `--api-only`: No frontend, backend API only
- `--frontend-only`: No backend, frontend with existing API
