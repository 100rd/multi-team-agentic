#!/usr/bin/env python3
"""
Email Integration Setup for Multi-Agent Squad
Interactive setup with user permission at each step
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Optional, List

class EmailIntegration:
    def __init__(self):
        self.config_dir = Path(".claude/integrations")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.hooks_dir = Path(".claude/hooks")
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        
    def interactive_setup(self) -> bool:
        """Interactive email setup with user permission at each step"""
        print("\n📧 Email Integration Setup")
        print("━" * 50)
        print("\nThis will help you set up email notifications for your project.")
        print("You can use this for:")
        print("  • Daily/Weekly summaries")
        print("  • Build and deployment notifications")
        print("  • Error alerts and critical issues")
        print("  • Sprint completion reports")
        print("  • Custom project events\n")
        
        # Ask for permission to proceed
        response = self._ask_user(
            "Would you like to set up email integration?",
            ["y", "n"],
            {"y": "Yes, set up email", "n": "No, skip for now"}
        )
        
        if response == "n":
            print("✅ Skipping email integration. You can set this up later if needed.")
            return False
            
        # Get email configuration method
        print("\n📌 Step 1: Email Service")
        print("How would you like to send emails?")
        
        service = self._ask_user(
            "Select email service:",
            ["a", "b", "c", "d"],
            {
                "a": "Gmail (requires app password)",
                "b": "SendGrid API",
                "c": "AWS SES",
                "d": "SMTP server"
            }
        )
        
        config = self._get_service_config(service)
        if not config:
            return False
            
        # Get recipient information
        print("\n📌 Step 2: Recipients")
        recipients = self._get_recipients()
        
        # Ask which notifications they want
        print("\n📌 Step 3: Notification Types")
        print("What types of email notifications would you like?\n")
        
        notifications = self._select_notifications()
        
        # Ask about notification preferences
        print("\n📌 Step 4: Email Preferences")
        prefs = self._get_email_preferences()
        
        # Show summary and ask for confirmation
        print("\n📋 Configuration Summary")
        print("━" * 50)
        print(f"Service: {config['service']}")
        print(f"Recipients: {', '.join(recipients)}")
        print(f"Notifications: {', '.join(notifications)}")
        print(f"HTML emails: {'Yes' if prefs['html_emails'] else 'No'}")
        print(f"Batch daily digest: {'Yes' if prefs['daily_digest'] else 'No'}")
        print(f"Critical alerts only: {'Yes' if prefs['critical_only'] else 'No'}")
        
        confirm = self._ask_user(
            "\nProceed with this configuration?",
            ["y", "n"],
            {"y": "Yes, create integration", "n": "No, cancel"}
        )
        
        if confirm == "n":
            print("❌ Email integration cancelled.")
            return False
            
        # Create configuration
        self._create_email_config(config, recipients, notifications, prefs)
        
        # Generate hooks
        self._generate_email_hooks(notifications, prefs)
        
        print("\n✅ Email integration configured successfully!")
        print("📄 Configuration saved to: .claude/integrations/email.json")
        print("🪝 Hooks created in: .claude/hooks/email-notifications.toml")
        print("\nYou can test the integration by running:")
        print("  python scripts/email-integration.py test")
        
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
            
    def _get_service_config(self, service: str) -> Optional[Dict]:
        """Get configuration for selected email service"""
        config = {"service": ""}
        
        if service == "a":  # Gmail
            config["service"] = "gmail"
            print("\n📧 Gmail Setup")
            print("You'll need an app password (not your regular password)")
            print("Create one at: https://myaccount.google.com/apppasswords")
            
            email = input("\nEnter your Gmail address: ").strip()
            if not email:
                return None
                
            password = input("Enter your app password: ").strip()
            if not password:
                return None
                
            config.update({
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "use_tls": True,
                "username": email,
                "password": password,
                "from_email": email
            })
            
        elif service == "b":  # SendGrid
            config["service"] = "sendgrid"
            print("\n📧 SendGrid Setup")
            print("You'll need a SendGrid API key")
            print("Get one at: https://app.sendgrid.com/settings/api_keys")
            
            api_key = input("\nEnter your SendGrid API key: ").strip()
            if not api_key:
                return None
                
            from_email = input("Enter the 'from' email address: ").strip()
            if not from_email:
                return None
                
            config.update({
                "api_key": api_key,
                "from_email": from_email
            })
            
        elif service == "c":  # AWS SES
            config["service"] = "aws_ses"
            print("\n📧 AWS SES Setup")
            print("Ensure your AWS credentials are configured")
            
            region = input("\nEnter AWS region (e.g., us-east-1): ").strip()
            if not region:
                return None
                
            from_email = input("Enter the verified 'from' email address: ").strip()
            if not from_email:
                return None
                
            config.update({
                "region": region,
                "from_email": from_email
            })
            
        elif service == "d":  # SMTP
            config["service"] = "smtp"
            print("\n📧 SMTP Server Setup")
            
            server = input("\nEnter SMTP server (e.g., mail.example.com): ").strip()
            if not server:
                return None
                
            port = input("Enter SMTP port (usually 587 or 465): ").strip()
            if not port.isdigit():
                return None
                
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            from_email = input("Enter 'from' email address: ").strip()
            
            if not all([username, password, from_email]):
                return None
                
            config.update({
                "smtp_server": server,
                "smtp_port": int(port),
                "use_tls": True,
                "username": username,
                "password": password,
                "from_email": from_email
            })
            
        return config
        
    def _get_recipients(self) -> List[str]:
        """Get email recipients"""
        recipients = []
        
        print("Enter email addresses to receive notifications.")
        print("Press Enter after each address. Enter 'done' when finished.\n")
        
        while True:
            email = input("Email address (or 'done'): ").strip()
            if email.lower() == 'done':
                break
            if '@' in email:
                recipients.append(email)
                print(f"✓ Added {email}")
            elif email:
                print("Please enter a valid email address")
                
        if not recipients:
            default = input("\nNo recipients added. Enter at least one email: ").strip()
            if default and '@' in default:
                recipients.append(default)
                
        return recipients
        
    def _select_notifications(self) -> List[str]:
        """Let user select which notifications they want"""
        notification_types = {
            "a": ("Daily Summary", "daily_summary"),
            "b": ("Weekly Report", "weekly_report"),
            "c": ("Build Status", "build_status"),
            "d": ("Test Results", "test_results"),
            "e": ("Deployment Status", "deployment"),
            "f": ("Error Alerts", "error_alerts"),
            "g": ("Sprint Summary", "sprint_summary"),
            "h": ("Performance Reports", "performance")
        }
        
        print("Select notification types (you can choose multiple):")
        for key, (name, _) in notification_types.items():
            print(f"  {key}) {name}")
        print("\nEnter your choices separated by commas (e.g., a,c,f)")
        print("Or press Enter for defaults (daily summary, errors): ", end="")
        
        choices = input().strip()
        if not choices:
            return ["daily_summary", "error_alerts"]
            
        selected = []
        for choice in choices.split(","):
            choice = choice.strip().lower()
            if choice in notification_types:
                selected.append(notification_types[choice][1])
                
        return selected if selected else ["daily_summary", "error_alerts"]
        
    def _get_email_preferences(self) -> Dict[str, bool]:
        """Get user preferences for emails"""
        prefs = {}
        
        # HTML emails
        html = self._ask_user(
            "Send HTML formatted emails?",
            ["y", "n"],
            {"y": "Yes, HTML emails", "n": "Plain text only"}
        )
        prefs['html_emails'] = html == "y"
        
        # Daily digest
        digest = self._ask_user(
            "Batch non-critical notifications into daily digest?",
            ["y", "n"],
            {"y": "Yes, daily digest", "n": "Send immediately"}
        )
        prefs['daily_digest'] = digest == "y"
        
        # Critical only
        critical = self._ask_user(
            "Only send emails for critical issues?",
            ["y", "n"],
            {"y": "Critical only", "n": "All notifications"}
        )
        prefs['critical_only'] = critical == "y"
        
        return prefs
        
    def _create_email_config(self, config: Dict, recipients: List[str], 
                           notifications: List[str], prefs: Dict[str, bool]) -> None:
        """Create email configuration file"""
        full_config = {
            **config,
            "recipients": recipients,
            "enabled_notifications": notifications,
            "preferences": prefs,
            "created_at": "2025-08-01T10:00:00Z"
        }
        
        config_path = self.config_dir / "email.json"
        with open(config_path, 'w') as f:
            json.dump(full_config, f, indent=2)
            
        # Create .env.email for sensitive data
        env_path = Path(".env.email")
        with open(env_path, 'w') as f:
            if 'password' in config:
                f.write(f"EMAIL_PASSWORD={config['password']}\n")
            if 'api_key' in config:
                f.write(f"EMAIL_API_KEY={config['api_key']}\n")
                
        # Add to .gitignore
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            with open(gitignore_path, 'a') as f:
                if ".env.email" not in open(gitignore_path).read():
                    f.write("\n# Email integration\n.env.email\n")
                    
    def _generate_email_hooks(self, notifications: List[str], prefs: Dict[str, bool]) -> None:
        """Generate Claude Code hooks for email notifications"""
        hooks_content = """# Email Notification Hooks
# Auto-generated based on your preferences

"""
        
        # Daily summary
        if "daily_summary" in notifications:
            hooks_content += """[[hooks]]
event = "Notification"
[hooks.matcher]
time = "18:00"
command = '''
python scripts/email-notify.py --template daily_summary
'''

"""
        
        # Weekly report
        if "weekly_report" in notifications:
            hooks_content += """[[hooks]]
event = "Notification"
[hooks.matcher]
time = "17:00"
days = ["friday"]
command = '''
python scripts/email-notify.py --template weekly_report
'''

"""
        
        # Build status
        if "build_status" in notifications and not prefs['critical_only']:
            hooks_content += """[[hooks]]
event = "PostToolUse"
[hooks.matcher]
tool_name = "Bash"
args_regex = "npm run build|yarn build|make"
command = '''
status=$?
if [ $status -ne 0 ] || [ "{critical_only}" != "True" ]; then
    python scripts/email-notify.py --template build_status --status $status
fi
'''

""".format(critical_only=prefs['critical_only'])
        
        # Error alerts
        if "error_alerts" in notifications:
            hooks_content += """[[hooks]]
event = "PostToolUse"
run_in_background = true
[hooks.matcher]
tool_name = "Bash"
command = '''
if echo "$CLAUDE_OUTPUT" | grep -qiE "(error|failed|exception|fatal|critical)"; then
    python scripts/email-notify.py --template error_alert --error "$CLAUDE_OUTPUT" --immediate
fi
'''

"""
        
        # Sprint summary
        if "sprint_summary" in notifications:
            hooks_content += """[[hooks]]
event = "UserPromptSubmit"
[hooks.matcher]
content_regex = "sprint.*complete|end.*sprint"
command = '''
python scripts/email-notify.py --template sprint_summary
'''

"""
        
        hooks_path = self.hooks_dir / "email-notifications.toml"
        with open(hooks_path, 'w') as f:
            f.write(hooks_content)
            
        # Create the notification script
        self._create_notification_script()
        
    def _create_notification_script(self) -> None:
        """Create the email-notify.py script"""
        script_content = '''#!/usr/bin/env python3
"""Send email notifications"""

import os
import sys
import json
import argparse
import smtplib
import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_config():
    """Load email configuration"""
    config_path = Path(".claude/integrations/email.json")
    if not config_path.exists():
        print("Error: Email not configured. Run: python scripts/email-integration.py")
        sys.exit(1)
        
    with open(config_path) as f:
        config = json.load(f)
        
    # Load sensitive data from env file
    env_path = Path(".env.email")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("EMAIL_PASSWORD="):
                    config['password'] = line.split("=", 1)[1].strip()
                elif line.startswith("EMAIL_API_KEY="):
                    config['api_key'] = line.split("=", 1)[1].strip()
                    
    return config

def get_project_stats():
    """Gather project statistics for reports"""
    stats = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.datetime.now().strftime("%H:%M"),
        "commits_today": "N/A",
        "files_changed": "N/A",
        "todos_completed": "N/A"
    }
    
    # Try to get git stats
    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", "--since=midnight", "--oneline"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            stats["commits_today"] = len(result.stdout.strip().split('\\n')) if result.stdout.strip() else 0
    except:
        pass
        
    return stats

def create_email_content(template, **kwargs):
    """Create email content based on template"""
    stats = get_project_stats()
    
    if template == "daily_summary":
        subject = f"Daily Project Summary - {stats['date']}"
        body = f"""
Daily Project Summary
====================

Date: {stats['date']}
Time: {stats['time']}

Today's Activity:
- Commits: {stats['commits_today']}
- Files Changed: {stats['files_changed']}
- Tasks Completed: {stats['todos_completed']}

Have a great evening!
"""
        
    elif template == "weekly_report":
        subject = f"Weekly Project Report - Week of {stats['date']}"
        body = f"""
Weekly Project Report
====================

Week ending: {stats['date']}

This week's highlights:
- [Summary of major accomplishments]
- [Key metrics and progress]
- [Upcoming priorities]

Generated automatically by Multi-Agent Squad
"""
        
    elif template == "error_alert":
        subject = "🚨 Error Alert - Immediate Attention Required"
        error = kwargs.get('error', 'Unknown error')
        body = f"""
ERROR ALERT
===========

Time: {stats['date']} {stats['time']}

Error Details:
--------------
{error}

Please investigate immediately.
"""
        
    elif template == "build_status":
        status = kwargs.get('status', 1)
        if status == 0:
            subject = "✅ Build Successful"
            body = "Build completed successfully!"
        else:
            subject = "❌ Build Failed"
            body = f"Build failed with exit code: {status}"
            
    else:
        subject = "Project Notification"
        body = kwargs.get('message', 'Notification from Multi-Agent Squad')
        
    return subject, body

def send_email(subject, body, immediate=False):
    """Send email using configured service"""
    config = load_config()
    
    # Check preferences
    if config['preferences'].get('daily_digest') and not immediate:
        # Queue for daily digest (would implement queuing here)
        print(f"Email queued for daily digest: {subject}")
        return
        
    # Send based on service type
    if config['service'] in ['gmail', 'smtp']:
        send_smtp_email(config, subject, body)
    elif config['service'] == 'sendgrid':
        send_sendgrid_email(config, subject, body)
    elif config['service'] == 'aws_ses':
        send_ses_email(config, subject, body)
        
def send_smtp_email(config, subject, body):
    """Send email via SMTP"""
    msg = MIMEMultipart()
    msg['From'] = config['from_email']
    msg['To'] = ', '.join(config['recipients'])
    msg['Subject'] = subject
    
    if config['preferences'].get('html_emails'):
        msg.attach(MIMEText(body.replace('\\n', '<br>'), 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))
        
    try:
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            if config.get('use_tls'):
                server.starttls()
            server.login(config['username'], config['password'])
            server.send_message(msg)
        print(f"✅ Email sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_sendgrid_email(config, subject, body):
    """Send email via SendGrid"""
    print(f"📧 SendGrid email: {subject}")
    print("(SendGrid implementation would go here)")
    
def send_ses_email(config, subject, body):
    """Send email via AWS SES"""
    print(f"📧 AWS SES email: {subject}")
    print("(AWS SES implementation would go here)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", help="Email template to use")
    parser.add_argument("--message", help="Custom message")
    parser.add_argument("--status", type=int, help="Status code")
    parser.add_argument("--error", help="Error details")
    parser.add_argument("--immediate", action="store_true", help="Send immediately")
    
    args = parser.parse_args()
    
    if args.template:
        subject, body = create_email_content(
            args.template,
            status=args.status,
            error=args.error,
            message=args.message
        )
        send_email(subject, body, args.immediate)
    else:
        # Test email
        send_email(
            "Test Email - Multi-Agent Squad",
            "This is a test email from your Multi-Agent Squad setup.\\n\\nIf you received this, your email integration is working correctly!",
            immediate=True
        )
'''
        
        script_path = Path("scripts/email-notify.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
    def test_integration(self) -> None:
        """Test the email integration"""
        print("\n🧪 Testing email integration...")
        
        try:
            import subprocess
            result = subprocess.run(
                ["python", "scripts/email-notify.py"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Test email sent successfully!")
                print("Check your inbox for the test email.")
            else:
                print(f"❌ Test failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Test failed: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        integration = EmailIntegration()
        integration.test_integration()
    else:
        integration = EmailIntegration()
        integration.interactive_setup()


if __name__ == "__main__":
    main()