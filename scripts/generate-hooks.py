#!/usr/bin/env python3
"""
Hook Generator for Multi-Agent Squad
Creates custom hooks based on project needs
"""

import os
import json
from pathlib import Path
from typing import Dict, List

class HookGenerator:
    def __init__(self):
        self.hooks_dir = Path(".claude/hooks")
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_hooks_from_needs(self, project_info: Dict) -> None:
        """Generate hooks based on project needs"""
        hooks = []
        
        # Analyze project type and needs
        project_type = project_info.get('type', 'general')
        automation_needs = project_info.get('automation_needs', [])
        automation_level = project_info.get('automation_level', 'minimal')
        
        # Generate appropriate hooks
        if project_type in ['web_app', 'api', 'software']:
            hooks.extend(self._coding_hooks(automation_needs, automation_level))
        elif project_type in ['documentation', 'writing', 'content']:
            hooks.extend(self._writing_hooks(automation_needs, automation_level))
        elif project_type in ['design', 'creative']:
            hooks.extend(self._creative_hooks(automation_needs, automation_level))
        
        # Add custom automation based on specific needs
        hooks.extend(self._custom_hooks(automation_needs))
        
        # Write hooks configuration
        self._write_hooks_config(hooks)
        
    def _coding_hooks(self, needs: List[str], level: str) -> List[Dict]:
        """Generate hooks for coding projects"""
        hooks = []
        
        # Test automation
        if any(need in str(needs).lower() for need in ['test', 'testing', 'forget test']):
            hooks.append({
                'event': 'PostToolUse',
                'matcher': {
                    'tool_name': 'Write',
                    'file_paths': ['src/**/*', 'lib/**/*']
                },
                'command': 'echo "🧪 Running tests..." && npm test 2>/dev/null || pytest 2>/dev/null || echo "Configure test command in package.json or setup.py"',
                'run_in_background': True
            })
        
        # Code formatting
        if any(need in str(needs).lower() for need in ['format', 'style', 'lint']):
            hooks.append({
                'event': 'PostToolUse',
                'matcher': {
                    'tool_name': 'Write',
                    'file_paths': ['**/*.py', '**/*.js', '**/*.ts']
                },
                'command': '''
if [[ $CLAUDE_FILE_PATH == *.py ]]; then
    black $CLAUDE_FILE_PATH 2>/dev/null || echo "Install black for Python formatting"
elif [[ $CLAUDE_FILE_PATH == *.js ]] || [[ $CLAUDE_FILE_PATH == *.ts ]]; then
    prettier --write $CLAUDE_FILE_PATH 2>/dev/null || echo "Install prettier for JS/TS formatting"
fi
''',
                'run_in_background': True
            })
        
        # Daily standup
        if any(need in str(needs).lower() for need in ['standup', 'daily meeting', 'status']):
            hooks.append({
                'event': 'Notification',
                'matcher': {
                    'time': '09:00',
                    'days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
                },
                'command': 'echo "📅 Daily Standup Reminder!\\n- What did you complete yesterday?\\n- What will you work on today?\\n- Any blockers?"'
            })
        
        # Git commit reminders
        if level in ['moderate', 'maximum']:
            hooks.append({
                'event': 'Notification',
                'matcher': {
                    'time': 'every 2 hours'
                },
                'command': 'echo "💾 Remember to commit your work!" && git status --short'
            })
        
        return hooks
    
    def _writing_hooks(self, needs: List[str], level: str) -> List[Dict]:
        """Generate hooks for writing projects"""
        hooks = []
        
        # Word count tracking
        if any(need in str(needs).lower() for need in ['word count', 'track progress', 'writing goal']):
            hooks.append({
                'event': 'Stop',
                'command': '''
count=$(find . -name "*.md" -o -name "*.txt" | xargs wc -w | tail -1 | awk '{print $1}')
echo "📝 Session word count: $count total words"
echo "$(date): $count words" >> .writing-progress.log
'''
            })
        
        # Grammar checking
        if any(need in str(needs).lower() for need in ['grammar', 'spelling', 'writing quality']):
            hooks.append({
                'event': 'PostToolUse',
                'matcher': {
                    'tool_name': 'Write',
                    'file_paths': ['**/*.md', '**/*.txt']
                },
                'command': 'echo "📖 Checking writing quality..." && echo "Install a grammar checker like LanguageTool or Grammarly CLI for automated checks"'
            })
        
        # Backup reminders
        if level in ['moderate', 'maximum']:
            hooks.append({
                'event': 'Notification',
                'matcher': {
                    'time': '17:00'
                },
                'command': 'echo "☁️ Daily backup reminder! Save your work to cloud storage."'
            })
        
        return hooks
    
    def _creative_hooks(self, needs: List[str], level: str) -> List[Dict]:
        """Generate hooks for creative projects"""
        hooks = []
        
        # Progress snapshots
        if any(need in str(needs).lower() for need in ['version', 'snapshot', 'backup']):
            hooks.append({
                'event': 'Notification',
                'matcher': {
                    'time': '16:00'
                },
                'command': 'echo "📸 Creating daily snapshot..." && git add -A && git commit -m "Daily progress: $(date +%Y-%m-%d)" || echo "No changes to snapshot"'
            })
        
        return hooks
    
    def _custom_hooks(self, needs: List[str]) -> List[Dict]:
        """Generate custom hooks based on specific needs"""
        hooks = []
        
        # Security checks
        if any(need in str(needs).lower() for need in ['security', 'secrets', 'password']):
            hooks.append({
                'event': 'PreToolUse',
                'matcher': {
                    'tool_name': 'Bash',
                    'args_regex': 'git commit'
                },
                'command': 'echo "🔒 Checking for secrets..." && git diff --cached | grep -iE "(password|secret|api_key|token)\\s*=" && echo "⚠️ WARNING: Possible secrets detected!" || echo "✅ No obvious secrets found"'
            })
        
        # Deadline reminders
        if any(need in str(needs).lower() for need in ['deadline', 'due date', 'reminder']):
            hooks.append({
                'event': 'Notification',
                'matcher': {
                    'time': '10:00',
                    'days': ['monday', 'friday']
                },
                'command': 'echo "📅 Check your deadlines and project timeline!"'
            })
        
        # Break reminders
        if any(need in str(needs).lower() for need in ['break', 'rest', 'health']):
            hooks.append({
                'event': 'Notification',
                'matcher': {
                    'time': 'every 1 hour'
                },
                'command': 'echo "🌟 Time for a 5-minute break! Stretch and rest your eyes."'
            })
        
        return hooks
    
    def _write_hooks_config(self, hooks: List[Dict]) -> None:
        """Write hooks to configuration file"""
        if not hooks:
            print("No specific automation needs identified. Hooks can be added later as needed.")
            return
            
        config_path = self.hooks_dir / "project-automation.toml"
        
        with open(config_path, 'w') as f:
            f.write("# Project-Specific Automation Hooks\n")
            f.write("# Generated based on your project needs\n")
            f.write("# Feel free to modify or add more hooks as needed\n\n")
            
            for hook in hooks:
                f.write("[[hooks]]\n")
                f.write(f'event = "{hook["event"]}"\n')
                
                if 'run_in_background' in hook:
                    f.write(f'run_in_background = {str(hook["run_in_background"]).lower()}\n')
                
                if 'matcher' in hook:
                    f.write("[hooks.matcher]\n")
                    for key, value in hook['matcher'].items():
                        if isinstance(value, list):
                            f.write(f'{key} = {json.dumps(value)}\n')
                        else:
                            f.write(f'{key} = "{value}"\n')
                
                # Format command nicely
                command = hook['command'].strip()
                if '\n' in command:
                    f.write('command = """\n')
                    f.write(command)
                    f.write('\n"""\n')
                else:
                    f.write(f'command = "{command}"\n')
                
                f.write("\n")
        
        print(f"✅ Created {len(hooks)} automation hooks based on your needs")
        print(f"📄 Hooks saved to: {config_path}")
        print("\nYou can modify these hooks anytime or ask me to add more!")


def interactive_hook_setup():
    """Interactive setup for hooks based on user needs"""
    print("🤖 Let's set up some helpful automations for your project!\n")
    
    generator = HookGenerator()
    
    # This would be called by Claude based on user responses
    # For demonstration, here's an example structure
    example_project_info = {
        'type': 'web_app',
        'automation_needs': [
            'forget to run tests',
            'daily standup reminders',
            'code formatting'
        ],
        'automation_level': 'moderate'
    }
    
    generator.generate_hooks_from_needs(example_project_info)


if __name__ == "__main__":
    # This script would typically be called by Claude during project setup
    # based on user responses to automation questions
    interactive_hook_setup()