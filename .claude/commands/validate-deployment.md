---
name: validate-deployment
description: Validate infrastructure deployment - checks URL accessibility, DNS, SSL, Kubernetes status, and ArgoCD health
args: "[app-name] [--url URL] [--namespace NAMESPACE] [--full]"
---

# Deployment Validation Skill

You are executing the deployment validation workflow. This skill performs comprehensive infrastructure validation for deployed applications.

## Arguments
- `app-name`: The application name (ArgoCD application name or Kubernetes deployment name)
- `--url URL`: The application URL to validate (optional, will be inferred if possible)
- `--namespace NAMESPACE`: Kubernetes namespace (default: derived from app-name)
- `--full`: Run extended validation including performance benchmarks

## Validation Workflow

### Step 1: Gather Deployment Information

First, collect information about the deployment:

1. **If ArgoCD is available**, use the ArgoCD MCP tools:
   - Load ArgoCD tools via ToolSearch: `select:mcp__argocd-mcp__get_application`
   - Get application details including:
     - Sync status
     - Health status
     - Source repository and path
     - Destination namespace and server

2. **If Kubernetes is available**, use Kubernetes MCP tools:
   - Load Kubernetes tools via ToolSearch: `select:mcp__kubernetes-mcp-server__pods_list`
   - Get deployment information:
     - Pod status and readiness
     - Service endpoints
     - Recent events

### Step 2: URL/Endpoint Validation

If a URL is provided or can be determined, validate:

```bash
# Check HTTP status
curl -sI -o /dev/null -w "%{http_code}" --connect-timeout 10 "$URL"

# Check response time
curl -o /dev/null -s -w "Connect: %{time_connect}s, TTFB: %{time_starttransfer}s, Total: %{time_total}s\n" "$URL"

# Check health endpoint (common patterns)
curl -sS --connect-timeout 10 "$URL/health" || \
curl -sS --connect-timeout 10 "$URL/healthz" || \
curl -sS --connect-timeout 10 "$URL/api/health"
```

### Step 3: DNS Validation

```bash
# Extract domain from URL
DOMAIN=$(echo "$URL" | sed -E 's|https?://([^/]+).*|\1|')

# Check DNS resolution
dig +short "$DOMAIN"

# Check from multiple DNS servers for propagation
for dns in 8.8.8.8 1.1.1.1 9.9.9.9; do
  echo "DNS $dns: $(dig @$dns +short $DOMAIN | head -1)"
done
```

### Step 4: SSL/TLS Validation

```bash
# Check certificate validity and expiry
echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | \
  openssl x509 -noout -dates -subject

# Check certificate chain
echo | openssl s_client -showcerts -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | \
  grep -E "s:|i:" | head -10

# Calculate days until expiry
EXPIRY=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | \
  openssl x509 -noout -enddate | cut -d= -f2)
echo "Certificate expires: $EXPIRY"
```

### Step 5: Kubernetes Status Check

Use Kubernetes MCP tools or kubectl:

```bash
# Check pods
kubectl get pods -n "$NAMESPACE" -l "app=$APP_NAME" -o wide

# Check if all pods are ready
kubectl get pods -n "$NAMESPACE" -l "app=$APP_NAME" -o jsonpath='{range .items[*]}{.metadata.name}: {.status.phase} - Ready: {.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}'

# Check recent events for issues
kubectl get events -n "$NAMESPACE" --field-selector "involvedObject.name=$APP_NAME" --sort-by='.lastTimestamp' | tail -10

# Check service endpoints
kubectl get endpoints -n "$NAMESPACE" "$APP_NAME" -o jsonpath='{.subsets[*].addresses[*].ip}'
```

### Step 6: ArgoCD Status Check

Use ArgoCD MCP tools:

1. Load required tools:
   - `mcp__argocd-mcp__get_application`
   - `mcp__argocd-mcp__get_application_resource_tree`
   - `mcp__argocd-mcp__get_application_events`

2. Check application status:
   - Sync Status: Should be "Synced"
   - Health Status: Should be "Healthy"
   - Operation State: Should be "Succeeded"

3. Check resource tree for any degraded components

### Step 7: Generate Validation Report

Create a structured report:

```markdown
# Deployment Validation Report
**Application**: $APP_NAME
**Timestamp**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Overall Status**: [PASSED/FAILED]

## Quick Summary
| Category | Status | Notes |
|----------|--------|-------|
| URL Accessible | [✅/❌] | [HTTP status] |
| DNS Resolution | [✅/❌] | [resolved IPs] |
| SSL Certificate | [✅/❌] | [expiry info] |
| Kubernetes | [✅/❌] | [pod status] |
| ArgoCD | [✅/❌] | [sync/health] |

## Detailed Results
[Include detailed output from each check]

## Issues Found
[List any issues discovered]

## Escalation Required
[If failed, specify who to escalate to and why]
```

### Step 8: Handle Failures and Escalation

If any validation check fails:

1. **Document the failure** clearly with:
   - What check failed
   - Expected vs actual result
   - Error messages or logs
   - Timestamp

2. **Determine escalation target**:
   - **DevOps Engineer**: For Kubernetes issues, ArgoCD sync problems, resource issues
   - **Solution Architect**: For design/architecture issues, service dependencies
   - **Security Expert**: For SSL/TLS issues, security misconfigurations

3. **Create escalation task**:
   ```markdown
   ## Escalation: Deployment Validation Failed

   **Application**: $APP_NAME
   **Failed Check**: [specific check]
   **Assigned To**: [devops-engineer/solution-architect]
   **Priority**: [Critical/High/Medium]

   ### Issue Details
   [Detailed description]

   ### Required Action
   [What needs to be fixed]

   ### Re-validation
   After fixes are applied, re-run: `/validate-deployment $APP_NAME`
   ```

4. **Update PROJECT_STATUS.md** with the failure and escalation

## Extended Validation (--full flag)

When `--full` is specified, also run:

1. **Performance Benchmarks**:
   ```bash
   # Run multiple requests to check consistency
   for i in {1..10}; do
     curl -o /dev/null -s -w "%{time_total}\n" "$URL"
   done | awk '{sum+=$1} END {print "Avg:", sum/NR, "s"}'
   ```

2. **Security Headers Check**:
   ```bash
   curl -sI "$URL" | grep -iE "^(strict-transport|content-security|x-frame|x-content-type|x-xss)"
   ```

3. **Resource Utilization**:
   ```bash
   kubectl top pods -n "$NAMESPACE" -l "app=$APP_NAME"
   ```

## Example Usage

```
/validate-deployment my-app
/validate-deployment my-app --url https://my-app.example.com
/validate-deployment my-app --namespace production --full
```

## Success Criteria

Deployment is considered **PASSED** when:
- ✅ URL returns HTTP 200 (or expected status)
- ✅ Response time < 500ms
- ✅ DNS resolves correctly from multiple servers
- ✅ SSL certificate valid for > 7 days
- ✅ All Kubernetes pods are Ready
- ✅ ArgoCD shows Synced and Healthy
- ✅ No error events in last 10 minutes

Deployment is considered **FAILED** when any of the above criteria are not met.
