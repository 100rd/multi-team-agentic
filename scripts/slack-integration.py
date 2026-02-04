#!/usr/bin/env python3
"""
Slack Integration Setup for Multi-Agent Squad
Interactive setup with user permission at each step
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Optional, List

class SlackIntegration:
    def __init__(self):
        self.config_dir = Path(".claude/integrations")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.hooks_dir = Path(".claude/hooks")
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        
    def interactive_setup(self) -> bool:
        """Interactive Slack setup with user permission at each step"""
        print("\n🔷 Slack Integration Setup")
        print("━" * 50)
        print("\nThis will help you set up Slack notifications for your project.")
        print("You can use this for:")
        print("  • Build status notifications")
        print("  • Daily standup reminders")
        print("  • PR/Code review alerts")
        print("  • Deployment notifications")
        print("  • Custom project events\n")
        
        # Ask for permission to proceed
        response = self._ask_user(
            "Would you like to set up Slack integration?",
            ["y", "n"],
            {"y": "Yes, set up Slack", "n": "No, skip for now"}
        )
        
        if response == "n":
            print("✅ Skipping Slack integration. You can set this up later if needed.")
            return False
            
        # Get Slack webhook URL
        print("\n📌 Step 1: Slack Webhook URL")
        print("To send notifications to Slack, we need a webhook URL.")
        print("You can create one at: https://api.slack.com/apps")
        print("Or use an existing webhook if you have one.\n")
        
        webhook_url = input("Enter your Slack webhook URL (or 'skip' to cancel): ").strip()
        if webhook_url.lower() == 'skip':
            print("✅ Skipping Slack integration.")
            return False
            
        # Ask which notifications they want
        print("\n📌 Step 2: Notification Types")
        print("What types of notifications would you like?\n")
        
        notifications = self._select_notifications()
        
        # Ask about notification preferences
        print("\n📌 Step 3: Notification Preferences")
        
        prefs = self._get_notification_preferences()
        
        # Show summary and ask for confirmation
        print("\n📋 Configuration Summary")
        print("━" * 50)
        print(f"Webhook URL: {webhook_url[:50]}...")
        print(f"Notifications: {', '.join(notifications)}")
        print(f"Thread messages: {'Yes' if prefs['thread_messages'] else 'No'}")
        print(f"Include user mentions: {'Yes' if prefs['include_mentions'] else 'No'}")
        print(f"Error notifications only: {'Yes' if prefs['errors_only'] else 'No'}")
        
        confirm = self._ask_user(
            "\nProceed with this configuration?",
            ["y", "n"],
            {"y": "Yes, create integration", "n": "No, cancel"}
        )
        
        if confirm == "n":
            print("❌ Slack integration cancelled.")
            return False
            
        # Create configuration
        self._create_slack_config(webhook_url, notifications, prefs)
        
        # Generate hooks
        self._generate_slack_hooks(notifications, prefs)
        
        print("\n✅ Slack integration configured successfully!")
        print("📄 Configuration saved to: .claude/integrations/slack.json")
        print("🪝 Hooks created in: .claude/hooks/slack-notifications.toml")
        print("\nYou can test the integration by running:")
        print("  python scripts/slack-integration.py test")
        
        return True
        
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
            
    def _select_notifications(self) -> List[str]:
        """Let user select which notifications they want"""
        notification_types = {
            "a": ("Build Status", "build_status"),
            "b": ("Test Results", "test_results"),
            "c": ("Daily Standup", "daily_standup"),
            "d": ("PR Reviews", "pr_reviews"),
            "e": ("Deployments", "deployments"),
            "f": ("Error Alerts", "error_alerts"),
            "g": ("Sprint Updates", "sprint_updates"),
            "h": ("Custom Events", "custom_events")
        }
        
        print("Select notification types (you can choose multiple):")
        for key, (name, _) in notification_types.items():
            print(f"  {key}) {name}")
        print("\nEnter your choices separated by commas (e.g., a,c,d)")
        print("Or press Enter for defaults (build, test, errors): ", end="")
        
        choices = input().strip()
        if not choices:
            return ["build_status", "test_results", "error_alerts"]
            
        selected = []
        for choice in choices.split(","):
            choice = choice.strip().lower()
            if choice in notification_types:
                selected.append(notification_types[choice][1])
                
        return selected if selected else ["build_status", "test_results", "error_alerts"]
        
    def _get_notification_preferences(self) -> Dict[str, bool]:
        """Get user preferences for notifications"""
        prefs = {}
        
        # Thread messages
        thread = self._ask_user(
            "Thread related messages together?",
            ["y", "n"],
            {"y": "Yes, use threads", "n": "No, separate messages"}
        )
        prefs['thread_messages'] = thread == "y"
        
        # Mentions
        mentions = self._ask_user(
            "Include @here or @channel mentions for critical alerts?",
            ["y", "n"],
            {"y": "Yes, include mentions", "n": "No mentions"}
        )
        prefs['include_mentions'] = mentions == "y"
        
        # Errors only
        errors = self._ask_user(
            "Only send notifications for errors/failures?",
            ["y", "n"],
            {"y": "Errors only", "n": "All events"}
        )
        prefs['errors_only'] = errors == "y"
        
        return prefs
        
    def _create_slack_config(self, webhook_url: str, notifications: List[str], prefs: Dict[str, bool]) -> None:
        """Create Slack configuration file"""
        config = {
            "webhook_url": webhook_url,
            "enabled_notifications": notifications,
            "preferences": prefs,
            "created_at": "2025-08-01T10:00:00Z"
        }
        
        config_path = self.config_dir / "slack.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        # Also create a .env.slack file for the webhook (more secure)
        env_path = Path(".env.slack")
        with open(env_path, 'w') as f:
            f.write(f"SLACK_WEBHOOK_URL={webhook_url}\n")
            
        # Add to .gitignore
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            with open(gitignore_path, 'a') as f:
                if ".env.slack" not in open(gitignore_path).read():
                    f.write("\n# Slack integration\n.env.slack\n")
                    
    def _generate_slack_hooks(self, notifications: List[str], prefs: Dict[str, bool]) -> None:
        """Generate Claude Code hooks for Slack notifications"""
        hooks_content = """# Slack Notification Hooks
# Auto-generated based on your preferences

"""
        
        # Build status notifications
        if "build_status" in notifications:
            hooks_content += """[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Bash"
args_regex = "npm run build|yarn build|make|cargo build"
command = '''
status=$?
if [ $status -eq 0 ]; then
    [ "{errors_only}" != "True" ] && python scripts/slack-notify.py "✅ Build succeeded"
else
    python scripts/slack-notify.py "❌ Build failed" --mention
fi
'''

""".format(errors_only=prefs['errors_only'])
        
        # Test result notifications
        if "test_results" in notifications:
            hooks_content += """[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Bash"
args_regex = "npm test|yarn test|pytest|cargo test"
command = '''
status=$?
if [ $status -eq 0 ]; then
    [ "{errors_only}" != "True" ] && python scripts/slack-notify.py "✅ Tests passed"
else
    python scripts/slack-notify.py "❌ Tests failed" --mention
fi
'''

""".format(errors_only=prefs['errors_only'])
        
        # Daily standup reminder
        if "daily_standup" in notifications:
            hooks_content += """[[hooks]]
event = "Notification"
[hooks.matcher]
time = "09:00"
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
command = '''
python scripts/slack-notify.py "🏃 Daily Standup Reminder" --template standup
'''

"""
        
        # PR review notifications
        if "pr_reviews" in notifications:
            hooks_content += """[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Bash"
args_regex = "gh pr create"
command = '''
python scripts/slack-notify.py "🔍 New PR ready for review" --template pr_created
'''

"""
        
        # Error alerts
        if "error_alerts" in notifications:
            hooks_content += """[[hooks]]
event = "PostToolUse"
run_in_background = true
[hooks.matcher]
tool_name = "Bash"
command = '''
# Check for common error patterns in output
if echo "$CLAUDE_OUTPUT" | grep -qiE "(error|failed|exception|fatal)"; then
    python scripts/slack-notify.py "⚠️ Error detected in command output" --error "$CLAUDE_OUTPUT"
fi
'''

"""
        
        hooks_path = self.hooks_dir / "slack-notifications.toml"
        with open(hooks_path, 'w') as f:
            f.write(hooks_content)
            
        # Create the notification script
        self._create_notification_script()
        
    def _create_notification_script(self) -> None:
        """Create the slack-notify.py script"""
        script_content = '''#!/usr/bin/env python3
"""Send notifications to Slack"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path

def load_config():
    """Load Slack configuration"""
    config_path = Path(".claude/integrations/slack.json")
    if not config_path.exists():
        print("Error: Slack not configured. Run: python scripts/slack-integration.py")
        sys.exit(1)
        
    with open(config_path) as f:
        config = json.load(f)
        
    # Load webhook from env file
    env_path = Path(".env.slack")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("SLACK_WEBHOOK_URL="):
                    config['webhook_url'] = line.split("=", 1)[1].strip()
                    
    return config

def send_message(message, mention=False, template=None, error=None):
    """Send message to Slack"""
    config = load_config()
    
    # Build payload
    payload = {"text": message}
    
    if config['preferences'].get('include_mentions') and mention:
        payload['text'] = f"<!here> {message}"
        
    # Apply templates
    if template == "standup":
        payload['blocks'] = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": message}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Questions for standup:*\\n• What did you complete yesterday?\\n• What will you work on today?\\n• Any blockers?"
                }
            }
        ]
    elif template == "pr_created":
        payload['blocks'] = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": message}
            }
        ]
        
    if error:
        # Truncate error if too long
        if len(error) > 500:
            error = error[:500] + "..."
        payload['attachments'] = [
            {
                "color": "danger",
                "text": f"```{error}```"
            }
        ]
    
    # Send to Slack
    response = requests.post(config['webhook_url'], json=payload)
    if response.status_code != 200:
        print(f"Failed to send Slack notification: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Message to send")
    parser.add_argument("--mention", action="store_true", help="Include @here mention")
    parser.add_argument("--template", help="Use message template")
    parser.add_argument("--error", help="Error details to include")
    
    args = parser.parse_args()
    send_message(args.message, args.mention, args.template, args.error)
'''
        
        script_path = Path("scripts/slack-notify.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
    def test_integration(self) -> None:
        """Test the Slack integration"""
        print("\n🧪 Testing Slack integration...")
        
        try:
            import subprocess
            result = subprocess.run(
                ["python", "scripts/slack-notify.py", "🎉 Slack integration test successful!"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Test message sent successfully!")
                print("Check your Slack channel for the test message.")
            else:
                print(f"❌ Test failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Test failed: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        integration = SlackIntegration()
        integration.test_integration()
    else:
        integration = SlackIntegration()
        integration.interactive_setup()


if __name__ == "__main__":
    main()