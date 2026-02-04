# Deployment Workflow

This workflow manages the deployment process from development to production with proper checks and rollback procedures.

## Prerequisites
- Feature development complete
- All tests passing
- Code review approved
- Documentation updated

## Deployment Strategies

### Step 1: Choose Deployment Strategy
**"How would you like to deploy this feature?"**

1️⃣ **Blue-Green Deployment**
   - Zero downtime
   - Easy rollback
   - Resource intensive

2️⃣ **Rolling Deployment**
   - Gradual update
   - Lower resource usage
   - Harder rollback

3️⃣ **Canary Release**
   - Test with small traffic %
   - Monitor before full rollout
   - Risk mitigation

4️⃣ **Feature Flag**
   - Deploy dark
   - Toggle when ready
   - Instant rollback

Press 1, 2, 3, or 4:

## Pre-Deployment Checklist

### Step 2: Automated Checks
Run all checks before proceeding:

```bash
# Run full test suite
npm test && npm run test:integration && npm run test:e2e

# Security scan
npm audit
snyk test

# Performance check
npm run lighthouse

# Build verification
npm run build
```

### Step 3: Manual Verification
**"Pre-deployment checklist:"**

- [ ] All tests passing?
- [ ] Security scan clean?
- [ ] Performance acceptable?
- [ ] Database migrations ready?
- [ ] Rollback plan prepared?
- [ ] Monitoring alerts configured?
- [ ] Team notified?

**⚠️ CRITICAL DECISION: Deploy to Production**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Feature: [Feature name]
Changes: [Summary of changes]
Risk Level: [Low/Medium/High]
Rollback Time: [Estimated time]

Do you approve deployment? (y/n):

## Deployment Stages

### Stage 1: Staging Deployment
**"First, deploying to staging..."**

1. **Deploy to Staging**
   ```bash
   # For containerized apps
   kubectl apply -f k8s/staging/
   
   # For traditional apps
   ./deploy.sh staging
   ```

2. **Smoke Tests**
   Run basic functionality tests
   Check critical paths

3. **Staging Sign-off**
   **"Staging deployment successful. Proceed to production?"**

### Stage 2: Production Deployment

Based on chosen strategy:

#### Blue-Green
```bash
# Deploy to green environment
./deploy.sh production-green

# Run health checks
./scripts/health-check.sh production-green

# Switch traffic
./scripts/switch-traffic.sh blue-to-green
```

#### Canary
```bash
# Deploy canary version
kubectl apply -f k8s/canary/

# Set initial traffic (5%)
kubectl patch virtualservice app --type merge -p '{"spec":{"http":[{"weight":5}]}}'

# Monitor metrics
watch -n 5 ./scripts/canary-metrics.sh
```

### Stage 3: Monitoring & Validation

**"Deployment in progress. Monitoring..."**

Track these metrics:
- Error rate
- Response time
- CPU/Memory usage
- User reports
- Business metrics

Create monitoring dashboard:
```markdown
## Deployment Monitor - [Feature Name]
Started: [Timestamp]
Status: In Progress

### Health Metrics
- Error Rate: 0.1% ✅
- Avg Response: 245ms ✅
- CPU Usage: 45% ✅
- Memory: 2.1GB ✅

### Business Metrics  
- Active Users: 1,234
- Transactions/min: 567
- Conversion Rate: 3.4%
```

### Stage 4: Progressive Rollout

For canary deployments:

**"Canary looks healthy. Increase traffic?"**

a) Yes, increase to 25%
b) Yes, increase to 50%  
c) Complete rollout (100%)
d) Hold at current %
e) Rollback

Monitor after each increase.

## Rollback Procedures

### Automatic Rollback Triggers
- Error rate > 5%
- Response time > 2s
- Health check failures
- Memory/CPU critical

### Manual Rollback
**"⚠️ Issue detected! Initiate rollback?"**

```bash
# Blue-Green rollback
./scripts/switch-traffic.sh green-to-blue

# Canary rollback
kubectl delete -f k8s/canary/

# Feature flag rollback
./scripts/feature-flag.sh disable [feature-name]
```

## Post-Deployment

### Step 1: Verification
**"Deployment complete! Running final checks..."**

- Production smoke tests
- User acceptance verification
- Performance benchmarks
- Security scan

### Step 2: Documentation
Update:
- Deployment log
- Version documentation
- Changelog
- Release notes

### Step 3: Notification
**"Who should be notified about this deployment?"**

Send notifications to:
- Team (Slack/Email)
- Stakeholders
- Status page
- Customers (if major feature)

### Step 4: Cleanup
- Remove old versions
- Clean up staging
- Archive deployment artifacts
- Update documentation

## Deployment Artifacts

Created during deployment:
```
project/deployments/
├── [date]-[feature]/
│   ├── deployment-plan.md
│   ├── pre-deployment-checklist.md
│   ├── deployment-log.txt
│   ├── monitoring-snapshot.json
│   ├── rollback-plan.md
│   └── post-mortem.md (if issues)
```

## Emergency Procedures

### Incident Response
1. **Assess Impact**
   - User impact %
   - Feature affected
   - Data integrity

2. **Immediate Actions**
   - Rollback if critical
   - Scale resources if needed
   - Enable maintenance mode

3. **Communication**
   - Update status page
   - Notify on-call
   - Stakeholder updates

### Post-Incident
Create `project/deployments/[date]/incident-report.md`:
- Timeline
- Root cause
- Impact assessment
- Remediation steps
- Prevention measures

## Success Criteria
- ✅ Deployed successfully
- ✅ All health checks passing
- ✅ No increase in errors
- ✅ Performance maintained
- ✅ Users notified
- ✅ Documentation updated

## Next Steps
After successful deployment:

1️⃣ **Monitor for 24h** - Watch metrics closely
2️⃣ **Gather feedback** - User responses
3️⃣ **Plan next feature** - Back to PRD creation
4️⃣ **Retrospective** - What went well/poorly
5️⃣ **Celebrate!** - Team achievement