#!/usr/bin/env python3
"""
Universal Integration Setup for Multi-Agent Squad
Handles all integration types with user permission at each step
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

class IntegrationManager:
    def __init__(self):
        self.config_dir = Path(".claude/integrations")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Import integration modules
        self.integrations = {
            "slack": "Slack notifications",
            "email": "Email notifications", 
            "discord": "Discord webhooks",
            "teams": "Microsoft Teams",
            "github": "GitHub issues/PRs",
            "jira": "Jira tickets",
            "linear": "Linear issues",
            "notion": "Notion pages",
            "confluence": "Confluence docs",
            "webhook": "Custom webhooks",
            "mcp_servers": "MCP Protocol servers",
            "agile_tools": "Agile development tools"
        }
        
    def interactive_setup(self) -> None:
        """Main interactive setup flow"""
        print("\n🔌 Integration Setup")
        print("━" * 50)
        print("\nLet's connect your project to external services.")
        print("All integrations are optional and can be added later.\n")
        
        # Check existing integrations
        existing = self._check_existing_integrations()
        if existing:
            print("📋 Existing integrations:")
            for name in existing:
                print(f"  ✓ {name}")
            print()
            
        # Ask what they want to set up
        response = self._ask_user(
            "What would you like to do?",
            ["a", "b", "c"],
            {
                "a": "Set up new integration",
                "b": "Modify existing integration",
                "c": "Skip for now"
            }
        )
        
        if response == "c":
            print("✅ Skipping integrations. You can run this anytime with:")
            print("   python scripts/integration-setup.py")
            return
            
        if response == "a":
            self._setup_new_integration()
        elif response == "b":
            self._modify_existing_integration(existing)
            
    def _check_existing_integrations(self) -> List[str]:
        """Check which integrations are already configured"""
        existing = []
        for integration in self.integrations:
            config_file = self.config_dir / f"{integration}.json"
            if config_file.exists():
                existing.append(integration)
        return existing
        
    def _setup_new_integration(self) -> None:
        """Set up a new integration"""
        print("\n📌 Available Integrations:")
        
        options = {}
        option_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        
        for i, (key, desc) in enumerate(self.integrations.items()):
            if i < len(option_keys):
                options[option_keys[i]] = (key, desc)
                print(f"  {option_keys[i]}) {desc}")
                
        print(f"  x) Go back")
        
        choice = input("\nSelect integration: ").strip().lower()
        
        if choice == 'x':
            return
            
        if choice in options:
            integration_type = options[choice][0]
            self._run_integration_setup(integration_type)
            
            # Ask if they want to set up another
            another = self._ask_user(
                "\nSet up another integration?",
                ["y", "n"],
                {"y": "Yes", "n": "No, I'm done"}
            )
            
            if another == "y":
                self._setup_new_integration()
                
    def _modify_existing_integration(self, existing: List[str]) -> None:
        """Modify an existing integration"""
        print("\n📌 Select integration to modify:")
        
        for i, name in enumerate(existing):
            print(f"  {i+1}) {name}")
            
        choice = input("\nEnter number: ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(existing):
                integration = existing[idx]
                
                action = self._ask_user(
                    f"\nWhat would you like to do with {integration}?",
                    ["a", "b", "c"],
                    {
                        "a": "Reconfigure",
                        "b": "Remove",
                        "c": "Cancel"
                    }
                )
                
                if action == "a":
                    self._run_integration_setup(integration)
                elif action == "b":
                    self._remove_integration(integration)
        except:
            print("Invalid selection")
            
    def _run_integration_setup(self, integration_type: str) -> None:
        """Run the setup for a specific integration"""
        print(f"\n🔧 Setting up {self.integrations[integration_type]}...")
        
        # Run the appropriate setup script
        script_map = {
            "slack": "slack-integration.py",
            "email": "email-integration.py",
            "discord": "discord-integration.py",
            "teams": "teams-integration.py",
            "github": "github-integration.py",
            "jira": "jira-integration.py",
            "linear": "linear-integration.py",
            "notion": "notion-integration.py",
            "confluence": "confluence-integration.py",
            "webhook": "webhook-integration.py",
            "mcp_servers": "mcp-server-setup.py",
            "agile_tools": "agile-tools-setup.py"
        }
        
        script = script_map.get(integration_type)
        if script:
            script_path = Path("scripts") / script
            
            if script_path.exists():
                import subprocess
                subprocess.run([sys.executable, str(script_path)])
            else:
                # For integrations we haven't created yet, use generic setup
                self._generic_integration_setup(integration_type)
                
    def _generic_integration_setup(self, integration_type: str) -> None:
        """Generic setup for integrations without specific scripts"""
        print(f"\n📋 Generic {integration_type} Setup")
        print("This integration requires manual configuration.")
        
        config = {
            "type": integration_type,
            "enabled": True,
            "created_at": "2025-08-01T10:00:00Z"
        }
        
        if integration_type == "discord":
            webhook = input("\nEnter Discord webhook URL: ").strip()
            if webhook:
                config["webhook_url"] = webhook
                
        elif integration_type == "teams":
            webhook = input("\nEnter Microsoft Teams webhook URL: ").strip()
            if webhook:
                config["webhook_url"] = webhook
                
        elif integration_type == "webhook":
            url = input("\nEnter webhook URL: ").strip()
            method = input("HTTP method (POST/GET) [POST]: ").strip() or "POST"
            config.update({
                "url": url,
                "method": method.upper()
            })
            
        # Save configuration
        if len(config) > 3:  # More than just the base fields
            config_path = self.config_dir / f"{integration_type}.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ {integration_type} integration configured!")
        else:
            print("❌ Configuration cancelled.")
            
    def _remove_integration(self, integration: str) -> None:
        """Remove an integration"""
        confirm = self._ask_user(
            f"\nAre you sure you want to remove {integration}?",
            ["y", "n"],
            {"y": "Yes, remove it", "n": "No, keep it"}
        )
        
        if confirm == "y":
            config_path = self.config_dir / f"{integration}.json"
            hooks_path = Path(".claude/hooks") / f"{integration}-notifications.toml"
            
            if config_path.exists():
                config_path.unlink()
            if hooks_path.exists():
                hooks_path.unlink()
                
            print(f"✅ {integration} integration removed.")
            
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
            
    def check_critical_decision(self, decision_type: str, context: Dict) -> bool:
        """Check if user approval is needed for a critical decision"""
        critical_decisions = [
            "deploy_to_production",
            "delete_data",
            "modify_production_config",
            "merge_to_main",
            "create_public_endpoint",
            "modify_security_settings",
            "execute_migration",
            "modify_user_permissions"
        ]
        
        if decision_type in critical_decisions:
            print(f"\n⚠️  CRITICAL DECISION: {decision_type}")
            print("━" * 50)
            print(f"Context: {json.dumps(context, indent=2)}")
            
            approval = self._ask_user(
                "Do you approve this action?",
                ["y", "n"],
                {"y": "Yes, proceed", "n": "No, cancel"}
            )
            
            return approval == "y"
            
        return True  # Non-critical decisions proceed automatically


def main():
    """Main entry point"""
    manager = IntegrationManager()
    
    if len(sys.argv) > 1:
        # Handle specific commands
        if sys.argv[1] == "check":
            # Check existing integrations
            existing = manager._check_existing_integrations()
            if existing:
                print("Active integrations:")
                for name in existing:
                    print(f"  ✓ {name}")
            else:
                print("No integrations configured yet.")
                
        elif sys.argv[1] in manager.integrations:
            # Set up specific integration
            manager._run_integration_setup(sys.argv[1])
            
    else:
        # Interactive setup
        manager.interactive_setup()


if __name__ == "__main__":
    main()