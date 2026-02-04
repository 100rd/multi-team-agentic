#!/usr/bin/env python3
"""
Agile Tools Integration Setup for Multi-Agent Squad
Configures popular agile development tools and services
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

class AgileToolsSetup:
    def __init__(self):
        self.config_dir = Path(".claude/integrations")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Popular agile tools and integrations
        self.agile_tools = {
            "project_management": {
                "github": {
                    "name": "GitHub Issues & Projects",
                    "description": "Issue tracking, project boards, and milestones",
                    "setup": self._setup_github
                },
                "jira": {
                    "name": "Jira",
                    "description": "Enterprise agile project management",
                    "setup": self._setup_jira
                },
                "linear": {
                    "name": "Linear",
                    "description": "Modern issue tracking for software teams",
                    "setup": self._setup_linear
                },
                "azure_devops": {
                    "name": "Azure DevOps",
                    "description": "Microsoft's agile planning tools",
                    "setup": self._setup_azure_devops
                },
                "monday": {
                    "name": "Monday.com",
                    "description": "Visual project management",
                    "setup": self._setup_monday
                },
                "clickup": {
                    "name": "ClickUp",
                    "description": "All-in-one project management",
                    "setup": self._setup_clickup
                },
                "asana": {
                    "name": "Asana",
                    "description": "Work management platform",
                    "setup": self._setup_asana
                }
            },
            "communication": {
                "slack": {
                    "name": "Slack",
                    "description": "Team communication and notifications",
                    "setup": self._setup_slack
                },
                "teams": {
                    "name": "Microsoft Teams",
                    "description": "Enterprise communication platform",
                    "setup": self._setup_teams
                },
                "discord": {
                    "name": "Discord",
                    "description": "Voice, video, and text communication",
                    "setup": self._setup_discord
                }
            },
            "documentation": {
                "confluence": {
                    "name": "Confluence",
                    "description": "Team documentation and knowledge base",
                    "setup": self._setup_confluence
                },
                "notion": {
                    "name": "Notion",
                    "description": "All-in-one workspace for notes and docs",
                    "setup": self._setup_notion
                },
                "wiki": {
                    "name": "GitHub/GitLab Wiki",
                    "description": "Repository-based documentation",
                    "setup": self._setup_wiki
                }
            },
            "ci_cd": {
                "github_actions": {
                    "name": "GitHub Actions",
                    "description": "CI/CD workflows in GitHub",
                    "setup": self._setup_github_actions
                },
                "jenkins": {
                    "name": "Jenkins",
                    "description": "Open source automation server",
                    "setup": self._setup_jenkins
                },
                "gitlab_ci": {
                    "name": "GitLab CI/CD",
                    "description": "GitLab's built-in CI/CD",
                    "setup": self._setup_gitlab_ci
                },
                "circleci": {
                    "name": "CircleCI",
                    "description": "Continuous integration platform",
                    "setup": self._setup_circleci
                }
            },
            "monitoring": {
                "datadog": {
                    "name": "Datadog",
                    "description": "Monitoring and analytics platform",
                    "setup": self._setup_datadog
                },
                "sentry": {
                    "name": "Sentry",
                    "description": "Error tracking and performance monitoring",
                    "setup": self._setup_sentry
                },
                "prometheus": {
                    "name": "Prometheus + Grafana",
                    "description": "Open source monitoring solution",
                    "setup": self._setup_prometheus
                },
                "newrelic": {
                    "name": "New Relic",
                    "description": "Application performance monitoring",
                    "setup": self._setup_newrelic
                }
            },
            "testing": {
                "browserstack": {
                    "name": "BrowserStack",
                    "description": "Cross-browser testing platform",
                    "setup": self._setup_browserstack
                },
                "sonarqube": {
                    "name": "SonarQube",
                    "description": "Code quality and security analysis",
                    "setup": self._setup_sonarqube
                },
                "cypress": {
                    "name": "Cypress Dashboard",
                    "description": "E2E testing dashboard",
                    "setup": self._setup_cypress
                }
            },
            "time_tracking": {
                "toggl": {
                    "name": "Toggl Track",
                    "description": "Time tracking for teams",
                    "setup": self._setup_toggl
                },
                "harvest": {
                    "name": "Harvest",
                    "description": "Time tracking and invoicing",
                    "setup": self._setup_harvest
                },
                "clockify": {
                    "name": "Clockify",
                    "description": "Free time tracking",
                    "setup": self._setup_clockify
                }
            }
        }
        
    def interactive_setup(self) -> None:
        """Main interactive setup flow"""
        print("\n🛠️ Agile Tools Integration Setup")
        print("━" * 50)
        print("\nLet's set up integrations with your agile development tools.")
        print("This will help automate your workflow and keep everything in sync.\n")
        
        # Show categories
        categories = list(self.agile_tools.keys())
        print("Available categories:")
        for i, cat in enumerate(categories):
            formatted_cat = cat.replace("_", " ").title()
            print(f"  {i+1}) {formatted_cat}")
            
        print(f"  {len(categories)+1}) Set up all recommended tools")
        print(f"  {len(categories)+2}) Skip setup")
        
        choice = input("\nSelect category (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx == len(categories):
                self._setup_recommended()
            elif idx == len(categories) + 1:
                print("✅ Skipping tool setup. You can run this anytime.")
                return
            elif 0 <= idx < len(categories):
                self._setup_category(categories[idx])
            else:
                print("Invalid selection")
        except:
            print("Invalid input")
            
    def _setup_category(self, category: str) -> None:
        """Set up tools in a specific category"""
        tools = self.agile_tools[category]
        formatted_cat = category.replace("_", " ").title()
        
        print(f"\n📌 {formatted_cat} Tools:")
        print("━" * 50)
        
        tool_list = list(tools.items())
        for i, (tool_id, tool) in enumerate(tool_list):
            print(f"  {i+1}) {tool['name']}: {tool['description']}")
            
        print(f"  {len(tool_list)+1}) Go back")
        
        choice = input("\nSelect tool to set up (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if idx == len(tool_list):
                self.interactive_setup()
                return
            elif 0 <= idx < len(tool_list):
                tool_id, tool = tool_list[idx]
                tool['setup'](tool_id)
                
                # Ask if they want to set up another
                another = input("\nSet up another tool? (y/n): ").strip().lower()
                if another == 'y':
                    self._setup_category(category)
        except:
            print("Invalid input")
            
    def _setup_recommended(self) -> None:
        """Set up recommended tools based on common patterns"""
        print("\n🎯 Setting up recommended agile tools...")
        print("━" * 50)
        
        print("\nI'll set up the most common integrations:")
        print("1. Project Management: GitHub Issues or Jira")
        print("2. Communication: Slack")
        print("3. Documentation: Confluence or GitHub Wiki")
        print("4. CI/CD: GitHub Actions")
        print("5. Monitoring: Sentry for errors")
        
        confirm = input("\nProceed with recommended setup? (y/n): ").strip().lower()
        if confirm != 'y':
            return
            
        # Project management
        pm_choice = input("\nProject Management - GitHub Issues (g) or Jira (j)? ").strip().lower()
        if pm_choice == 'g':
            self._setup_github("github")
        elif pm_choice == 'j':
            self._setup_jira("jira")
            
        # Communication
        slack_choice = input("\nSet up Slack integration? (y/n): ").strip().lower()
        if slack_choice == 'y':
            self._setup_slack("slack")
            
        # Documentation
        doc_choice = input("\nDocumentation - Confluence (c) or GitHub Wiki (w)? ").strip().lower()
        if doc_choice == 'c':
            self._setup_confluence("confluence")
        elif doc_choice == 'w':
            self._setup_wiki("wiki")
            
        # CI/CD
        ci_choice = input("\nSet up GitHub Actions? (y/n): ").strip().lower()
        if ci_choice == 'y':
            self._setup_github_actions("github_actions")
            
        # Monitoring
        sentry_choice = input("\nSet up Sentry for error tracking? (y/n): ").strip().lower()
        if sentry_choice == 'y':
            self._setup_sentry("sentry")
            
        print("\n✅ Recommended tools configured!")
        
    # Tool-specific setup methods
    def _setup_github(self, tool_id: str) -> None:
        """Set up GitHub integration"""
        print("\n🐙 GitHub Integration Setup")
        print("━" * 50)
        
        print("\nGitHub integration enables:")
        print("• Automatic issue creation from Claude")
        print("• PR management and reviews")
        print("• Project board updates")
        print("• Milestone tracking")
        
        token = input("\nEnter GitHub Personal Access Token (or 'skip'): ").strip()
        if token.lower() == 'skip':
            return
            
        repo = input("Enter repository (owner/repo): ").strip()
        
        config = {
            "type": "github",
            "token": token,
            "repository": repo,
            "features": {
                "issues": True,
                "projects": True,
                "pull_requests": True,
                "actions": True
            }
        }
        
        self._save_config("github", config)
        self._create_github_hooks()
        
        print("✅ GitHub integration configured!")
        
    def _setup_jira(self, tool_id: str) -> None:
        """Set up Jira integration"""
        print("\n🎯 Jira Integration Setup")
        print("━" * 50)
        
        print("\nJira integration enables:")
        print("• Sprint management")
        print("• Story creation and updates")
        print("• Epic tracking")
        print("• Burndown charts")
        
        url = input("\nEnter Jira URL (e.g., company.atlassian.net): ").strip()
        if not url:
            return
            
        email = input("Enter email: ").strip()
        token = input("Enter API token: ").strip()
        project = input("Enter project key: ").strip()
        
        config = {
            "type": "jira",
            "url": f"https://{url}",
            "email": email,
            "token": token,
            "project": project,
            "features": {
                "sprints": True,
                "epics": True,
                "stories": True,
                "subtasks": True
            }
        }
        
        self._save_config("jira", config)
        self._create_jira_automation()
        
        print("✅ Jira integration configured!")
        
    def _setup_linear(self, tool_id: str) -> None:
        """Set up Linear integration"""
        print("\n📊 Linear Integration Setup")
        print("━" * 50)
        
        api_key = input("\nEnter Linear API key: ").strip()
        if not api_key:
            return
            
        config = {
            "type": "linear",
            "api_key": api_key,
            "features": {
                "issues": True,
                "projects": True,
                "cycles": True
            }
        }
        
        self._save_config("linear", config)
        print("✅ Linear integration configured!")
        
    def _setup_slack(self, tool_id: str) -> None:
        """Set up Slack integration"""
        # Delegate to existing slack integration script
        import subprocess
        subprocess.run([sys.executable, "scripts/slack-integration.py"])
        
    def _setup_teams(self, tool_id: str) -> None:
        """Set up Microsoft Teams integration"""
        print("\n👥 Microsoft Teams Integration Setup")
        print("━" * 50)
        
        webhook = input("\nEnter Teams webhook URL: ").strip()
        if not webhook:
            return
            
        config = {
            "type": "teams",
            "webhook_url": webhook,
            "features": {
                "notifications": True,
                "daily_summary": True
            }
        }
        
        self._save_config("teams", config)
        print("✅ Teams integration configured!")
        
    def _setup_confluence(self, tool_id: str) -> None:
        """Set up Confluence integration"""
        print("\n📚 Confluence Integration Setup")
        print("━" * 50)
        
        url = input("\nEnter Confluence URL: ").strip()
        email = input("Enter email: ").strip()
        token = input("Enter API token: ").strip()
        space = input("Enter space key: ").strip()
        
        if not all([url, email, token, space]):
            return
            
        config = {
            "type": "confluence",
            "url": url,
            "email": email,
            "token": token,
            "space": space,
            "features": {
                "pages": True,
                "templates": True,
                "search": True
            }
        }
        
        self._save_config("confluence", config)
        print("✅ Confluence integration configured!")
        
    def _setup_notion(self, tool_id: str) -> None:
        """Set up Notion integration"""
        print("\n📝 Notion Integration Setup")
        print("━" * 50)
        
        token = input("\nEnter Notion integration token: ").strip()
        if not token:
            return
            
        config = {
            "type": "notion",
            "token": token,
            "features": {
                "pages": True,
                "databases": True,
                "search": True
            }
        }
        
        self._save_config("notion", config)
        print("✅ Notion integration configured!")
        
    def _setup_github_actions(self, tool_id: str) -> None:
        """Set up GitHub Actions workflows"""
        print("\n🚀 GitHub Actions Setup")
        print("━" * 50)
        
        print("\nI'll create workflow templates for:")
        print("• CI/CD pipeline")
        print("• Automated testing")
        print("• Code quality checks")
        print("• Security scanning")
        
        confirm = input("\nCreate workflow templates? (y/n): ").strip().lower()
        if confirm == 'y':
            self._create_github_workflows()
            print("✅ GitHub Actions workflows created!")
            
    def _setup_sentry(self, tool_id: str) -> None:
        """Set up Sentry integration"""
        print("\n🐛 Sentry Integration Setup")
        print("━" * 50)
        
        dsn = input("\nEnter Sentry DSN: ").strip()
        if not dsn:
            return
            
        config = {
            "type": "sentry",
            "dsn": dsn,
            "features": {
                "error_tracking": True,
                "performance": True,
                "release_tracking": True
            }
        }
        
        self._save_config("sentry", config)
        print("✅ Sentry integration configured!")
        
    # Placeholder methods for other tools
    def _setup_azure_devops(self, tool_id: str) -> None:
        self._generic_setup("Azure DevOps", tool_id)
        
    def _setup_monday(self, tool_id: str) -> None:
        self._generic_setup("Monday.com", tool_id)
        
    def _setup_clickup(self, tool_id: str) -> None:
        self._generic_setup("ClickUp", tool_id)
        
    def _setup_asana(self, tool_id: str) -> None:
        self._generic_setup("Asana", tool_id)
        
    def _setup_discord(self, tool_id: str) -> None:
        self._generic_setup("Discord", tool_id)
        
    def _setup_wiki(self, tool_id: str) -> None:
        print("\n📖 Wiki Setup")
        print("Wiki documentation is automatically available in your repository.")
        print("Enable it in your repository settings.")
        
    def _setup_jenkins(self, tool_id: str) -> None:
        self._generic_setup("Jenkins", tool_id)
        
    def _setup_gitlab_ci(self, tool_id: str) -> None:
        self._generic_setup("GitLab CI/CD", tool_id)
        
    def _setup_circleci(self, tool_id: str) -> None:
        self._generic_setup("CircleCI", tool_id)
        
    def _setup_datadog(self, tool_id: str) -> None:
        self._generic_setup("Datadog", tool_id)
        
    def _setup_prometheus(self, tool_id: str) -> None:
        self._generic_setup("Prometheus", tool_id)
        
    def _setup_newrelic(self, tool_id: str) -> None:
        self._generic_setup("New Relic", tool_id)
        
    def _setup_browserstack(self, tool_id: str) -> None:
        self._generic_setup("BrowserStack", tool_id)
        
    def _setup_sonarqube(self, tool_id: str) -> None:
        self._generic_setup("SonarQube", tool_id)
        
    def _setup_cypress(self, tool_id: str) -> None:
        self._generic_setup("Cypress Dashboard", tool_id)
        
    def _setup_toggl(self, tool_id: str) -> None:
        self._generic_setup("Toggl Track", tool_id)
        
    def _setup_harvest(self, tool_id: str) -> None:
        self._generic_setup("Harvest", tool_id)
        
    def _setup_clockify(self, tool_id: str) -> None:
        self._generic_setup("Clockify", tool_id)
        
    def _generic_setup(self, name: str, tool_id: str) -> None:
        """Generic setup for tools"""
        print(f"\n🔧 {name} Setup")
        print("━" * 50)
        print(f"\n{name} integration requires manual configuration.")
        print("Please refer to their documentation for setup instructions.")
        
        config = {
            "type": tool_id,
            "configured": False,
            "notes": "Manual configuration required"
        }
        
        self._save_config(tool_id, config)
        
    def _save_config(self, tool_id: str, config: Dict) -> None:
        """Save tool configuration"""
        config_file = self.config_dir / f"{tool_id}.json"
        
        # Mask sensitive data
        safe_config = config.copy()
        for key in ["token", "api_key", "password", "dsn"]:
            if key in safe_config:
                safe_config[key] = "***CONFIGURED***"
                
        with open(config_file, 'w') as f:
            json.dump(safe_config, f, indent=2)
            
        # Create .env file for sensitive data
        env_file = Path(f".env.{tool_id}")
        with open(env_file, 'w') as f:
            for key in ["token", "api_key", "password", "dsn"]:
                if key in config:
                    f.write(f"{tool_id.upper()}_{key.upper()}={config[key]}\n")
                    
        # Add to .gitignore
        gitignore = Path(".gitignore")
        if gitignore.exists():
            with open(gitignore, 'a') as f:
                if f".env.{tool_id}" not in open(gitignore).read():
                    f.write(f"\n.env.{tool_id}\n")
                    
    def _create_github_hooks(self) -> None:
        """Create GitHub-specific automation hooks"""
        hooks_dir = Path(".claude/hooks")
        hooks_dir.mkdir(parents=True, exist_ok=True)
        
        hooks_content = """# GitHub Integration Hooks

[[hooks]]
event = "UserPromptSubmit"
[hooks.matcher]
content_regex = "create.*issue|new.*issue|file.*bug"
command = '''
echo "📝 Creating GitHub issue..."
python scripts/github-integration.py create-issue
'''

[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Bash"
args_regex = "git push.*origin"
command = '''
echo "🔗 Creating pull request..."
python scripts/github-integration.py auto-pr
'''
"""
        
        with open(hooks_dir / "github-hooks.toml", 'w') as f:
            f.write(hooks_content)
            
    def _create_jira_automation(self) -> None:
        """Create Jira automation scripts"""
        script_content = '''#!/usr/bin/env python3
"""Jira automation helpers"""

import json
from pathlib import Path

def create_story(title, description):
    """Create a new Jira story"""
    # Implementation would go here
    print(f"Would create story: {title}")
    
def update_sprint():
    """Update sprint progress"""
    # Implementation would go here
    print("Would update sprint progress")
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "story":
            create_story(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
        elif sys.argv[1] == "sprint":
            update_sprint()
'''
        
        script_path = Path("scripts/jira-automation.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
    def _create_github_workflows(self) -> None:
        """Create GitHub Actions workflow templates"""
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # CI/CD workflow
        ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up environment
      run: |
        # Add your setup commands here
        echo "Setting up environment..."
        
    - name: Run tests
      run: |
        # Add your test commands here
        echo "Running tests..."
        
    - name: Check code quality
      run: |
        # Add linting/formatting checks
        echo "Checking code quality..."
        
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Build application
      run: |
        # Add your build commands
        echo "Building application..."
        
    - name: Deploy
      run: |
        # Add deployment steps
        echo "Deploying..."
"""
        
        with open(workflows_dir / "ci-cd.yml", 'w') as f:
            f.write(ci_workflow)
            
        # Security scanning workflow
        security_workflow = """name: Security Scan

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  push:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      run: |
        # Add security scanning tools
        echo "Running security scan..."
"""
        
        with open(workflows_dir / "security.yml", 'w') as f:
            f.write(security_workflow)


def main():
    """Main entry point"""
    setup = AgileToolsSetup()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            print("\nAvailable Agile Tools:")
            print("━" * 50)
            for category, tools in setup.agile_tools.items():
                print(f"\n{category.replace('_', ' ').title()}:")
                for tool_id, tool in tools.items():
                    print(f"  • {tool['name']}: {tool['description']}")
        elif sys.argv[1] == "check":
            # Check configured tools
            configs = list(setup.config_dir.glob("*.json"))
            if configs:
                print("\nConfigured tools:")
                for config in configs:
                    print(f"  ✓ {config.stem}")
            else:
                print("No tools configured yet.")
    else:
        setup.interactive_setup()


if __name__ == "__main__":
    main()