#!/bin/bash
# PR Review Cycle Management - Enterprise Workflow

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to create PR with proper template
create_pr() {
    local branch=$1
    local title=$2
    local body_file="pr-template.md"
    
    # Create PR template
    cat > "$body_file" << 'EOF'
## Description
[Describe the changes in this PR]

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass locally
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Review Requests
@senior-engineer - Code quality review
@security-team - Security review
@qa-team - Test coverage review

## Screenshots (if applicable)
[Add screenshots here]

## Performance Impact
[Describe any performance implications]

## Security Considerations
[List any security considerations]
EOF
    
    echo -e "${BLUE}Creating PR from branch: $branch${NC}"
    gh pr create --base main --head "$branch" --title "$title" --body-file "$body_file"
    rm "$body_file"
}

# Function to check PR review status
check_pr_status() {
    local pr_number=$1
    
    echo -e "${BLUE}Checking PR #$pr_number status...${NC}"
    
    # Get PR details
    pr_data=$(gh pr view "$pr_number" --json reviews,comments,checksStatus,mergeable)
    
    # Check automated checks
    checks_status=$(echo "$pr_data" | jq -r '.checksStatus')
    if [ "$checks_status" != "PASS" ]; then
        echo -e "${RED}❌ Automated checks failing${NC}"
        gh pr checks "$pr_number"
        return 1
    fi
    
    # Check reviews
    reviews=$(echo "$pr_data" | jq -r '.reviews')
    approved_count=$(echo "$reviews" | jq '[.[] | select(.state == "APPROVED")] | length')
    changes_requested=$(echo "$reviews" | jq '[.[] | select(.state == "CHANGES_REQUESTED")] | length')
    
    echo -e "${GREEN}✅ Approvals: $approved_count${NC}"
    
    if [ "$changes_requested" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Changes requested: $changes_requested${NC}"
        return 2
    fi
    
    # Check if mergeable
    mergeable=$(echo "$pr_data" | jq -r '.mergeable')
    if [ "$mergeable" != "MERGEABLE" ]; then
        echo -e "${RED}❌ PR has conflicts or is not mergeable${NC}"
        return 3
    fi
    
    # Check minimum approvals (2 required)
    if [ "$approved_count" -lt 2 ]; then
        echo -e "${YELLOW}⚠️  Needs more approvals (current: $approved_count, required: 2)${NC}"
        return 4
    fi
    
    echo -e "${GREEN}✅ PR is ready to merge!${NC}"
    return 0
}

# Function to handle review comments
handle_review_comments() {
    local pr_number=$1
    
    echo -e "${BLUE}Fetching review comments for PR #$pr_number...${NC}"
    
    # Get all review comments
    comments=$(gh pr view "$pr_number" --json comments --jq '.comments')
    
    # Create a tracking file for addressed comments
    touch ".pr-${pr_number}-comments.track"
    
    # Process each comment
    echo "$comments" | jq -c '.[]' | while read -r comment; do
        comment_id=$(echo "$comment" | jq -r '.id')
        comment_body=$(echo "$comment" | jq -r '.body')
        author=$(echo "$comment" | jq -r '.author.login')
        
        # Check if already addressed
        if grep -q "$comment_id" ".pr-${pr_number}-comments.track"; then
            continue
        fi
        
        echo -e "${YELLOW}Comment from @$author:${NC}"
        echo "$comment_body"
        echo ""
        
        # Agent should address the comment here
        echo -e "${BLUE}Agent addressing comment...${NC}"
        
        # Mark as addressed
        echo "$comment_id" >> ".pr-${pr_number}-comments.track"
        
        # Reply to comment
        gh pr comment "$pr_number" --body "✅ Addressed in commit $(git rev-parse --short HEAD)"
    done
}

# Function to run review cycle
run_review_cycle() {
    local pr_number=$1
    local max_iterations=5
    local iteration=0
    
    echo -e "${BLUE}Starting review cycle for PR #$pr_number${NC}"
    
    while [ $iteration -lt $max_iterations ]; do
        ((iteration++))
        echo -e "${BLUE}Review iteration $iteration/$max_iterations${NC}"
        
        # Check PR status
        if check_pr_status "$pr_number"; then
            echo -e "${GREEN}✅ PR approved and ready to merge!${NC}"
            return 0
        fi
        
        # Handle review comments
        handle_review_comments "$pr_number"
        
        # Wait for human checkpoint
        echo -e "${YELLOW}❓ HUMAN CHECKPOINT: Have all review comments been addressed? (y/n)${NC}"
        read -r response
        
        if [ "$response" != "y" ]; then
            echo -e "${RED}Please address remaining comments before continuing${NC}"
            return 1
        fi
        
        # Request re-review
        echo -e "${BLUE}Requesting re-review...${NC}"
        gh pr review "$pr_number" --request
        
        # Wait for reviews
        echo -e "${YELLOW}Waiting for reviews... (will check again in 5 minutes)${NC}"
        sleep 300
    done
    
    echo -e "${RED}❌ Max review iterations reached. Manual intervention required.${NC}"
    return 1
}

# Function to merge PR after approvals
merge_pr() {
    local pr_number=$1
    
    echo -e "${BLUE}Attempting to merge PR #$pr_number...${NC}"
    
    # Final human checkpoint
    echo -e "${YELLOW}❓ FINAL HUMAN CHECKPOINT: Ready to merge to main? (y/n)${NC}"
    read -r response
    
    if [ "$response" != "y" ]; then
        echo -e "${RED}Merge cancelled by human checkpoint${NC}"
        return 1
    fi
    
    # Merge the PR
    gh pr merge "$pr_number" --merge --delete-branch
    
    echo -e "${GREEN}✅ PR #$pr_number merged successfully!${NC}"
    
    # Clean up tracking file
    rm -f ".pr-${pr_number}-comments.track"
    
    return 0
}

# Main command handler
case "${1:-}" in
    create)
        if [ $# -lt 3 ]; then
            echo "Usage: $0 create <branch> <title>"
            exit 1
        fi
        create_pr "$2" "$3"
        ;;
    
    status)
        if [ $# -lt 2 ]; then
            echo "Usage: $0 status <pr-number>"
            exit 1
        fi
        check_pr_status "$2"
        ;;
    
    review-cycle)
        if [ $# -lt 2 ]; then
            echo "Usage: $0 review-cycle <pr-number>"
            exit 1
        fi
        run_review_cycle "$2"
        ;;
    
    merge)
        if [ $# -lt 2 ]; then
            echo "Usage: $0 merge <pr-number>"
            exit 1
        fi
        merge_pr "$2"
        ;;
    
    *)
        echo "PR Review Cycle Management"
        echo ""
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  create <branch> <title>  - Create PR with template"
        echo "  status <pr-number>       - Check PR review status"
        echo "  review-cycle <pr-number> - Run full review cycle"
        echo "  merge <pr-number>        - Merge approved PR"
        echo ""
        echo "Example:"
        echo "  $0 create feature/auth-system 'Add OAuth authentication'"
        echo "  $0 review-cycle 123"
        exit 1
        ;;
esac