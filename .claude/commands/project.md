---
name: project
description: Start the Multi-Agent Squad project orchestration - creates project structure, deploys agents, and begins development workflow
---

# Project Command

This is the main entry point for the Multi-Agent Squad orchestration system.

## What This Command Does

Initiates the complete project setup and orchestration flow:

1. **Checks for existing project** - Looks for PROJECT.md
2. **Interactive setup** - Asks about your project if new
3. **Creates structure** - Sets up directories based on your needs
4. **Deploys agents** - Creates specialized AI agents
5. **Begins orchestration** - Starts managing your development

## Usage

Simply type:
- `/project`

Or in natural language:
- "Start a new project"
- "Set up project"
- "Begin orchestration"

## What Happens

When you run this command, I'll:

1. **Check if this is a new or existing project**
   - If PROJECT.md exists, I'll read it and continue orchestration
   - If not, I'll start the interactive setup

2. **Ask you key questions** (for new projects):
   - What are you building?
   - New project or existing code?
   - Monorepo or multi-repo?
   - How do you track issues?
   - Any specialized needs?

3. **Create your project structure**
   - `projects/` for multi-repo setups
   - `src/` for monorepos
   - `docs/` for documentation
   - `.claude/agents/` for your AI team

4. **Deploy specialized agents**
   - Product Manager for requirements
   - Architect for system design
   - Engineers for implementation
   - QA for testing
   - DevOps for deployment

5. **Begin orchestration**
   - Ready to manage features
   - Track progress
   - Coordinate development

## Example Flow

```
You: /project

Me: Hello! I'm your Multi-Agent Squad Orchestrator. 
    I see this is a new project setup. What are you building?

You: A task management web app

Me: Great! Is this a brand new project or do you have existing code?

You: Brand new

Me: How would you like to organize your code?
    - Monorepo (all code in one repository)
    - Multi-repo (separate repositories)
    - Let me decide

You: Multi-repo

[Continues with setup...]
```

## For Existing Projects

If you already have a PROJECT.md file:

```
You: /project

Me: I found your existing project configuration!
    Project: Task Management System
    Structure: Multi-repo (frontend, backend)
    Tracking: GitHub Issues
    
    What would you like to work on today?
```

## Related Commands

After project setup, use:
- `/start-feature` - Begin a new feature
- `/project-status` - Check current status
- `/create-agent` - Add specialized agents

## Tips

- Answer questions based on your actual needs
- You can always change configuration later
- The system adapts to your preferences
- No technical knowledge required

Ready to start? Just type `/project`!