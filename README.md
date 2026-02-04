# Multi-Agent Squad 🤖

An intelligent orchestration system for Claude Code that adapts to your project structure and manages development through specialized AI agents.

## 🌟 Overview

Multi-Agent Squad transforms Claude Code into a complete software development team with enterprise-grade integrations. Simply start Claude in this directory, and it will:

1. **Ask you about your project** through natural conversation
2. **Create the perfect structure** based on your needs
3. **Set up specialized agents** for your project type
4. **Configure integrations** with 30+ popular tools
5. **Enable MCP servers** for enhanced AI capabilities
6. **Orchestrate development** through the entire lifecycle
7. **Automate workflows** based on your specific needs

### 🎯 Complete System Architecture

```
┌──────────────────────────────────────────────────────┐
│                     MULTI-AGENT SQUAD                │
│                                                      │
│  ┌────────────────────┐    ┌─────────────────────┐   │
│  │   AI AGENTS        │    │   INTEGRATIONS      │   │
│  │                    │    │                     │   │
│  │ • Orchestrator     │    │ • Slack/Teams       │   │
│  │ • Product Mgr      │    │ • Jira/Linear       │   │
│  │ • Architect        │    │ • GitHub/GitLab     │   │
│  │ • Engineers        │    │ • CI/CD Tools       │   │
│  │ • QA/DevOps        │    │ • Monitoring        │   │
│  └────────────────────┘    └─────────────────────┘   │
│                                                      │
│  ┌────────────────────┐    ┌─────────────────────┐   │
│  │   MCP SERVERS      │    │   AUTOMATION        │   │
│  │                    │    │                     │   │
│  │ • Database         │    │ • Claude Hooks      │   │
│  │ • GitHub API       │    │ • Git Hooks         │   │
│  │ • Memory           │    │ • Sprint Mgmt       │   │
│  │ • Analytics        │    │ • PR Reviews        │   │
│  │ • Docker/K8s       │    │ • Quality Gates     │   │
│  └────────────────────┘    └─────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/bijutharakan/multi-agent-squad.git
cd multi-agent-squad

# 2. Start Claude Code
claude

# 3. Start the orchestration with ONE of these commands:
/project          # Recommended: Start project orchestration
"Start project"   # Natural language also works
"Help me set up"  # Any variation works
```

The `/project` command triggers the complete orchestration setup!

### 🌟 What You Get

After setup, you'll have:
- **🤖 Specialized AI agents** tailored to your project
- **🔌 Configured integrations** with your existing tools
- **🚀 MCP servers** for enhanced capabilities
- **🦝 Automated workflows** based on your needs
- **📊 Sprint management** with review cycles
- **🔔 Smart notifications** where you want them
- **🔐 Security checks** and quality gates

## 🎯 How It Works

### First Time Setup

When you start Claude with `/project`, it will guide you through:

1. **"What are you building?"** - Describe your project
2. **"Is this new or existing?"** - It adapts accordingly  
3. **"Monorepo or multi-repo?"** - Your choice
4. **"How do you track tasks?"** - GitHub, Jira, Linear, or manual
5. **"What would you like to automate?"** - Custom hooks for your needs
6. **"Which integrations?"** - Slack, email, Teams, and more
7. **"Enable MCP servers?"** - Enhanced AI capabilities

Claude then creates the perfect structure, integrations, and automations for YOUR project.

### Flexible Structure Examples

#### For a Multi-Repo Web App
```
your-project/
├── CLAUDE.md          # Orchestration instructions
├── PROJECT.md         # Your project details
├── projects/          # Your repos (you manage these)
│   ├── frontend/      # Your React app
│   └── backend/       # Your API
├── docs/              # All documentation
└── .claude/agents/    # Your AI team
```

#### For a Monorepo
```
your-project/
├── CLAUDE.md          # Orchestration instructions
├── PROJECT.md         # Your project details
├── src/               # All your code
│   ├── frontend/
│   ├── backend/
│   └── shared/
├── docs/              # Documentation
└── .claude/agents/    # Your AI team
```

#### For a Documentation Project
```
your-project/
├── CLAUDE.md          # Orchestration instructions
├── PROJECT.md         # Project details
├── docs/              # All documentation
│   ├── architecture/
│   ├── guides/
│   └── api/
└── .claude/agents/    # Documentation-focused agents
```

## 🎭 Your AI Development Team

Based on your project, Claude will suggest relevant agents:

### For Full-Stack Projects
- **🎯 Prime Orchestrator** - Manages the entire workflow
- **📊 Product Manager** - Requirements and user stories
- **🏗️ Solution Architect** - System design
- **💻 Backend Engineer** - API development
- **🎨 Frontend Engineer** - User interface
- **✅ QA Engineer** - Testing
- **🔧 DevOps Engineer** - Deployment

### For API Projects
- **🏗️ API Architect** - API design
- **💻 Backend Engineer** - Implementation
- **📖 API Documentation Specialist** - Docs
- **✅ API Test Engineer** - Testing

### For Documentation Projects
- **📝 Technical Writer** - Documentation
- **🏗️ Information Architect** - Structure
- **👁️ Documentation Reviewer** - Quality

## 🛠️ Key Features

### 🤖 Enterprise Agile Workflow
- **Sprint Management** - Automated ceremonies and tracking
- **PR Review Cycles** - Enforced code review with comment resolution
- **Quality Gates** - Automated checks before phase transitions
- **Human Checkpoints** - Critical decisions require approval
- **Daily Standups** - Automated reminders and reports

### Natural Language Control
Just talk to Claude normally:
- "I need to add user authentication"
- "Help me set up CI/CD"
- "Create API documentation"
- "Review our architecture"

### Intelligent Automation (Claude Code Hooks)
Tell Claude what you want automated:
- **"I forget to run tests"** → Auto-runs tests after file changes
- **"Remind me of daily standups"** → 9 AM Slack/email reminders
- **"Check code quality"** → Auto-lint and format on save
- **"Track my progress"** → Automatic time tracking and reports
- **"Security checks"** → Scan for secrets before commits
- **"Break reminders"** → Health reminders every hour

Hooks are dynamically generated based on YOUR specific needs using:
```bash
python scripts/generate-hooks.py
```

### 🔌 Extensive Integrations (30+ Tools)

#### Project Management
- **GitHub** - Issues, PRs, Projects, Actions
- **Jira** - Sprints, epics, stories, burndown charts
- **Linear** - Modern issue tracking with cycles
- **Azure DevOps** - Boards, repos, pipelines
- **ClickUp, Monday.com, Asana** - Visual project management

#### Communication
- **Slack** - Real-time notifications, daily summaries, thread management
- **Microsoft Teams** - Adaptive cards, channel updates
- **Discord** - Webhooks, embeds for communities
- **Email** - HTML/plain text, daily digests, critical alerts

#### Development & DevOps
- **CI/CD** - GitHub Actions, Jenkins, GitLab CI, CircleCI
- **Monitoring** - Sentry, Datadog, Prometheus, New Relic
- **Testing** - BrowserStack, SonarQube, Cypress Dashboard
- **Documentation** - Confluence, Notion, GitHub Wiki
- **Time Tracking** - Toggl, Harvest, Clockify

### 🚀 MCP (Model Context Protocol) Server Support

Extend Claude's capabilities with 14+ pre-configured MCP servers:

#### Data & Storage
- **PostgreSQL Explorer** - Natural language database queries
- **Memory Server** - Persistent context across Claude sessions
- **Enhanced Filesystem** - Advanced file operations with permissions

#### Development Tools  
- **GitHub Integration** - Deep PR and issue management
- **Test Runner** - Execute and monitor test suites
- **Docker Management** - Container and image control
- **Kubernetes** - Deployment and pod management

#### Communication & Docs
- **Slack Server** - Read channels, send messages
- **Linear Server** - Full issue tracking integration
- **Notion Server** - Access pages and databases
- **Confluence Server** - Documentation management

#### Analytics & Monitoring
- **Project Analytics** - Custom metrics and insights
- **Monitoring Integration** - Datadog, Prometheus access

Setup with: `python scripts/mcp-server-setup.py`

### Smart Development Workflow
1. **Requirements** → PM agent creates specs
2. **Design** → Architect creates system design
3. **Implementation** → Engineers build it
4. **Testing** → QA ensures quality
5. **Deployment** → DevOps handles release

### Git Worktree Support (Optional)
For multi-repo projects with parallel development:
```bash
./scripts/worktree-manager.sh create-feature auth frontend backend
```

## 📋 No Complex Setup Required

Unlike other tools, Multi-Agent Squad:
- ✅ **No installation process** - Just clone and start
- ✅ **No configuration files** - Claude asks what you need
- ✅ **No forced structure** - Adapts to your preferences
- ✅ **No learning curve** - Plain English control

## 🔧 System Requirements

### Required
- **Git** - For version control
- **Claude Code** - The AI interface

### Optional
- **GitHub CLI** (`gh`) - For GitHub integration
- **Python 3.8+** - For automation scripts
- **Jira API Token** - For Jira integration

Claude will check what you have and work with it!

## 🔧 Available Scripts & Tools

### Core Orchestration
- **`/project`** - Main entry point to start orchestration
- **`worktree-manager.sh`** - Git worktree management for multi-repo
- **`discover-project.py`** - Analyze existing codebases

### Integration Scripts
- **`integration-setup.py`** - Universal integration manager
- **`mcp-server-setup.py`** - MCP server configuration
- **`agile-tools-setup.py`** - Agile tool integrations
- **`slack-integration.py`** - Slack webhook setup
- **`email-integration.py`** - Email notification setup
- **`github-integration.py`** - GitHub API automation

### Workflow Automation
- **`sprint-management.sh`** - Sprint ceremonies and tracking
- **`pr-review-cycle.sh`** - Automated PR review enforcement
- **`generate-hooks.py`** - Dynamic hook generation
- **`setup-git-hooks.sh`** - Git hook configuration

## 🎯 Example Workflows

### Starting a New SaaS Product
```
You: "/project"
Claude: "Hello! I'm your Multi-Agent Squad Orchestrator. What are you building?"
You: "A SaaS product for team collaboration"
Claude: "Great! Is this a new project or existing code?"
You: "Brand new"
Claude: "How would you like to organize your code?"
[Shows options: monorepo, multi-repo, etc.]
You: "Multi-repo - separate frontend and backend"
Claude: "What would you like me to automate for you?"
You: "I often forget to run tests"
Claude: [Creates structure, agents, test automation hooks]
```

### Setting Up Integrations
```
You: "Set up Slack notifications for builds"
Claude: "I'll help you set up Slack integration. Running the setup..."
[Interactive setup with permissions]
Claude: "Would you like notifications for:
  a) Build status
  b) Test results  
  c) Daily standup reminders
  d) PR reviews"
You: "All of them"
Claude: [Configures Slack with all requested notifications]
```

### Using MCP Servers
```
You: "Show me all users in our database"
Claude: [Uses PostgreSQL MCP server]
"Here are the users in your database:
- alice@example.com (Admin)
- bob@example.com (User)
- charlie@example.com (User)"

You: "What's our test coverage?"
Claude: [Uses Analytics MCP server]
"Current test coverage: 78%
- Frontend: 82%
- Backend: 74%
Trend: +3% this week"
```

## 🎆 What Makes This Different?

### 🧠 True AI Orchestration
Unlike simple templates or scripts, Multi-Agent Squad uses Claude's intelligence to:
- **Understand your project** contextually, not through rigid configs
- **Adapt to your workflow** instead of forcing you into one
- **Learn your preferences** and adjust automation accordingly
- **Make intelligent decisions** while keeping you in control

### 🔗 Native Claude Code Integration
- **Built for Claude Code** - Not a generic framework
- **Uses sub-agents** - Real AI delegation, not just prompts
- **MCP Protocol** - Direct tool access, not API wrappers
- **Claude Hooks** - Deep integration with your workflow

### 🎯 Zero Configuration Philosophy
- **No YAML files** - Just conversation
- **No setup wizards** - Claude asks what it needs
- **No dependencies** - Works with what you have
- **No lock-in** - Your project, your way

## 🤝 Integration Setup

Multi-Agent Squad supports 30+ integrations across all aspects of agile development:

### Quick Setup Commands
```bash
# Interactive integration setup (recommended)
python scripts/integration-setup.py

# Set up MCP servers for enhanced capabilities
python scripts/mcp-server-setup.py

# Configure specific agile tools
python scripts/agile-tools-setup.py

# Individual integrations
python scripts/slack-integration.py      # Slack notifications
python scripts/email-integration.py      # Email alerts
python scripts/github-integration.py     # GitHub automation
```

### Integration Categories
- **📋 Project Management** - GitHub, Jira, Linear, Azure DevOps, ClickUp
- **💬 Communication** - Slack, Teams, Discord, Email
- **📄 Documentation** - Confluence, Notion, GitHub Wiki  
- **🚀 CI/CD** - GitHub Actions, Jenkins, GitLab CI
- **📊 Monitoring** - Sentry, Datadog, Prometheus
- **🧪 Testing** - BrowserStack, SonarQube, Cypress
- **⏱️ Time Tracking** - Toggl, Harvest, Clockify

See [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) for complete setup instructions.

## 📚 Advanced Features

### 🔐 Security & Permissions
- **Credential Management** - Secure storage in `.env.*` files
- **Permission Scoping** - Minimal required access
- **Secret Detection** - Pre-commit hooks for security
- **MCP Server Security** - Warnings for internet-accessing servers

### Custom Agent Creation
```
You: "I need an agent who understands blockchain"
Claude: [Creates specialized blockchain agent]
```

### MCP Server Capabilities
```
You: "Show me all users in the database"
Claude: [Uses PostgreSQL MCP server to query directly]

You: "What's our test coverage trend?"
Claude: [Uses Analytics MCP server to show metrics]
```

### Multi-Environment Support
- Development
- Staging  
- Production
- All managed through conversation

### Automated Workflows
- Code review orchestration
- Deployment pipelines
- Documentation updates
- Sprint ceremonies
- All through plain English

### Critical Decision Gates
Claude always asks permission for:
- Production deployments
- Database migrations
- Security changes
- Main branch merges
- Resource deletion

## 🛡️ Philosophy

Multi-Agent Squad believes in:
- **Flexibility** - Your project, your way
- **Simplicity** - No complex commands or configs
- **Intelligence** - Agents with real expertise
- **Adaptability** - Works with what you have
- **Transparency** - Clear, documented decisions

## 🚦 Getting Help

### Ask Claude
- "How do I add a new feature?"
- "What agents do I have?"
- "Show me the project status"
- "Help me set up Slack notifications"
- "Configure MCP servers for my database"
- "Create a custom automation hook"

### Check Documentation
- **[INTEGRATIONS.md](docs/INTEGRATIONS.md)** - Complete integration guide
- **[AGILE_WORKFLOW.md](docs/AGILE_WORKFLOW.md)** - Enterprise workflow details
- **[HOOKS_GUIDE.md](docs/HOOKS_GUIDE.md)** - Automation hook reference
- **[AGENT_GUIDELINES.md](docs/AGENT_GUIDELINES.md)** - Agent creation guide

### Quick Commands
```bash
# List available integrations
python scripts/integration-setup.py

# Check MCP server status
python scripts/mcp-server-setup.py check

# View configured tools
python scripts/agile-tools-setup.py list
```

## 📄 License

MIT License - see LICENSE file

## 🙏 Contributing

We welcome contributions! The best way to contribute is to use the system and share your experience.

---

**Ready to start?** Just `cd` into this directory and start Claude Code. No installation, no configuration, just natural conversation to build amazing software!

*Multi-Agent Squad: Where AI meets human creativity to build exceptional software.*
