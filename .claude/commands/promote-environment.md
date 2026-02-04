---
name: promote-environment
description: Promote infrastructure changes through environments (dev → staging → prod) with validation gates
args: "<from-env> <to-env> [--skip-tests] [--force]"
---

# Environment Promotion Skill

Safely promote infrastructure changes through environment tiers with validation gates at each stage.

## Environment Hierarchy

```
dev → staging → prod
 │       │        │
 │       │        └── Production (requires approval)
 │       └── Staging (requires tests pass)
 └── Development (can apply freely)
```

## Arguments
- `from-env`: Source environment (dev, staging)
- `to-env`: Target environment (staging, prod)
- `--skip-tests`: Skip test validation (NOT recommended)
- `--force`: Force promotion (requires explicit justification)

## Promotion Rules

### dev → staging
**Requirements:**
- [ ] Terraform plan succeeds
- [ ] No security violations (Checkov/tfsec pass)
- [ ] Cost estimate within threshold
- [ ] Drift check passes in dev
- [ ] Basic integration tests pass

### staging → prod
**Requirements:**
- [ ] All staging requirements pass
- [ ] Staging deployment stable for X hours
- [ ] Performance tests pass
- [ ] Security review completed
- [ ] Change ticket created
- [ ] Human approval obtained
- [ ] Rollback plan documented

## Workflow

### Step 1: Verify Promotion Path

```bash
# Valid promotion paths
VALID_PATHS=("dev:staging" "staging:prod")

if [[ ! " ${VALID_PATHS[@]} " =~ " ${FROM_ENV}:${TO_ENV} " ]]; then
  echo "❌ Invalid promotion path: $FROM_ENV → $TO_ENV"
  echo "   Valid paths: dev→staging, staging→prod"
  exit 1
fi
```

### Step 2: Pre-flight Checks

```bash
echo "🔍 Running pre-flight checks for $FROM_ENV → $TO_ENV promotion..."

# Check source environment is healthy
cd "environments/$FROM_ENV"
terraform plan -detailed-exitcode
if [ $? -eq 1 ]; then
  echo "❌ Source environment has errors"
  exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Uncommitted changes detected. Commit before promoting."
  exit 1
fi
```

### Step 3: Run Validation Gates

```bash
echo "🚦 Running validation gates..."

# Gate 1: Security Scan
echo "  [1/5] Security scan..."
checkov -d . --quiet
if [ $? -ne 0 ]; then
  echo "❌ Security scan failed"
  exit 1
fi
echo "  ✅ Security scan passed"

# Gate 2: Cost Estimate
echo "  [2/5] Cost estimate..."
infracost breakdown --path "environments/$TO_ENV" --format json > /tmp/cost.json
COST_DIFF=$(jq -r '.diffTotalMonthlyCost' /tmp/cost.json)
if (( $(echo "$COST_DIFF > 500" | bc -l) )); then
  echo "  ⚠️ Cost increase: \$$COST_DIFF/month - requires approval"
fi
echo "  ✅ Cost estimate complete"

# Gate 3: Drift Check
echo "  [3/5] Drift detection..."
cd "environments/$FROM_ENV"
terraform plan -detailed-exitcode > /dev/null 2>&1
DRIFT_CODE=$?
if [ $DRIFT_CODE -eq 2 ]; then
  echo "  ⚠️ Drift detected in $FROM_ENV - resolve before promoting"
  exit 1
fi
echo "  ✅ No drift detected"

# Gate 4: Tests
echo "  [4/5] Running tests..."
if [ "$SKIP_TESTS" != "true" ]; then
  # Run integration/smoke tests
  ./scripts/test-environment.sh "$FROM_ENV"
  if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
  fi
fi
echo "  ✅ Tests passed"

# Gate 5: Best Practices
echo "  [5/5] Best practices validation..."
tflint --recursive
echo "  ✅ Best practices check passed"
```

### Step 4: Generate Promotion Plan

```markdown
# Environment Promotion Plan

**From**: [from-env]
**To**: [to-env]
**Timestamp**: [ISO timestamp]
**Requested By**: [agent/user]

## Pre-flight Results

| Check | Status | Details |
|-------|--------|---------|
| Source Health | ✅ PASS | No errors |
| Security Scan | ✅ PASS | 0 violations |
| Cost Estimate | ✅ PASS | +$X/month |
| Drift Check | ✅ PASS | No drift |
| Tests | ✅ PASS | X/Y passed |
| Best Practices | ✅ PASS | 0 warnings |

## Changes to Apply

### Resources to Create
- aws_instance.new_server

### Resources to Modify
- aws_security_group.app (ingress rules)

### Resources to Destroy
- (none)

## Risk Assessment

- **Blast Radius**: [Low/Medium/High]
- **Rollback Complexity**: [Simple/Moderate/Complex]
- **Downtime Expected**: [None/Brief/Extended]

## Rollback Plan

1. Revert to previous Terraform state
2. Run: `terraform apply -target=<resources>`
3. Verify services restored

## Approval Required

[For staging→prod only]

⚠️ PRODUCTION PROMOTION
━━━━━━━━━━━━━━━━━━━━━━━
This will apply changes to PRODUCTION.

Do you approve? (y/n):
```

### Step 5: Execute Promotion

```bash
if [ "$TO_ENV" == "prod" ]; then
  echo ""
  echo "⚠️ PRODUCTION PROMOTION REQUIRES APPROVAL"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  # Approval must be obtained before proceeding
  exit 2  # Signal that approval is needed
fi

# For non-prod, proceed
cd "environments/$TO_ENV"

echo "📋 Creating Terraform plan..."
terraform plan -out=promotion.tfplan

echo "🚀 Applying changes to $TO_ENV..."
terraform apply promotion.tfplan

echo "✅ Promotion complete: $FROM_ENV → $TO_ENV"
```

### Step 6: Post-Promotion Validation

```bash
echo "🔍 Running post-promotion validation..."

# Health check
./scripts/health-check.sh "$TO_ENV"

# Smoke tests
./scripts/smoke-tests.sh "$TO_ENV"

# Update deployment record
echo "📝 Logging promotion to history..."
```

### Step 7: Log to History

```markdown
## [TIMESTAMP] promote-environment: Promoted from dev to staging

**Action**: deployment
**Category**: infrastructure

### Promotion Summary
- Source: dev
- Target: staging
- Resources changed: X

### Validation Results
- Security: PASS
- Cost: +$Y/month
- Tests: PASS

### Changes Applied
[List of changes]

### Outcome
✅ Completed - Promotion successful

**Tags**: #promotion #infrastructure #staging
```

## Production Safeguards

When promoting to production:

1. **Require Change Ticket**
   ```bash
   if [ -z "$CHANGE_TICKET" ]; then
     echo "❌ Production promotion requires a change ticket number"
     echo "   Usage: /promote-environment staging prod --ticket CHANGE-123"
     exit 1
   fi
   ```

2. **Require Approval**
   - Must have explicit human approval
   - Logged with approver name and timestamp

3. **Maintenance Window Check**
   ```bash
   # Check if within maintenance window
   CURRENT_HOUR=$(date +%H)
   if [ $CURRENT_HOUR -lt 2 ] || [ $CURRENT_HOUR -gt 6 ]; then
     echo "⚠️ Outside maintenance window (02:00-06:00 UTC)"
     echo "   Production changes require --force flag outside this window"
   fi
   ```

4. **Rollback Ready**
   - Previous state saved
   - Rollback commands documented
   - Monitoring alerts configured

## Example Usage

```bash
# Promote dev to staging
/promote-environment dev staging

# Promote staging to prod (requires approval)
/promote-environment staging prod --ticket CHANGE-456

# Force promotion (with justification)
/promote-environment staging prod --force "Critical security patch"
```
