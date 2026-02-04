#!/bin/bash
# Git Worktree Manager for Multi-Agent Squad
# Manages isolated worktrees for feature development across multiple repositories

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PROJECTS_DIR="${PROJECTS_DIR:-./projects}"
WORKTREES_DIR="${WORKTREES_DIR:-./worktrees}"
DEFAULT_BASE_BRANCH="${DEFAULT_BASE_BRANCH:-main}"

# Ensure directories exist
mkdir -p "$WORKTREES_DIR"

# Function to print colored output
print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Function to print usage
usage() {
    cat << EOF
Git Worktree Manager for Multi-Agent Squad

Usage: $0 <command> [arguments]

Commands:
    create-feature <feature-name> <repo1> [repo2...]
        Create worktrees for a new feature across specified repositories
        
    list-active
        List all active worktrees and their status
        
    cleanup-merged
        Remove worktrees for branches that have been merged
        
    sync-status
        Synchronize worktree status with GitHub issues
        
    remove-worktree <repo> <feature-name>
        Remove a specific worktree
        
    feature-status <feature-name>
        Show status of all worktrees for a feature

Examples:
    $0 create-feature auth-system frontend backend
    $0 list-active
    $0 cleanup-merged
    $0 feature-status auth-system

Environment Variables:
    PROJECTS_DIR    - Directory containing project repositories (default: ./projects)
    WORKTREES_DIR   - Directory for worktrees (default: ./worktrees)
    DEFAULT_BASE_BRANCH - Default base branch (default: main)
EOF
}

# Function to check if a repository exists
check_repo() {
    local repo=$1
    if [[ ! -d "$PROJECTS_DIR/$repo" ]]; then
        print_color $RED "Error: Repository '$repo' not found in $PROJECTS_DIR"
        return 1
    fi
    if [[ ! -d "$PROJECTS_DIR/$repo/.git" ]]; then
        print_color $RED "Error: '$repo' is not a git repository"
        return 1
    fi
    return 0
}

# Function to create worktrees for a feature
create_feature() {
    local feature_name=$1
    shift
    local repos=("$@")
    
    if [[ ${#repos[@]} -eq 0 ]]; then
        print_color $RED "Error: No repositories specified"
        usage
        exit 1
    fi
    
    print_color $BLUE "Creating worktrees for feature: $feature_name"
    echo
    
    local created_worktrees=()
    
    for repo in "${repos[@]}"; do
        if ! check_repo "$repo"; then
            continue
        fi
        
        local worktree_path="$WORKTREES_DIR/$repo/$feature_name"
        local branch_name="feature/$feature_name"
        
        # Check if worktree already exists
        if [[ -d "$worktree_path" ]]; then
            print_color $YELLOW "⚠ Worktree already exists: $worktree_path"
            continue
        fi
        
        print_color $PURPLE "Creating worktree for $repo..."
        
        # Create worktree directory
        mkdir -p "$(dirname "$worktree_path")"
        
        # Change to repo directory
        cd "$PROJECTS_DIR/$repo"
        
        # Ensure we have the latest base branch
        git fetch origin "$DEFAULT_BASE_BRANCH" --quiet
        
        # Create the worktree
        if git worktree add "$worktree_path" -b "$branch_name" "origin/$DEFAULT_BASE_BRANCH" 2>/dev/null; then
            print_color $GREEN "✓ Created worktree: $worktree_path"
            print_color $GREEN "  Branch: $branch_name"
            created_worktrees+=("$repo:$worktree_path")
        else
            # Branch might already exist
            if git show-ref --verify --quiet "refs/heads/$branch_name"; then
                git worktree add "$worktree_path" "$branch_name"
                print_color $GREEN "✓ Created worktree with existing branch: $worktree_path"
            else
                print_color $RED "✗ Failed to create worktree for $repo"
            fi
        fi
        
        cd - > /dev/null
        echo
    done
    
    if [[ ${#created_worktrees[@]} -gt 0 ]]; then
        print_color $GREEN "\nSuccessfully created ${#created_worktrees[@]} worktree(s) for feature: $feature_name"
        
        # Create a feature tracking file
        local tracking_file="$WORKTREES_DIR/.feature-$feature_name"
        printf "%s\n" "${created_worktrees[@]}" > "$tracking_file"
        
        print_color $BLUE "\nNext steps:"
        echo "1. Agents will work in these isolated worktrees"
        echo "2. Changes will be committed to feature branches"
        echo "3. PRs will be created when feature is ready"
        echo "4. Run '$0 feature-status $feature_name' to check progress"
    fi
}

# Function to list active worktrees
list_active() {
    print_color $BLUE "Active Worktrees:"
    echo
    
    if [[ ! -d "$WORKTREES_DIR" ]] || [[ -z "$(ls -A "$WORKTREES_DIR" 2>/dev/null)" ]]; then
        print_color $YELLOW "No active worktrees found"
        return
    fi
    
    for repo_dir in "$WORKTREES_DIR"/*; do
        if [[ -d "$repo_dir" ]]; then
            local repo=$(basename "$repo_dir")
            print_color $PURPLE "Repository: $repo"
            
            for worktree in "$repo_dir"/*; do
                if [[ -d "$worktree" ]]; then
                    local feature=$(basename "$worktree")
                    local branch_name="feature/$feature"
                    
                    # Get worktree status
                    cd "$worktree" 2>/dev/null || continue
                    
                    local status="Clean"
                    local changes=$(git status --porcelain 2>/dev/null | wc -l)
                    if [[ $changes -gt 0 ]]; then
                        status="$changes uncommitted changes"
                    fi
                    
                    local ahead_behind=$(git rev-list --left-right --count origin/$DEFAULT_BASE_BRANCH...HEAD 2>/dev/null || echo "0 0")
                    local behind=$(echo $ahead_behind | cut -d' ' -f1)
                    local ahead=$(echo $ahead_behind | cut -d' ' -f2)
                    
                    print_color $GREEN "  ├─ Feature: $feature"
                    echo "  │  Path: $worktree"
                    echo "  │  Branch: $branch_name"
                    echo "  │  Status: $status"
                    echo "  │  Commits: $ahead ahead, $behind behind $DEFAULT_BASE_BRANCH"
                    echo "  │"
                    
                    cd - > /dev/null
                done
            done
            echo
        fi
    done
}

# Function to cleanup merged worktrees
cleanup_merged() {
    print_color $BLUE "Cleaning up merged worktrees..."
    echo
    
    local removed_count=0
    
    for repo_dir in "$WORKTREES_DIR"/*; do
        if [[ -d "$repo_dir" ]]; then
            local repo=$(basename "$repo_dir")
            
            if ! check_repo "$repo"; then
                continue
            fi
            
            cd "$PROJECTS_DIR/$repo"
            
            # Get list of merged branches
            local merged_branches=$(git branch -r --merged origin/$DEFAULT_BASE_BRANCH | grep -E "origin/feature/" | sed 's/.*origin\///' || true)
            
            for worktree in "$repo_dir"/*; do
                if [[ -d "$worktree" ]]; then
                    local feature=$(basename "$worktree")
                    local branch_name="feature/$feature"
                    
                    if echo "$merged_branches" | grep -q "^$branch_name$"; then
                        print_color $YELLOW "Removing merged worktree: $repo/$feature"
                        
                        # Remove the worktree
                        git worktree remove "$worktree" --force 2>/dev/null || rm -rf "$worktree"
                        
                        # Delete the local branch
                        git branch -D "$branch_name" 2>/dev/null || true
                        
                        ((removed_count++))
                    fi
                fi
            done
            
            cd - > /dev/null
            
            # Remove empty repo directories
            rmdir "$repo_dir" 2>/dev/null || true
        fi
    done
    
    # Clean up feature tracking files
    for tracking_file in "$WORKTREES_DIR"/.feature-*; do
        if [[ -f "$tracking_file" ]]; then
            local feature_name=$(basename "$tracking_file" | sed 's/^\.feature-//')
            local has_active_worktree=false
            
            while IFS= read -r line; do
                local worktree_path=$(echo "$line" | cut -d: -f2)
                if [[ -d "$worktree_path" ]]; then
                    has_active_worktree=true
                    break
                fi
            done < "$tracking_file"
            
            if [[ "$has_active_worktree" == false ]]; then
                rm "$tracking_file"
            fi
        fi
    done
    
    if [[ $removed_count -gt 0 ]]; then
        print_color $GREEN "\nRemoved $removed_count merged worktree(s)"
    else
        print_color $YELLOW "\nNo merged worktrees found to cleanup"
    fi
}

# Function to show feature status
feature_status() {
    local feature_name=$1
    
    print_color $BLUE "Status for feature: $feature_name"
    echo
    
    local tracking_file="$WORKTREES_DIR/.feature-$feature_name"
    
    if [[ ! -f "$tracking_file" ]]; then
        print_color $RED "No tracking information found for feature: $feature_name"
        return 1
    fi
    
    while IFS= read -r line; do
        local repo=$(echo "$line" | cut -d: -f1)
        local worktree_path=$(echo "$line" | cut -d: -f2)
        
        if [[ -d "$worktree_path" ]]; then
            print_color $PURPLE "Repository: $repo"
            
            cd "$worktree_path"
            
            # Get detailed status
            local branch=$(git branch --show-current)
            local changes=$(git status --porcelain | wc -l)
            local commits=$(git rev-list --count origin/$DEFAULT_BASE_BRANCH..HEAD)
            
            echo "  Branch: $branch"
            echo "  Path: $worktree_path"
            echo "  Uncommitted changes: $changes"
            echo "  Commits ahead of $DEFAULT_BASE_BRANCH: $commits"
            
            if [[ $changes -gt 0 ]]; then
                echo "  Modified files:"
                git status --porcelain | head -5 | sed 's/^/    /'
                if [[ $(git status --porcelain | wc -l) -gt 5 ]]; then
                    echo "    ... and $((changes - 5)) more"
                fi
            fi
            
            # Check if PR exists
            if command -v gh &> /dev/null; then
                local pr_status=$(gh pr list --head "$branch" --json state,url --jq '.[0] | "\(.state) - \(.url)"' 2>/dev/null || echo "No PR")
                echo "  Pull Request: $pr_status"
            fi
            
            cd - > /dev/null
            echo
        else
            print_color $YELLOW "  Worktree not found: $worktree_path"
        fi
    done < "$tracking_file"
}

# Function to remove a specific worktree
remove_worktree() {
    local repo=$1
    local feature_name=$2
    
    if ! check_repo "$repo"; then
        exit 1
    fi
    
    local worktree_path="$WORKTREES_DIR/$repo/$feature_name"
    
    if [[ ! -d "$worktree_path" ]]; then
        print_color $RED "Worktree not found: $worktree_path"
        exit 1
    fi
    
    print_color $YELLOW "Removing worktree: $repo/$feature_name"
    
    cd "$PROJECTS_DIR/$repo"
    
    # Remove the worktree
    git worktree remove "$worktree_path" --force 2>/dev/null || rm -rf "$worktree_path"
    
    # Optionally delete the branch
    read -p "Delete the branch 'feature/$feature_name'? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -D "feature/$feature_name" 2>/dev/null || true
        print_color $GREEN "Branch deleted"
    fi
    
    cd - > /dev/null
    
    # Clean up empty directories
    rmdir "$WORKTREES_DIR/$repo" 2>/dev/null || true
    
    print_color $GREEN "Worktree removed successfully"
}

# Function to sync status with GitHub
sync_status() {
    if ! command -v gh &> /dev/null; then
        print_color $RED "Error: GitHub CLI (gh) is not installed"
        echo "Install it from: https://cli.github.com/"
        exit 1
    fi
    
    print_color $BLUE "Syncing worktree status with GitHub..."
    echo
    
    # This is a placeholder for GitHub integration
    # In a real implementation, this would:
    # 1. Check GitHub issues for active features
    # 2. Update issue status based on worktree progress
    # 3. Link PRs to issues
    # 4. Update project boards
    
    print_color $YELLOW "GitHub sync functionality coming soon!"
    echo "This will integrate with the github-integration.py script"
}

# Main command handler
case "${1:-}" in
    create-feature)
        shift
        if [[ $# -lt 2 ]]; then
            print_color $RED "Error: Feature name and at least one repository required"
            usage
            exit 1
        fi
        create_feature "$@"
        ;;
    list-active)
        list_active
        ;;
    cleanup-merged)
        cleanup_merged
        ;;
    sync-status)
        sync_status
        ;;
    feature-status)
        shift
        if [[ -z "${1:-}" ]]; then
            print_color $RED "Error: Feature name required"
            usage
            exit 1
        fi
        feature_status "$1"
        ;;
    remove-worktree)
        shift
        if [[ $# -ne 2 ]]; then
            print_color $RED "Error: Repository and feature name required"
            usage
            exit 1
        fi
        remove_worktree "$1" "$2"
        ;;
    *)
        usage
        exit 1
        ;;
esac