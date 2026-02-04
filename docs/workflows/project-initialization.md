# Project Initialization Workflow

This document contains the complete workflow for initializing a new project with Multi-Agent Squad.

## Trigger Commands
- `/project`
- `/create-project`
- "Start a new project"
- "Initialize project"

## Workflow Steps

### Step 1: Check Project Status
```bash
# Check if PROJECT.md exists
if [ -f "PROJECT.md" ]; then
    echo "PROJECT.md found - reading project configuration..."
    # Read PROJECT.md and go to feature-development.md workflow
else
    echo "No PROJECT.md found - starting interactive setup..."
    # Continue with Step 2
fi
```

### Step 2: Interactive Project Setup
ASK THE USER THESE QUESTIONS IN ORDER:

1. **"Hello! I'm your Multi-Agent Squad Orchestrator. What are you building?"**
   - Listen carefully to understand their project
   - Examples: web app, API, mobile app, ML model, library

2. **"Is this a brand new project or do you have existing code?"**
   - If new → continue to question 3
   - If existing → ask "Where is your code located?"

3. **"How would you like to organize your code?"**
   - Listen to their preferences
   - Suggest options based on what they're building
   - Don't force predefined structures

4. **"How do you track tasks and issues?"**
   - GitHub Issues
   - Jira
   - Linear
   - Trello
   - Just markdown files
   - Let me suggest

5. **"Do you need any specialized expertise?"**
   - Listen for technical requirements
   - Note specialized needs for agent creation

6. **"What would you like me to automate?"**
   - Listen for specific pain points
   - Common needs: testing, formatting, reminders, quality checks

### Step 3: Create Project Structure
Based on conversation, create appropriate structure under `project/`:

```bash
# Create main project directory
mkdir -p project

# Create structure based on their needs
# Examples (adapt to what they described):

# For web app:
mkdir -p project/{frontend,backend,shared,docs}

# For library:
mkdir -p project/{src,tests,examples,docs}

# For microservices:
mkdir -p project/{services,shared,infrastructure,docs}
```

Show what you created with tree view.

### Step 4: Epic/Requirements Gathering
**"How would you like to provide project requirements?"**

a) I have requirements docs already
b) I use Jira/GitHub for requirements
c) Let's create them together now
d) I'll add requirements later

Press a, b, c, or d:

If c) selected → Go to `prd-creation.md` workflow

### Step 5: Integration Setup (Optional)
**"Would you like to set up any integrations?"**

Show options and let them choose.
If selected → Go to `integration-setup.md` workflow

### Step 6: Planning Approval
Show complete plan before executing.

### Step 7: Generate Configuration Files
- Create PROJECT.md with project details
- Create PROJECT_STATUS.md with initialization status
- Create project-specific hooks (only if requested)

### Step 8: Deploy Agents
Create agents based on project needs in correct categories:
- `.claude/agents/engineering/`
- `.claude/agents/product/`
- `.claude/agents/architecture/`
- `.claude/agents/specialized/`

### Step 9: Git Repository Setup
Ask about remote repositories and help connect if needed.

### Step 10: Show Summary
Display exactly what was created with file tree.

### Step 11: Next Actions
**"What would you like to work on next?"**

1️⃣ **Create Product Requirements Document (PRD)**
   → Go to `prd-creation.md` workflow

2️⃣ **Set up development environment**
   → Go to `dev-environment.md` workflow

3️⃣ **Start first feature**
   → Go to `feature-development.md` workflow

4️⃣ **Configure CI/CD**
   → Go to `cicd-setup.md` workflow

5️⃣ **Something else** (describe)

## Success Criteria
- ✅ Project structure created under `project/`
- ✅ PROJECT.md generated
- ✅ Appropriate agents deployed
- ✅ PROJECT_STATUS.md created
- ✅ User knows next steps