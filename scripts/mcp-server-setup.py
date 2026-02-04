#!/usr/bin/env python3
"""
MCP Server Setup for Multi-Agent Squad
Configures Model Context Protocol servers for enhanced agile development
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

class MCPServerSetup:
    def __init__(self):
        self.config_dir = Path(".claude/mcp")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Available MCP servers for agile development
        self.mcp_servers = {
            "database": {
                "name": "PostgreSQL Explorer",
                "description": "Query and explore your project database",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"],
                "env": {"DATABASE_URL": "${DATABASE_URL}"}
            },
            "github": {
                "name": "GitHub Integration",
                "description": "Manage issues, PRs, and repositories",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"}
            },
            "jira": {
                "name": "Jira Integration",
                "description": "Manage Jira tickets and sprints",
                "command": "python",
                "args": ["scripts/mcp-servers/jira-server.py"],
                "env": {
                    "JIRA_URL": "${JIRA_URL}",
                    "JIRA_EMAIL": "${JIRA_EMAIL}",
                    "JIRA_TOKEN": "${JIRA_TOKEN}"
                }
            },
            "slack": {
                "name": "Slack Integration",
                "description": "Send messages and read channels",
                "command": "python",
                "args": ["scripts/mcp-servers/slack-server.py"],
                "env": {"SLACK_TOKEN": "${SLACK_TOKEN}"}
            },
            "linear": {
                "name": "Linear Integration",
                "description": "Manage Linear issues and projects",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-linear"],
                "env": {"LINEAR_API_KEY": "${LINEAR_API_KEY}"}
            },
            "notion": {
                "name": "Notion Integration",
                "description": "Access Notion pages and databases",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-notion"],
                "env": {"NOTION_TOKEN": "${NOTION_TOKEN}"}
            },
            "confluence": {
                "name": "Confluence Integration",
                "description": "Read and update documentation",
                "command": "python",
                "args": ["scripts/mcp-servers/confluence-server.py"],
                "env": {
                    "CONFLUENCE_URL": "${CONFLUENCE_URL}",
                    "CONFLUENCE_TOKEN": "${CONFLUENCE_TOKEN}"
                }
            },
            "memory": {
                "name": "Project Memory",
                "description": "Remember context across sessions",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-memory"]
            },
            "filesystem": {
                "name": "Enhanced Filesystem",
                "description": "Advanced file operations",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "config": {
                    "directories": [
                        {"path": ".", "access": "read-write"},
                        {"path": "/tmp", "access": "read-write"}
                    ]
                }
            },
            "docker": {
                "name": "Docker Management",
                "description": "Manage containers and images",
                "command": "python",
                "args": ["scripts/mcp-servers/docker-server.py"]
            },
            "kubernetes": {
                "name": "Kubernetes Management",
                "description": "Manage K8s deployments",
                "command": "python",
                "args": ["scripts/mcp-servers/k8s-server.py"],
                "env": {"KUBECONFIG": "${KUBECONFIG}"}
            },
            "analytics": {
                "name": "Analytics Dashboard",
                "description": "Project metrics and insights",
                "command": "python",
                "args": ["scripts/mcp-servers/analytics-server.py"]
            },
            "testrunner": {
                "name": "Test Runner",
                "description": "Execute and monitor tests",
                "command": "python",
                "args": ["scripts/mcp-servers/test-server.py"]
            },
            "monitoring": {
                "name": "Monitoring Integration",
                "description": "Access logs and metrics",
                "command": "python",
                "args": ["scripts/mcp-servers/monitoring-server.py"],
                "env": {
                    "DATADOG_API_KEY": "${DATADOG_API_KEY}",
                    "PROMETHEUS_URL": "${PROMETHEUS_URL}"
                }
            }
        }
        
    def interactive_setup(self) -> None:
        """Interactive MCP server setup"""
        print("\n🔌 MCP Server Setup")
        print("━" * 50)
        print("\nModel Context Protocol (MCP) servers extend Claude's capabilities")
        print("by connecting to external tools and services.\n")
        
        # Check existing servers
        existing = self._check_existing_servers()
        if existing:
            print("📋 Configured MCP servers:")
            for name in existing:
                print(f"  ✓ {name}")
            print()
            
        # Ask what they want to configure
        response = self._ask_user(
            "What would you like to do?",
            ["a", "b", "c"],
            {
                "a": "Add MCP servers for this project",
                "b": "View available servers",
                "c": "Skip for now"
            }
        )
        
        if response == "c":
            print("✅ Skipping MCP setup. You can run this anytime with:")
            print("   python scripts/mcp-server-setup.py")
            return
            
        if response == "b":
            self._show_available_servers()
            self.interactive_setup()  # Go back to menu
            return
            
        # Add servers
        self._add_mcp_servers()
        
    def _check_existing_servers(self) -> List[str]:
        """Check which MCP servers are configured"""
        config_file = Path(".vscode/mcp.json")
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                return list(config.get("mcpServers", {}).keys())
        return []
        
    def _show_available_servers(self) -> None:
        """Show all available MCP servers"""
        print("\n📚 Available MCP Servers:")
        print("━" * 50)
        
        categories = {
            "Project Management": ["github", "jira", "linear", "notion", "confluence"],
            "Communication": ["slack"],
            "Development": ["database", "filesystem", "memory", "testrunner"],
            "DevOps": ["docker", "kubernetes", "monitoring"],
            "Analytics": ["analytics"]
        }
        
        for category, servers in categories.items():
            print(f"\n{category}:")
            for server_id in servers:
                if server_id in self.mcp_servers:
                    server = self.mcp_servers[server_id]
                    print(f"  • {server['name']}: {server['description']}")
                    
    def _add_mcp_servers(self) -> None:
        """Add MCP servers based on project needs"""
        print("\n📌 Let's configure MCP servers for your project.")
        print("I'll suggest servers based on your project type.\n")
        
        # Ask about project management
        pm_response = self._ask_user(
            "What project management tool do you use?",
            ["a", "b", "c", "d", "e", "f"],
            {
                "a": "GitHub Issues",
                "b": "Jira",
                "c": "Linear",
                "d": "Notion",
                "e": "None",
                "f": "Multiple tools"
            }
        )
        
        selected_servers = ["memory", "filesystem"]  # Always include these
        
        # Add project management servers
        if pm_response == "a":
            selected_servers.append("github")
        elif pm_response == "b":
            selected_servers.append("jira")
        elif pm_response == "c":
            selected_servers.append("linear")
        elif pm_response == "d":
            selected_servers.append("notion")
        elif pm_response == "f":
            # Let them select multiple
            print("\nSelect all that apply (comma-separated):")
            print("  1) GitHub Issues")
            print("  2) Jira")
            print("  3) Linear")
            print("  4) Notion")
            choices = input("Enter numbers: ").strip()
            
            pm_map = {"1": "github", "2": "jira", "3": "linear", "4": "notion"}
            for choice in choices.split(","):
                if choice.strip() in pm_map:
                    selected_servers.append(pm_map[choice.strip()])
                    
        # Ask about communication
        comm_response = self._ask_user(
            "\nDo you use Slack for team communication?",
            ["y", "n"],
            {"y": "Yes", "n": "No"}
        )
        
        if comm_response == "y":
            selected_servers.append("slack")
            
        # Ask about documentation
        doc_response = self._ask_user(
            "\nDo you use Confluence for documentation?",
            ["y", "n"],
            {"y": "Yes", "n": "No"}
        )
        
        if doc_response == "y":
            selected_servers.append("confluence")
            
        # Ask about database
        db_response = self._ask_user(
            "\nDoes your project use a PostgreSQL database?",
            ["y", "n"],
            {"y": "Yes", "n": "No"}
        )
        
        if db_response == "y":
            selected_servers.append("database")
            
        # Ask about DevOps
        devops_response = self._ask_user(
            "\nDo you use containerization?",
            ["a", "b", "c"],
            {
                "a": "Docker",
                "b": "Kubernetes",
                "c": "No"
            }
        )
        
        if devops_response == "a":
            selected_servers.append("docker")
        elif devops_response == "b":
            selected_servers.extend(["docker", "kubernetes"])
            
        # Ask about testing
        test_response = self._ask_user(
            "\nWould you like automated test execution?",
            ["y", "n"],
            {"y": "Yes", "n": "No"}
        )
        
        if test_response == "y":
            selected_servers.append("testrunner")
            
        # Ask about monitoring
        monitor_response = self._ask_user(
            "\nDo you have monitoring/observability tools?",
            ["y", "n"],
            {"y": "Yes", "n": "No"}
        )
        
        if monitor_response == "y":
            selected_servers.append("monitoring")
            
        # Show summary
        print("\n📋 Selected MCP Servers:")
        print("━" * 50)
        for server_id in selected_servers:
            if server_id in self.mcp_servers:
                print(f"  • {self.mcp_servers[server_id]['name']}")
                
        # Confirm
        confirm = self._ask_user(
            "\nProceed with this configuration?",
            ["y", "n"],
            {"y": "Yes", "n": "No, let me customize"}
        )
        
        if confirm == "n":
            selected_servers = self._custom_select_servers()
            
        # Configure servers
        self._configure_servers(selected_servers)
        
    def _custom_select_servers(self) -> List[str]:
        """Let user manually select servers"""
        print("\n📌 Select MCP servers (comma-separated numbers):")
        
        server_list = list(self.mcp_servers.keys())
        for i, server_id in enumerate(server_list):
            server = self.mcp_servers[server_id]
            print(f"  {i+1}) {server['name']}: {server['description']}")
            
        choices = input("\nEnter numbers: ").strip()
        selected = []
        
        for choice in choices.split(","):
            try:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(server_list):
                    selected.append(server_list[idx])
            except:
                pass
                
        return selected
        
    def _configure_servers(self, server_ids: List[str]) -> None:
        """Configure the selected MCP servers"""
        print("\n🔧 Configuring MCP servers...")
        
        # Create .vscode directory if needed
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        # Build MCP configuration
        mcp_config = {
            "mcpServers": {}
        }
        
        # Environment variables needed
        env_vars = {}
        
        for server_id in server_ids:
            if server_id not in self.mcp_servers:
                continue
                
            server = self.mcp_servers[server_id]
            server_config = {
                "command": server["command"],
                "args": server["args"]
            }
            
            # Add environment variables
            if "env" in server:
                server_config["env"] = server["env"]
                for key, value in server["env"].items():
                    if value.startswith("${") and value.endswith("}"):
                        env_key = value[2:-1]
                        env_vars[env_key] = f"Your {server['name']} {env_key}"
                        
            # Add config if present
            if "config" in server:
                server_config["config"] = server["config"]
                
            mcp_config["mcpServers"][server_id] = server_config
            
        # Write MCP configuration
        mcp_file = vscode_dir / "mcp.json"
        with open(mcp_file, 'w') as f:
            json.dump(mcp_config, f, indent=2)
            
        print(f"✅ Created MCP configuration: {mcp_file}")
        
        # Create environment template if needed
        if env_vars:
            self._create_env_template(env_vars)
            
        # Create server implementations that don't exist yet
        self._create_server_implementations(server_ids)
        
        print("\n✅ MCP server setup complete!")
        print("\nNext steps:")
        print("1. Set up required environment variables in .env.mcp")
        print("2. Restart Claude Code to load the MCP servers")
        print("3. Use @ mentions to access MCP server capabilities")
        
    def _create_env_template(self, env_vars: Dict[str, str]) -> None:
        """Create environment variable template"""
        print("\n📝 Creating environment template...")
        
        env_file = Path(".env.mcp.template")
        with open(env_file, 'w') as f:
            f.write("# MCP Server Environment Variables\n")
            f.write("# Copy this to .env.mcp and fill in your values\n\n")
            
            for key, description in env_vars.items():
                f.write(f"# {description}\n")
                f.write(f"{key}=\n\n")
                
        print(f"✅ Created environment template: {env_file}")
        print("   Copy to .env.mcp and add your credentials")
        
        # Add to .gitignore
        gitignore = Path(".gitignore")
        if gitignore.exists():
            with open(gitignore, 'a') as f:
                if ".env.mcp" not in open(gitignore).read():
                    f.write("\n# MCP Server credentials\n.env.mcp\n")
                    
    def _create_server_implementations(self, server_ids: List[str]) -> None:
        """Create placeholder implementations for custom servers"""
        custom_servers = ["jira", "slack", "confluence", "docker", "kubernetes", 
                         "analytics", "testrunner", "monitoring"]
        
        servers_dir = Path("scripts/mcp-servers")
        servers_dir.mkdir(parents=True, exist_ok=True)
        
        for server_id in server_ids:
            if server_id in custom_servers:
                server_file = servers_dir / f"{server_id}-server.py"
                if not server_file.exists():
                    self._create_server_template(server_id, server_file)
                    
    def _create_server_template(self, server_id: str, file_path: Path) -> None:
        """Create a template MCP server implementation"""
        template = f'''#!/usr/bin/env python3
"""
{self.mcp_servers[server_id]['name']} MCP Server
{self.mcp_servers[server_id]['description']}
"""

import os
import sys
import json
import asyncio
from typing import Dict, List, Any

# MCP Server implementation for {server_id}
# This is a template - implement the actual functionality

class {server_id.title()}MCPServer:
    def __init__(self):
        self.name = "{server_id}"
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        
        if method == "list_tools":
            return self.list_tools()
        elif method == "execute_tool":
            return await self.execute_tool(request.get("params", {{}}))
        else:
            return {{"error": f"Unknown method: {{method}}"}}
            
    def list_tools(self) -> Dict[str, Any]:
        """List available tools for this server"""
        return {{
            "tools": [
                {{
                    "name": "{server_id}_example",
                    "description": "Example tool for {server_id}",
                    "parameters": {{
                        "type": "object",
                        "properties": {{
                            "query": {{
                                "type": "string",
                                "description": "Query parameter"
                            }}
                        }}
                    }}
                }}
            ]
        }}
        
    async def execute_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given parameters"""
        tool_name = params.get("name")
        tool_params = params.get("parameters", {{}})
        
        if tool_name == "{server_id}_example":
            # Implement your tool logic here
            return {{
                "result": f"Executed {{tool_name}} with params: {{tool_params}}"
            }}
        else:
            return {{"error": f"Unknown tool: {{tool_name}}"}}
            
            
async def main():
    """Main entry point for MCP server"""
    server = {server_id.title()}MCPServer()
    
    # Simple stdio-based MCP server
    while True:
        try:
            line = input()
            request = json.loads(line)
            response = await server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except EOFError:
            break
        except Exception as e:
            error_response = {{"error": str(e)}}
            print(json.dumps(error_response))
            sys.stdout.flush()
            

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        with open(file_path, 'w') as f:
            f.write(template)
        os.chmod(file_path, 0o755)
        
        print(f"   Created template: {file_path}")
        
    def _ask_user(self, question: str, options: List[str], descriptions: Dict[str, str]) -> str:
        """Ask user a question with keyboard-selectable options"""
        print(f"\n{question}")
        for opt in options:
            print(f"  {opt}) {descriptions[opt]}")
        
        while True:
            response = input(f"\nPress {', '.join(options)}: ").strip().lower()
            if response in options:
                return response
            print(f"Please enter one of: {', '.join(options)}")


def main():
    """Main entry point"""
    setup = MCPServerSetup()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            setup._show_available_servers()
        elif sys.argv[1] == "check":
            existing = setup._check_existing_servers()
            if existing:
                print("Configured MCP servers:")
                for name in existing:
                    print(f"  ✓ {name}")
            else:
                print("No MCP servers configured yet.")
    else:
        setup.interactive_setup()


if __name__ == "__main__":
    main()