#!/usr/bin/env python3
"""
Project Discovery Script for Multi-Agent Squad
Automatically discovers project structure and helps initialize PROJECT.md
"""

import os
import json
import yaml
import glob
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Optional

class ProjectDiscovery:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.project_info = {
            'repositories': [],
            'technology_stack': {
                'languages': set(),
                'frameworks': set(),
                'databases': set(),
                'tools': set()
            },
            'project_type': set(),
            'has_tests': False,
            'has_ci_cd': False,
            'has_docker': False
        }
    
    def discover(self) -> Dict:
        """Main discovery process"""
        print("🔍 Discovering project structure...\n")
        
        # Check if this is a multi-repo setup
        projects_dir = self.root_path / "projects"
        if projects_dir.exists():
            self.discover_multi_repo(projects_dir)
        else:
            self.discover_single_repo(self.root_path)
        
        # Analyze discovered information
        self.analyze_project_type()
        self.check_integrations()
        
        return self.format_report()
    
    def discover_multi_repo(self, projects_dir: Path):
        """Discover repositories in projects directory"""
        print(f"📁 Found projects directory: {projects_dir}")
        
        for repo_path in projects_dir.iterdir():
            if repo_path.is_dir() and not repo_path.name.startswith('.'):
                repo_info = self.analyze_repository(repo_path)
                if repo_info:
                    self.project_info['repositories'].append(repo_info)
                    print(f"  ✓ Discovered repository: {repo_path.name}")
    
    def discover_single_repo(self, repo_path: Path):
        """Discover single repository setup"""
        repo_info = self.analyze_repository(repo_path)
        if repo_info:
            self.project_info['repositories'].append(repo_info)
    
    def analyze_repository(self, repo_path: Path) -> Optional[Dict]:
        """Analyze a single repository"""
        if not (repo_path / ".git").exists() and not any(repo_path.glob("*")):
            return None
        
        repo_info = {
            'name': repo_path.name,
            'path': str(repo_path.relative_to(self.root_path)),
            'type': 'unknown',
            'language': 'unknown',
            'framework': 'unknown',
            'has_tests': False,
            'dependencies': []
        }
        
        # Detect language and framework
        files = list(repo_path.rglob("*"))
        
        # Python detection
        if any(f.name == "requirements.txt" or f.name == "setup.py" or f.name == "pyproject.toml" for f in files):
            repo_info['language'] = 'Python'
            self.project_info['technology_stack']['languages'].add('Python')
            
            # Detect Python frameworks
            for file in files:
                if file.name in ["requirements.txt", "Pipfile", "pyproject.toml"]:
                    content = self.read_file_safe(file)
                    if content:
                        if 'django' in content.lower():
                            repo_info['framework'] = 'Django'
                            self.project_info['technology_stack']['frameworks'].add('Django')
                        elif 'fastapi' in content.lower():
                            repo_info['framework'] = 'FastAPI'
                            self.project_info['technology_stack']['frameworks'].add('FastAPI')
                        elif 'flask' in content.lower():
                            repo_info['framework'] = 'Flask'
                            self.project_info['technology_stack']['frameworks'].add('Flask')
        
        # JavaScript/TypeScript detection
        elif any(f.name == "package.json" for f in files):
            package_json_path = next(f for f in files if f.name == "package.json")
            package_data = self.read_json_safe(package_json_path)
            
            if package_data:
                repo_info['language'] = 'TypeScript' if any(f.suffix == '.ts' or f.suffix == '.tsx' for f in files) else 'JavaScript'
                self.project_info['technology_stack']['languages'].add(repo_info['language'])
                
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                # Detect frameworks
                if 'react' in deps:
                    repo_info['framework'] = 'React'
                    self.project_info['technology_stack']['frameworks'].add('React')
                elif 'vue' in deps:
                    repo_info['framework'] = 'Vue'
                    self.project_info['technology_stack']['frameworks'].add('Vue')
                elif 'angular' in deps:
                    repo_info['framework'] = 'Angular'
                    self.project_info['technology_stack']['frameworks'].add('Angular')
                elif 'express' in deps:
                    repo_info['framework'] = 'Express'
                    self.project_info['technology_stack']['frameworks'].add('Express')
                elif 'next' in deps:
                    repo_info['framework'] = 'Next.js'
                    self.project_info['technology_stack']['frameworks'].add('Next.js')
        
        # Go detection
        elif any(f.name == "go.mod" for f in files):
            repo_info['language'] = 'Go'
            self.project_info['technology_stack']['languages'].add('Go')
        
        # Java detection
        elif any(f.name == "pom.xml" or f.name == "build.gradle" for f in files):
            repo_info['language'] = 'Java'
            self.project_info['technology_stack']['languages'].add('Java')
            
            if any(f.name == "pom.xml" for f in files):
                pom_content = self.read_file_safe(next(f for f in files if f.name == "pom.xml"))
                if pom_content and 'spring' in pom_content.lower():
                    repo_info['framework'] = 'Spring'
                    self.project_info['technology_stack']['frameworks'].add('Spring')
        
        # Detect repository type
        if repo_info['framework'] in ['React', 'Vue', 'Angular', 'Next.js']:
            repo_info['type'] = 'frontend'
        elif repo_info['framework'] in ['Django', 'FastAPI', 'Flask', 'Express', 'Spring']:
            repo_info['type'] = 'backend'
        elif 'docker' in repo_path.name.lower() or 'infra' in repo_path.name.lower():
            repo_info['type'] = 'infrastructure'
        
        # Check for tests
        test_patterns = ['**/test/**', '**/tests/**', '**/*test*', '**/*spec*']
        repo_info['has_tests'] = any(list(repo_path.glob(pattern)) for pattern in test_patterns)
        if repo_info['has_tests']:
            self.project_info['has_tests'] = True
        
        # Check for Docker
        if any(f.name == "Dockerfile" or f.name == "docker-compose.yml" for f in files):
            self.project_info['has_docker'] = True
        
        return repo_info
    
    def analyze_project_type(self):
        """Determine overall project type based on repositories"""
        repo_types = [repo['type'] for repo in self.project_info['repositories']]
        
        if 'frontend' in repo_types and 'backend' in repo_types:
            self.project_info['project_type'].add('Web Application (Full Stack)')
        elif 'backend' in repo_types and 'frontend' not in repo_types:
            self.project_info['project_type'].add('API Service (Backend Only)')
        elif 'frontend' in repo_types and 'backend' not in repo_types:
            self.project_info['project_type'].add('Frontend Application')
        
        if len(self.project_info['repositories']) > 3:
            self.project_info['project_type'].add('Microservices Architecture')
        elif len(self.project_info['repositories']) == 1:
            self.project_info['project_type'].add('Monolithic Application')
    
    def check_integrations(self):
        """Check for CI/CD and other integrations"""
        ci_patterns = [
            '.github/workflows',
            '.gitlab-ci.yml',
            'Jenkinsfile',
            '.circleci',
            'azure-pipelines.yml'
        ]
        
        for pattern in ci_patterns:
            if list(self.root_path.glob(f"**/{pattern}")):
                self.project_info['has_ci_cd'] = True
                break
    
    def read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read file content"""
        try:
            return file_path.read_text(encoding='utf-8')
        except:
            return None
    
    def read_json_safe(self, file_path: Path) -> Optional[Dict]:
        """Safely read JSON file"""
        try:
            return json.loads(file_path.read_text(encoding='utf-8'))
        except:
            return None
    
    def format_report(self) -> Dict:
        """Format discovery report"""
        return {
            'project_info': {
                'repository_count': len(self.project_info['repositories']),
                'project_types': list(self.project_info['project_type']),
                'languages': list(self.project_info['technology_stack']['languages']),
                'frameworks': list(self.project_info['technology_stack']['frameworks']),
                'has_tests': self.project_info['has_tests'],
                'has_docker': self.project_info['has_docker'],
                'has_ci_cd': self.project_info['has_ci_cd']
            },
            'repositories': self.project_info['repositories']
        }
    
    def generate_project_md(self, report: Dict) -> str:
        """Generate PROJECT.md content based on discovery"""
        content = f"""# Project Description

## Project Overview

**Project Name:** {self.root_path.name}

**Project Type:** (Auto-detected, please verify)
"""
        
        for ptype in report['project_info']['project_types']:
            content += f"- [x] {ptype}\n"
        
        content += f"""
**Project Description:** (Please fill in)
```
[Describe your project's purpose and main features]
```

## Repository Structure

**Repository Type:**
- [x] {"Multi-Repository" if len(report['repositories']) > 1 else "Single Repository"}

**Repositories:** (Auto-detected)
```yaml
repositories:
"""
        
        for repo in report['repositories']:
            content += f"""  - name: {repo['name']}
    path: {repo['path']}
    description: {repo['type'].title()} application
    primary_language: {repo['language']}
    framework: {repo['framework']}
    
"""
        
        content += f"""```

## Technology Stack (Auto-detected)

**Languages:** {', '.join(report['project_info']['languages'])}
**Frameworks:** {', '.join(report['project_info']['frameworks'])}
**Has Tests:** {"Yes" if report['project_info']['has_tests'] else "No - Consider adding tests"}
**Has Docker:** {"Yes" if report['project_info']['has_docker'] else "No"}
**Has CI/CD:** {"Yes" if report['project_info']['has_ci_cd'] else "No - Consider adding CI/CD"}

## Next Steps

1. Review and update the auto-detected information
2. Fill in the missing sections
3. Run `python scripts/generate-agents.py` to create your agent squad
"""
        
        return content


def main():
    print("🚀 Multi-Agent Squad Project Discovery\n")
    
    discovery = ProjectDiscovery()
    report = discovery.discover()
    
    print("\n📊 Discovery Report:")
    print(f"  • Found {report['project_info']['repository_count']} repositories")
    print(f"  • Languages: {', '.join(report['project_info']['languages'])}")
    print(f"  • Frameworks: {', '.join(report['project_info']['frameworks'])}")
    print(f"  • Project Types: {', '.join(report['project_info']['project_types'])}")
    
    print("\n📁 Repositories:")
    for repo in report['repositories']:
        print(f"  • {repo['name']} ({repo['type']}) - {repo['language']}/{repo['framework']}")
    
    # Check if PROJECT.md exists
    project_md_path = Path("PROJECT.md")
    if project_md_path.exists():
        print("\n⚠️  PROJECT.md already exists.")
        response = input("Do you want to update it with discovered information? (y/N): ")
        if response.lower() != 'y':
            print("Skipping PROJECT.md update.")
            return
    
    # Generate PROJECT.md
    project_md_content = discovery.generate_project_md(report)
    
    # Save or display
    response = input("\n💾 Save discovered information to PROJECT.md? (Y/n): ")
    if response.lower() != 'n':
        project_md_path.write_text(project_md_content)
        print("✅ PROJECT.md has been updated with discovered information.")
        print("📝 Please review and complete the missing sections.")
    else:
        print("\n--- PROJECT.md Preview ---")
        print(project_md_content)


if __name__ == '__main__':
    main()