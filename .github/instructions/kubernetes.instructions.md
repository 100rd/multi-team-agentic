---
applyTo: "**/k8s/**/*.yaml,**/k8s/**/*.yml,**/kubernetes/**/*.yaml,**/kubernetes/**/*.yml,**/deploy/**/*.yaml,**/helm/**/*.yaml"
---

## Kubernetes Manifest Standards

### Resource Definitions
- Always specify `apiVersion` and `kind`
- Use namespaces for all resources (no default namespace)
- Set resource requests AND limits for all containers
- Include liveness and readiness probes
- Use `apps/v1` for Deployments, StatefulSets, DaemonSets

### Security
- Never run containers as root (`runAsNonRoot: true`)
- Drop all capabilities, add only what's needed
- Use read-only root filesystem where possible
- Set `allowPrivilegeEscalation: false`
- Use Network Policies for pod-to-pod traffic control
- Store secrets in external secrets managers, not in manifests

### Labels & Annotations
```yaml
metadata:
  labels:
    app.kubernetes.io/name: <app-name>
    app.kubernetes.io/version: <version>
    app.kubernetes.io/component: <component>
    app.kubernetes.io/part-of: <system>
    app.kubernetes.io/managed-by: <tool>
```

### Pod Security
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault
containers:
  - securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
```

### Health Checks
- `livenessProbe`: Restart container if unhealthy
- `readinessProbe`: Remove from service if not ready
- `startupProbe`: For slow-starting containers
- Set appropriate `initialDelaySeconds`, `periodSeconds`, `failureThreshold`

### Resource Management
```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### Deployment Strategy
- Use `RollingUpdate` with `maxUnavailable: 0` for zero-downtime
- Set `minReadySeconds` to catch quick crashes
- Include `PodDisruptionBudget` for HA workloads

### Helm Charts
- Use `.Values` for all configurable fields
- Include sensible defaults in `values.yaml`
- Document values with comments
- Use `_helpers.tpl` for common labels and selectors
- Version charts semantically
