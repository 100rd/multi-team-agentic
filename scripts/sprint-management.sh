#!/bin/bash
# Sprint Management - Enterprise Agile Ceremonies

set -euo pipefail

# Configuration
SPRINT_DIR=".sprints"
CURRENT_SPRINT_FILE="$SPRINT_DIR/current-sprint.json"
BACKLOG_FILE="$SPRINT_DIR/product-backlog.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Ensure sprint directory exists
mkdir -p "$SPRINT_DIR"

# Initialize sprint data if not exists
init_sprint_data() {
    if [ ! -f "$BACKLOG_FILE" ]; then
        echo '{"stories": []}' > "$BACKLOG_FILE"
    fi
    
    if [ ! -f "$CURRENT_SPRINT_FILE" ]; then
        echo '{"sprint_number": 0, "status": "not_started", "stories": [], "velocity": 0}' > "$CURRENT_SPRINT_FILE"
    fi
}

# Sprint planning ceremony
sprint_planning() {
    echo -e "${PURPLE}🏃 SPRINT PLANNING CEREMONY${NC}"
    echo "=========================="
    
    # Get sprint number
    local sprint_num=$(($(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE") + 1))
    echo -e "${BLUE}Planning Sprint #$sprint_num${NC}"
    
    # Calculate velocity (average of last 3 sprints)
    local velocity=20  # Default for first sprint
    if [ $sprint_num -gt 1 ]; then
        velocity=$(calculate_velocity)
    fi
    echo -e "${GREEN}Team velocity: $velocity story points${NC}"
    
    # Human checkpoint
    echo -e "\n${YELLOW}❓ HUMAN CHECKPOINT: Product Owner, please prioritize the backlog${NC}"
    echo "Press Enter when backlog is ready..."
    read -r
    
    # Select stories for sprint
    local total_points=0
    local selected_stories='[]'
    
    echo -e "\n${BLUE}Selecting stories based on velocity...${NC}"
    
    # This would be interactive in real implementation
    # For now, simulate story selection
    cat > "$SPRINT_DIR/sprint-$sprint_num-plan.json" << EOF
{
    "sprint_number": $sprint_num,
    "start_date": "$(date -I)",
    "end_date": "$(date -I -d '+2 weeks')",
    "velocity_target": $velocity,
    "sprint_goal": "Complete user authentication feature",
    "stories": [
        {
            "id": "US-101",
            "title": "User login with email",
            "points": 5,
            "acceptance_criteria": ["User can login", "Session is created", "Errors are handled"],
            "assigned_to": "backend-engineer"
        },
        {
            "id": "US-102", 
            "title": "Password reset flow",
            "points": 8,
            "acceptance_criteria": ["Email sent", "Token validates", "Password updates"],
            "assigned_to": "full-stack-engineer"
        },
        {
            "id": "US-103",
            "title": "Login UI components", 
            "points": 3,
            "acceptance_criteria": ["Responsive design", "Form validation", "Error display"],
            "assigned_to": "frontend-engineer"
        }
    ],
    "total_points": 16,
    "risks": ["OAuth provider integration complexity", "Email service setup"],
    "dependencies": ["Email service contract", "UI mockups approval"]
}
EOF
    
    echo -e "${GREEN}✅ Sprint plan created${NC}"
    
    # Team commitment
    echo -e "\n${YELLOW}❓ HUMAN CHECKPOINT: Team, do you commit to this sprint? (y/n)${NC}"
    read -r commitment
    
    if [ "$commitment" != "y" ]; then
        echo -e "${RED}Sprint planning cancelled. Please adjust and retry.${NC}"
        return 1
    fi
    
    # Update current sprint
    jq --arg sn "$sprint_num" '.sprint_number = ($sn | tonumber) | .status = "active"' "$CURRENT_SPRINT_FILE" > tmp.json
    mv tmp.json "$CURRENT_SPRINT_FILE"
    
    echo -e "${GREEN}✅ Sprint #$sprint_num is now active!${NC}"
    
    # Create sprint board
    create_sprint_board "$sprint_num"
}

# Daily standup
daily_standup() {
    echo -e "${PURPLE}📅 DAILY STANDUP${NC}"
    echo "================"
    echo "Date: $(date)"
    
    local sprint_num=$(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE")
    echo -e "${BLUE}Sprint #$sprint_num - Day $(calculate_sprint_day)${NC}\n"
    
    # Get updates from each agent
    echo -e "${GREEN}Backend Engineer Agent:${NC}"
    echo "Yesterday: Implemented JWT token generation"
    echo "Today: Working on session management"
    echo "Blockers: None"
    echo ""
    
    echo -e "${GREEN}Frontend Engineer Agent:${NC}"
    echo "Yesterday: Created login form component"
    echo "Today: Adding form validation"
    echo "Blockers: Waiting for API endpoint documentation"
    echo ""
    
    echo -e "${GREEN}QA Engineer Agent:${NC}"
    echo "Yesterday: Wrote test cases for login flow"
    echo "Today: Setting up automated tests"
    echo "Blockers: Test environment not ready"
    echo ""
    
    # Human checkpoint
    echo -e "${YELLOW}❓ HUMAN CHECKPOINT: Any impediments to discuss? (y/n)${NC}"
    read -r impediments
    
    if [ "$impediments" = "y" ]; then
        echo "Please describe the impediments:"
        read -r impediment_desc
        echo "$impediment_desc" >> "$SPRINT_DIR/sprint-$sprint_num-impediments.log"
    fi
    
    # Update burndown
    update_burndown
}

# Sprint review
sprint_review() {
    echo -e "${PURPLE}🎯 SPRINT REVIEW${NC}"
    echo "================"
    
    local sprint_num=$(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE")
    echo -e "${BLUE}Sprint #$sprint_num Review${NC}\n"
    
    # Demo completed features
    echo -e "${GREEN}Completed User Stories:${NC}"
    echo "1. US-101: User login with email ✅"
    echo "   - Demo: [Shows login flow]"
    echo "2. US-103: Login UI components ✅"
    echo "   - Demo: [Shows responsive UI]"
    echo ""
    
    echo -e "${YELLOW}Incomplete Stories:${NC}"
    echo "1. US-102: Password reset flow (70% complete)"
    echo "   - Carried over to next sprint"
    echo ""
    
    # Stakeholder feedback
    echo -e "${YELLOW}❓ HUMAN CHECKPOINT: Product Owner, please provide feedback${NC}"
    read -r feedback
    
    echo "$feedback" >> "$SPRINT_DIR/sprint-$sprint_num-feedback.log"
    
    # Update velocity
    local completed_points=8  # In real implementation, calculate from completed stories
    echo -e "${GREEN}Velocity this sprint: $completed_points points${NC}"
}

# Sprint retrospective
sprint_retrospective() {
    echo -e "${PURPLE}🔄 SPRINT RETROSPECTIVE${NC}"
    echo "======================"
    
    local sprint_num=$(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE")
    
    # Collect feedback
    echo -e "${BLUE}What went well?${NC}"
    echo "- Automated testing saved time"
    echo "- Good collaboration between agents"
    echo "- Clear acceptance criteria"
    echo ""
    
    echo -e "${YELLOW}What could be improved?${NC}"
    echo "- API documentation was delayed"
    echo "- Test environment setup took too long"
    echo "- Need better estimation for complex stories"
    echo ""
    
    echo -e "${RED}Action items:${NC}"
    echo "1. Set up API documentation automation"
    echo "2. Create test environment provisioning script"
    echo "3. Add spike stories for complex features"
    echo ""
    
    # Human input
    echo -e "${YELLOW}❓ HUMAN CHECKPOINT: Any additional feedback? (y/n)${NC}"
    read -r additional
    
    if [ "$additional" = "y" ]; then
        echo "Please provide feedback:"
        read -r retro_feedback
        echo "$retro_feedback" >> "$SPRINT_DIR/sprint-$sprint_num-retrospective.log"
    fi
    
    # Close sprint
    close_sprint "$sprint_num"
}

# Create sprint board
create_sprint_board() {
    local sprint_num=$1
    
    cat > "$SPRINT_DIR/sprint-$sprint_num-board.md" << EOF
# Sprint $sprint_num Board

## Sprint Goal
Complete user authentication feature

## Stories

| ID | Story | Points | Status | Assigned To |
|----|-------|--------|---------|-------------|
| US-101 | User login with email | 5 | In Progress | backend-engineer |
| US-102 | Password reset flow | 8 | To Do | full-stack-engineer |
| US-103 | Login UI components | 3 | In Progress | frontend-engineer |

## Burndown
\`\`\`
Points
16 |*
14 | *
12 |  *
10 |   *
8  |    *
6  |     *
4  |      *
2  |       *
0  |________*
   1 2 3 4 5 6 7 8 9 10 Days
\`\`\`

## Impediments
- None currently

## Daily Updates
Check daily-standup.log for details
EOF
}

# Update burndown chart
update_burndown() {
    local sprint_num=$(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE")
    local day=$(calculate_sprint_day)
    
    # In real implementation, calculate remaining points
    local remaining_points=$((16 - day * 2))  # Simplified
    
    echo "Day $day: $remaining_points points remaining" >> "$SPRINT_DIR/sprint-$sprint_num-burndown.log"
}

# Calculate sprint day
calculate_sprint_day() {
    # Simplified - in real implementation, calculate from sprint start date
    echo 3
}

# Calculate velocity
calculate_velocity() {
    # Average of last 3 sprints - simplified
    echo 20
}

# Close sprint
close_sprint() {
    local sprint_num=$1
    
    # Archive sprint data
    mv "$SPRINT_DIR/sprint-$sprint_num-"* "$SPRINT_DIR/archived/"
    
    # Update current sprint status
    jq '.status = "completed"' "$CURRENT_SPRINT_FILE" > tmp.json
    mv tmp.json "$CURRENT_SPRINT_FILE"
    
    echo -e "${GREEN}✅ Sprint #$sprint_num closed${NC}"
}

# Generate sprint report
generate_sprint_report() {
    local sprint_num=$(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE")
    
    cat > "$SPRINT_DIR/sprint-$sprint_num-report.md" << EOF
# Sprint $sprint_num Report

## Summary
- **Duration**: $(date -I -d '-2 weeks') to $(date -I)
- **Velocity Target**: 20 points
- **Velocity Achieved**: 8 points
- **Stories Completed**: 2/3

## Completed Stories
- US-101: User login with email (5 points)
- US-103: Login UI components (3 points)

## Incomplete Stories
- US-102: Password reset flow (8 points) - 70% complete

## Key Metrics
- **Burndown Trend**: On track until day 8
- **Defects Found**: 3 (all resolved)
- **Code Coverage**: 85%
- **PR Cycle Time**: Average 2.5 days

## Impediments Encountered
- Test environment provisioning delay
- API documentation lag

## Action Items for Next Sprint
1. Automate test environment setup
2. Implement API doc generation
3. Better story estimation process

## Team Health
- **Morale**: Good
- **Collaboration**: Excellent
- **Process Adherence**: 90%
EOF
    
    echo -e "${GREEN}✅ Sprint report generated${NC}"
}

# Main command handler
init_sprint_data

case "${1:-}" in
    planning)
        sprint_planning
        ;;
    
    standup)
        daily_standup
        ;;
    
    review)
        sprint_review
        ;;
    
    retrospective)
        sprint_retrospective
        ;;
    
    report)
        generate_sprint_report
        ;;
    
    status)
        sprint_num=$(jq -r '.sprint_number' "$CURRENT_SPRINT_FILE")
        status=$(jq -r '.status' "$CURRENT_SPRINT_FILE")
        echo -e "${BLUE}Current Sprint: #$sprint_num${NC}"
        echo -e "${GREEN}Status: $status${NC}"
        ;;
    
    *)
        echo "Sprint Management - Agile Ceremonies"
        echo ""
        echo "Usage: $0 <ceremony>"
        echo ""
        echo "Ceremonies:"
        echo "  planning      - Run sprint planning"
        echo "  standup       - Daily standup"
        echo "  review        - Sprint review"
        echo "  retrospective - Sprint retrospective"
        echo "  report        - Generate sprint report"
        echo "  status        - Current sprint status"
        echo ""
        echo "Example:"
        echo "  $0 planning"
        echo "  $0 standup"
        exit 1
        ;;
esac