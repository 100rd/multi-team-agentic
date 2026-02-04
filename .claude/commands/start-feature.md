---
name: start-feature
description: Start a new feature with full orchestration - creates GitHub issue, worktrees, and assigns agents
---

# Start Feature Command

This command initiates a new feature development with full Multi-Agent Squad orchestration.

## What This Command Does

1. **Gathers Requirements** - Prompts for feature details
2. **Creates GitHub Issue** - Tracks the feature (if integrated)
3. **Analyzes Impact** - Determines which repositories are affected
4. **Creates Worktrees** - Sets up isolated development environments
5. **Assigns Agents** - Deploys appropriate specialists
6. **Begins Development** - Kicks off implementation

## Usage

Simply say:
- `/start-feature`
- "Start a new feature"
- "I want to add [feature description]"

## Interactive Process

I'll ask you:

1. **Feature Name** (kebab-case, e.g., "user-authentication")
2. **Feature Description** (what should it do?)
3. **User Story** (as a user, I want...)
4. **Affected Components** (or I'll analyze)
5. **Priority** (high/medium/low)
6. **Target Deadline** (optional)

## Example Flow

```
You: /start-feature

Me: Let's start a new feature! What would you like to call it?

You: payment-integration

Me: Great! Please describe what this feature should do.

You: Add Stripe payment processing for subscriptions

Me: I'll analyze which repositories this affects...
- Backend: API endpoints for payment processing
- Frontend: Payment forms and subscription management
- Database: Schema updates for subscriptions

Creating worktrees:
✓ backend/feature-payment-integration
✓ frontend/feature-payment-integration

Assigning agents:
- Backend Developer Agent → Payment API
- Frontend Developer Agent → Payment UI
- Database Expert → Schema updates

GitHub Issue #47 created: "Feature: Payment Integration"

Ready to begin development! The PM Agent will now create detailed requirements.
```

## What Happens Next

1. **Product Manager Agent** creates detailed requirements
2. **Solution Architect** designs the implementation
3. **Developers** work in their assigned worktrees
4. **Progress** is tracked in GitHub
5. **PRs** are created when ready
6. **Review** by senior engineers
7. **Merge** and cleanup when complete

## Options

You can also specify details upfront:
- `/start-feature auth-system "User authentication with OAuth"`
- `/start-feature --priority=high payment-api`
- `/start-feature --repos=backend,frontend search-feature`

## Related Commands

- `/project-status` - Check feature progress
- `/create-agent` - Add specialized agents
- `/manage-worktrees` - Manual worktree management