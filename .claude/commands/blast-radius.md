---
name: blast-radius
description: Analyze the blast radius and impact of Terraform changes before applying
args: "[path] [--graph] [--dependencies]"
---

# Blast Radius Analysis Skill

Analyze the potential impact of Terraform/Terragrunt changes before applying them. Identifies affected resources, downstream dependencies, and potential risks.

## Arguments
- `path`: Path to Terraform/Terragrunt directory
- `--graph`: Generate visual dependency graph
- `--dependencies`: Show downstream dependencies

## Purpose

Before running `terraform apply`, understand:
1. **What will change** - Resources created/modified/destroyed
2. **What depends on it** - Downstream resources affected
3. **What's the risk** - Potential for service disruption
4. **What's the rollback** - How to undo if needed

## Workflow

### Step 1: Generate Terraform Plan

```bash
cd "$PATH"
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
```

### Step 2: Extract Changes

```bash
# Parse plan JSON for changes
CREATES=$(jq '[.resource_changes[] | select(.change.actions | contains(["create"]))] | length' plan.json)
UPDATES=$(jq '[.resource_changes[] | select(.change.actions | contains(["update"]))] | length' plan.json)
DELETES=$(jq '[.resource_changes[] | select(.change.actions | contains(["delete"]))] | length' plan.json)
REPLACES=$(jq '[.resource_changes[] | select(.change.actions | contains(["delete", "create"]))] | length' plan.json)

echo "📊 Change Summary:"
echo "   Create:  $CREATES"
echo "   Update:  $UPDATES"
echo "   Delete:  $DELETES"
echo "   Replace: $REPLACES"
```

### Step 3: Identify High-Risk Changes

```bash
# High-risk resource types
HIGH_RISK_TYPES=(
  "aws_db_instance"
  "aws_rds_cluster"
  "aws_elasticache_cluster"
  "aws_iam_role"
  "aws_iam_policy"
  "aws_security_group"
  "aws_vpc"
  "aws_subnet"
  "aws_route_table"
  "aws_nat_gateway"
  "aws_internet_gateway"
  "aws_lb"
  "aws_autoscaling_group"
  "aws_ecs_service"
  "aws_eks_cluster"
  "aws_lambda_function"
)

# Check for high-risk changes
jq -r '.resource_changes[] | select(.change.actions != ["no-op"]) | "\(.type) \(.name) \(.change.actions)"' plan.json | while read line; do
  TYPE=$(echo $line | cut -d' ' -f1)
  if [[ " ${HIGH_RISK_TYPES[@]} " =~ " ${TYPE} " ]]; then
    echo "⚠️ HIGH RISK: $line"
  fi
done
```

### Step 4: Analyze Dependencies

```bash
# Generate dependency graph
terraform graph > graph.dot

# Find resources that depend on changed resources
for resource in $(jq -r '.resource_changes[] | select(.change.actions != ["no-op"]) | .address' plan.json); do
  echo "Dependencies for: $resource"
  grep -E "\"$resource\".*->|->.*\"$resource\"" graph.dot | head -10
done
```

### Step 5: Generate Blast Radius Report

```markdown
# Blast Radius Analysis Report

**Path**: [terraform-path]
**Timestamp**: [ISO timestamp]
**Total Resources in State**: [X]

## Executive Summary

| Metric | Count | Risk Level |
|--------|-------|------------|
| Resources to Create | X | Low |
| Resources to Update | Y | Medium |
| Resources to Delete | Z | High |
| Resources to Replace | W | Critical |
| **Total Blast Radius** | **N resources** | **[Level]** |

## Risk Classification

### 🔴 Critical Risk Changes (Immediate Review Required)
Resources that could cause significant outage:

| Resource | Action | Risk | Impact |
|----------|--------|------|--------|
| aws_rds_cluster.main | replace | Critical | Database downtime |
| aws_vpc.primary | update | Critical | Network disruption |

### 🟠 High Risk Changes
Resources that may cause service degradation:

| Resource | Action | Risk | Impact |
|----------|--------|------|--------|
| aws_security_group.app | update | High | Connection issues |
| aws_iam_role.lambda | update | High | Permission changes |

### 🟡 Medium Risk Changes
Changes with limited impact:

| Resource | Action | Risk | Impact |
|----------|--------|------|--------|
| aws_instance.worker | update | Medium | Restart required |

### 🟢 Low Risk Changes
Safe changes:

| Resource | Action | Risk | Impact |
|----------|--------|------|--------|
| aws_s3_bucket_policy.logs | update | Low | None |
| aws_cloudwatch_metric_alarm.cpu | create | Low | None |

## Dependency Analysis

### Upstream Dependencies (What this change depends on)
```
resource.a → resource.b → [CHANGED] resource.c
```

### Downstream Dependencies (What depends on this change)
```
[CHANGED] resource.c → resource.d → resource.e
                     → resource.f → resource.g
```

**Downstream Impact**: X resources may be affected

## Detailed Change Analysis

### 1. [Resource Address]

**Action**: [create/update/delete/replace]
**Type**: [aws_instance, etc.]

#### Before
```hcl
[current configuration]
```

#### After
```hcl
[new configuration]
```

#### Specific Changes
- `instance_type`: t3.medium → t3.large
- `tags.Environment`: dev → staging

#### Risk Assessment
- **Service Impact**: [None/Degraded/Outage]
- **Data Impact**: [None/Temporary/Permanent]
- **Recovery Time**: [Immediate/Minutes/Hours]

---

## Rollback Plan

### If changes fail:

1. **Immediate**:
   ```bash
   terraform plan -target=[specific-resource]
   ```

2. **Full Rollback**:
   ```bash
   # Revert to previous state
   git checkout HEAD~1 -- .
   terraform apply
   ```

3. **Manual Recovery**:
   [Steps for manual intervention if needed]

## Pre-Apply Checklist

- [ ] Reviewed all high-risk changes
- [ ] Verified downstream dependencies
- [ ] Confirmed rollback plan
- [ ] Notified affected teams
- [ ] Scheduled maintenance window (if needed)
- [ ] Backup verified (for data resources)

## Recommendations

1. **[High Priority]**: [Specific recommendation]
2. **[Consider]**: [Optional improvement]
3. **[Future]**: [Technical debt to address]
```

### Step 6: Visual Graph (Optional)

If `--graph` is specified:

```bash
# Generate SVG graph
terraform graph | dot -Tsvg > blast-radius.svg

# Or use blast-radius tool if available
blast-radius --serve .
```

### Step 7: Approval Gate

For high blast radius changes:

```
⚠️ HIGH BLAST RADIUS DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Changes affect: X resources
Risk level: [Critical/High]
Downstream impact: Y resources

This change requires human approval.

Affected services:
- Service A (database)
- Service B (API)
- Service C (workers)

Do you want to proceed? (y/n):
```

## Blast Radius Thresholds

| Metric | Low | Medium | High | Critical |
|--------|-----|--------|------|----------|
| Total changes | 1-5 | 6-15 | 16-30 | 30+ |
| Deletes/Replaces | 0 | 1-3 | 4-10 | 10+ |
| Database changes | 0 | 0 | 1 | 2+ |
| Network changes | 0-2 | 3-5 | 6-10 | 10+ |
| IAM changes | 0-3 | 4-10 | 11-20 | 20+ |

## Integration

This skill should be called:
1. Before any `terraform apply`
2. As part of PR review for infrastructure changes
3. During change management review
4. Before production deployments

## Example Usage

```bash
# Basic analysis
/blast-radius ./infrastructure/prod

# With dependency graph
/blast-radius ./infrastructure/prod --graph

# Show all downstream dependencies
/blast-radius ./infrastructure/prod --dependencies
```
