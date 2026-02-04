#!/usr/bin/env python3
"""
GitHub Integration for Multi-Agent Squad
Manages issues, PRs, and project synchronization
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class GitHubIntegration:
    def __init__(self):
        self.check_gh_cli()
        self.load_config()
        
    def check_gh_cli(self):
        """Check if GitHub CLI is installed and authenticated"""
        try:
            result = subprocess.run(['gh', 'auth', 'status'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ GitHub CLI not authenticated. Run: gh auth login")
                sys.exit(1)
        except FileNotFoundError:
            print("❌ GitHub CLI not found. Install from: https://cli.github.com/")
            sys.exit(1)
    
    def load_config(self):
        """Load GitHub configuration from PROJECT.md"""
        self.config = {
            'organization': None,
            'project_board': None,
            'labels': ['feature', 'bug', 'enhancement', 'documentation'],
            'auto_assign': True,
            'require_reviews': 2
        }
        
        # Try to parse PROJECT.md for GitHub config
        if os.path.exists('PROJECT.md'):
            with open('PROJECT.md', 'r') as f:
                content = f.read()
                # Simple parsing - in production, use proper YAML parser
                if 'github:' in content:
                    # Extract GitHub configuration section
                    pass
    
    def create_feature_issue(self, feature_name: str, description: str, 
                           repos: List[str], priority: str = 'medium') -> str:
        """Create a GitHub issue for a new feature"""
        title = f"Feature: {feature_name.replace('-', ' ').title()}"
        
        # Build issue body
        body = f"""## Feature Description
{description}

## Affected Repositories
{chr(10).join(f'- [ ] {repo}' for repo in repos)}

## Priority
{priority.upper()}

## Acceptance Criteria
- [ ] Implementation complete in all affected repositories
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Code review approved
- [ ] Documentation updated

## Worktrees
{chr(10).join(f'- `{repo}/feature-{feature_name}`' for repo in repos)}

---
*Tracked by Multi-Agent Squad Orchestrator*
"""
        
        # Create issue
        cmd = [
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
            '--label', 'feature',
            '--label', f'priority:{priority}'
        ]
        
        if self.config.get('project_board'):
            cmd.extend(['--project', self.config['project_board']])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            issue_url = result.stdout.strip()
            issue_number = issue_url.split('/')[-1]
            print(f"✅ Created issue #{issue_number}: {issue_url}")
            return issue_number
        else:
            print(f"❌ Failed to create issue: {result.stderr}")
            return None
    
    def update_issue_status(self, issue_number: str, status: str, 
                          details: Optional[str] = None):
        """Update issue with current status"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        comment = f"""## Status Update - {timestamp}
**Current Status**: {status}

"""
        
        if details:
            comment += f"{details}\n\n"
        
        comment += "*Updated by Multi-Agent Squad Orchestrator*"
        
        cmd = [
            'gh', 'issue', 'comment', issue_number,
            '--body', comment
        ]
        
        subprocess.run(cmd, capture_output=True)
        print(f"✅ Updated issue #{issue_number} status")
    
    def create_pr(self, repo: str, feature_name: str, 
                  issue_number: Optional[str] = None) -> str:
        """Create a pull request for a feature"""
        branch = f"feature/{feature_name}"
        title = f"feat: {feature_name.replace('-', ' ').title()}"
        
        # Generate PR body
        body = f"""## Description
Implementation of {feature_name} feature.

"""
        
        if issue_number:
            body += f"Fixes #{issue_number}\n\n"
        
        body += """## Changes
- [ ] Implementation complete
- [ ] Tests added/updated
- [ ] Documentation updated

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete

## Review Checklist
- [ ] Code follows project standards
- [ ] No security vulnerabilities
- [ ] Performance impact acceptable
- [ ] Error handling appropriate
"""
        
        # Change to repo directory
        repo_path = f"projects/{repo}"
        if not os.path.exists(repo_path):
            print(f"❌ Repository not found: {repo_path}")
            return None
        
        os.chdir(repo_path)
        
        # Create PR
        cmd = [
            'gh', 'pr', 'create',
            '--title', title,
            '--body', body,
            '--base', 'main',
            '--head', branch
        ]
        
        if self.config.get('require_reviews'):
            # Note: Can't set required reviewers via CLI, but can add reviewers
            cmd.extend(['--reviewer', '@team/senior-engineers'])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            pr_url = result.stdout.strip()
            print(f"✅ Created PR: {pr_url}")
            return pr_url
        else:
            print(f"❌ Failed to create PR: {result.stderr}")
            return None
    
    def link_pr_to_issue(self, pr_url: str, issue_number: str):
        """Link a PR to an issue"""
        pr_number = pr_url.split('/')[-1]
        
        # Add comment to issue
        comment = f"🔗 Pull Request #{pr_number} has been created: {pr_url}"
        
        cmd = [
            'gh', 'issue', 'comment', issue_number,
            '--body', comment
        ]
        
        subprocess.run(cmd, capture_output=True)
    
    def get_issue_status(self, issue_number: str) -> Dict:
        """Get current status of an issue"""
        cmd = [
            'gh', 'issue', 'view', issue_number,
            '--json', 'title,state,labels,assignees,projectItems'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return None
    
    def list_feature_prs(self, feature_name: str) -> List[Dict]:
        """List all PRs for a feature across repos"""
        branch = f"feature/{feature_name}"
        
        cmd = [
            'gh', 'pr', 'list',
            '--head', branch,
            '--json', 'number,title,state,repository,url',
            '--limit', '50'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return []
    
    def close_completed_issue(self, issue_number: str, merged_prs: List[str]):
        """Close an issue after feature completion"""
        comment = f"""## ✅ Feature Complete!

All pull requests have been merged:
{chr(10).join(f'- {pr}' for pr in merged_prs)}

Worktrees have been cleaned up.

*Closed by Multi-Agent Squad Orchestrator*
"""
        
        # Add closing comment
        subprocess.run([
            'gh', 'issue', 'comment', issue_number,
            '--body', comment
        ], capture_output=True)
        
        # Close the issue
        subprocess.run([
            'gh', 'issue', 'close', issue_number
        ], capture_output=True)
        
        print(f"✅ Closed issue #{issue_number}")
    
    def generate_status_report(self) -> str:
        """Generate a comprehensive status report"""
        report = """# GitHub Integration Status Report

## Open Issues
"""
        
        # Get open issues
        cmd = [
            'gh', 'issue', 'list',
            '--label', 'feature',
            '--json', 'number,title,labels,assignees,createdAt',
            '--limit', '20'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            issues = json.loads(result.stdout)
            for issue in issues:
                labels = ', '.join(l['name'] for l in issue['labels'])
                report += f"- #{issue['number']}: {issue['title']} ({labels})\n"
        
        report += "\n## Active Pull Requests\n"
        
        # Get open PRs
        cmd = [
            'gh', 'pr', 'list',
            '--json', 'number,title,state,isDraft,repository',
            '--limit', '20'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            prs = json.loads(result.stdout)
            for pr in prs:
                status = "Draft" if pr['isDraft'] else "Ready"
                report += f"- #{pr['number']}: {pr['title']} ({status})\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description='GitHub Integration for Multi-Agent Squad')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create issue command
    create_issue = subparsers.add_parser('create-issue', help='Create a feature issue')
    create_issue.add_argument('feature_name', help='Feature name (kebab-case)')
    create_issue.add_argument('description', help='Feature description')
    create_issue.add_argument('--repos', nargs='+', required=True, help='Affected repositories')
    create_issue.add_argument('--priority', default='medium', choices=['low', 'medium', 'high'])
    
    # Update issue command
    update_issue = subparsers.add_parser('update-issue', help='Update issue status')
    update_issue.add_argument('issue_number', help='Issue number')
    update_issue.add_argument('status', help='Current status')
    update_issue.add_argument('--details', help='Additional details')
    
    # Create PR command
    create_pr = subparsers.add_parser('create-pr', help='Create a pull request')
    create_pr.add_argument('repo', help='Repository name')
    create_pr.add_argument('feature_name', help='Feature name')
    create_pr.add_argument('--issue', help='Related issue number')
    
    # Status report command
    subparsers.add_parser('status', help='Generate status report')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    gh = GitHubIntegration()
    
    if args.command == 'create-issue':
        gh.create_feature_issue(
            args.feature_name,
            args.description,
            args.repos,
            args.priority
        )
    
    elif args.command == 'update-issue':
        gh.update_issue_status(
            args.issue_number,
            args.status,
            args.details
        )
    
    elif args.command == 'create-pr':
        pr_url = gh.create_pr(args.repo, args.feature_name, args.issue)
        if pr_url and args.issue:
            gh.link_pr_to_issue(pr_url, args.issue)
    
    elif args.command == 'status':
        print(gh.generate_status_report())


if __name__ == '__main__':
    main()