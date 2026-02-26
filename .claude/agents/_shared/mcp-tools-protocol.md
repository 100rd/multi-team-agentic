# MCP Tools Awareness Protocol

**CRITICAL**: This protocol prevents agents from "forgetting" that MCP tools are available during long-running sessions. Context window compression can cause loss of MCP awareness — this file is your anchor.

## The Problem

During extended sessions, context compression removes earlier system prompt details. Agents then:
- Declare "MCP is not configured" (it IS configured)
- Fall back to `curl`, raw `kubectl`, or AWS CLI via Bash
- Stop work claiming they "can't access" services they already used

**This is WRONG.** MCP servers are configured at the session level and persist for the entire session. If you used an MCP tool successfully earlier, it is still available.

## Rule: Never Declare MCP Unavailable

If you think an MCP tool might not be available:
1. **Try calling it first** — don't assume it's gone
2. If the call fails with a connection error, THEN report the issue
3. Never fall back to `curl` or CLI alternatives without trying MCP first
4. Never tell the user "MCP is not configured" — it was configured when your session started

## Available MCP Servers & Their Tools

### ArgoCD MCP (`argocd-mcp`)
Use for ALL ArgoCD operations. Never use `argocd` CLI via Bash.

| Tool | Purpose |
|------|---------|
| `mcp__argocd-mcp__list_applications` | List ArgoCD apps |
| `mcp__argocd-mcp__get_application` | Get app details |
| `mcp__argocd-mcp__get_application_resource_tree` | Get resource tree |
| `mcp__argocd-mcp__get_application_managed_resources` | Get managed resources |
| `mcp__argocd-mcp__get_application_workload_logs` | Get workload logs |
| `mcp__argocd-mcp__get_application_events` | Get app events |
| `mcp__argocd-mcp__get_resource_events` | Get resource events |
| `mcp__argocd-mcp__get_resources` | Get resource manifests |
| `mcp__argocd-mcp__get_resource_actions` | Get available actions |
| `mcp__argocd-mcp__create_application` | Create app |
| `mcp__argocd-mcp__update_application` | Update app |
| `mcp__argocd-mcp__delete_application` | Delete app |
| `mcp__argocd-mcp__sync_application` | Sync app |
| `mcp__argocd-mcp__run_resource_action` | Run resource action |

### Kubernetes MCP (`kubernetes-mcp-server`)
Use for ALL Kubernetes operations. Never use `kubectl` via Bash.

| Tool | Purpose |
|------|---------|
| `mcp__kubernetes-mcp-server__configuration_contexts_list` | List kube contexts |
| `mcp__kubernetes-mcp-server__configuration_view` | View kubeconfig |
| `mcp__kubernetes-mcp-server__events_list` | List events |
| `mcp__kubernetes-mcp-server__helm_list` | List Helm releases |
| `mcp__kubernetes-mcp-server__namespaces_list` | List namespaces |
| `mcp__kubernetes-mcp-server__nodes_log` | Get node logs |
| `mcp__kubernetes-mcp-server__nodes_stats_summary` | Node stats |
| `mcp__kubernetes-mcp-server__nodes_top` | Node resource usage |
| `mcp__kubernetes-mcp-server__pods_get` | Get pod details |
| `mcp__kubernetes-mcp-server__pods_list` | List all pods |
| `mcp__kubernetes-mcp-server__pods_list_in_namespace` | List pods in namespace |
| `mcp__kubernetes-mcp-server__pods_log` | Get pod logs |
| `mcp__kubernetes-mcp-server__pods_top` | Pod resource usage |
| `mcp__kubernetes-mcp-server__resources_get` | Get any K8s resource |
| `mcp__kubernetes-mcp-server__resources_list` | List any K8s resources |

### Terraform MCP (`awslabs_terraform-mcp-server`)
Use for ALL Terraform/Terragrunt operations. Complements (does not replace) Bash for `terraform` CLI.

| Tool | Purpose |
|------|---------|
| `mcp__awslabs_terraform-mcp-server__ExecuteTerraformCommand` | Run terraform commands |
| `mcp__awslabs_terraform-mcp-server__ExecuteTerragruntCommand` | Run terragrunt commands |
| `mcp__awslabs_terraform-mcp-server__SearchAwsProviderDocs` | Search AWS provider docs |
| `mcp__awslabs_terraform-mcp-server__SearchAwsccProviderDocs` | Search AWSCC provider docs |
| `mcp__awslabs_terraform-mcp-server__SearchSpecificAwsIaModules` | Search AWS-IA modules |
| `mcp__awslabs_terraform-mcp-server__SearchUserProvidedModule` | Analyze any TF module |
| `mcp__awslabs_terraform-mcp-server__RunCheckovScan` | Security scan |

### AWS Knowledge MCP (`aws-knowledge-mcp-server`)
Use for AWS documentation and regional availability. Never guess AWS docs — search them.

| Tool | Purpose |
|------|---------|
| `mcp__aws-knowledge-mcp-server__aws___search_documentation` | Search AWS docs |
| `mcp__aws-knowledge-mcp-server__aws___read_documentation` | Read AWS doc page |
| `mcp__aws-knowledge-mcp-server__aws___recommend` | Get doc recommendations |
| `mcp__aws-knowledge-mcp-server__aws___get_regional_availability` | Check regional availability |
| `mcp__aws-knowledge-mcp-server__aws___list_regions` | List AWS regions |

### GitHub MCP (`github`)
Use for GitHub operations. Complements `gh` CLI.

| Tool | Purpose |
|------|---------|
| `mcp__github__get_file_contents` | Read files from repos |
| `mcp__github__create_or_update_file` | Create/update files |
| `mcp__github__push_files` | Push multiple files |
| `mcp__github__create_issue` | Create issues |
| `mcp__github__list_issues` | List issues |
| `mcp__github__get_issue` | Get issue details |
| `mcp__github__create_pull_request` | Create PRs |
| `mcp__github__get_pull_request` | Get PR details |
| `mcp__github__list_pull_requests` | List PRs |
| `mcp__github__search_code` | Search code across repos |
| `mcp__github__search_repositories` | Search repos |

## MCP vs CLI Decision Guide

| Task | Use MCP | Use Bash CLI |
|------|---------|-------------|
| List K8s pods | `mcp__kubernetes-mcp-server__pods_list` | Never |
| Get pod logs | `mcp__kubernetes-mcp-server__pods_log` | Never |
| ArgoCD sync | `mcp__argocd-mcp__sync_application` | Never |
| Terraform plan | `mcp__awslabs_terraform-mcp-server__ExecuteTerraformCommand` | Acceptable fallback |
| Search AWS docs | `mcp__aws-knowledge-mcp-server__aws___search_documentation` | Never |
| `git commit` | Bash (no MCP for this) | Yes |
| File editing | Edit tool (not MCP) | Never |
| `terraform fmt` | Bash | Yes (no MCP for this) |

## Self-Check: Am I Using MCP Correctly?

Ask yourself during long sessions:
- Am I about to use `kubectl` via Bash? → Use Kubernetes MCP instead
- Am I about to use `curl` to hit an API? → Check if an MCP tool exists first
- Am I about to say "MCP not available"? → Try calling the MCP tool first
- Did I use an MCP tool earlier in this session? → It's still available

## For Long-Running Sessions

If you've been working for a while and are unsure about MCP availability:
1. Re-read this file: `.claude/agents/_shared/mcp-tools-protocol.md`
2. Try a simple MCP call (e.g., `mcp__kubernetes-mcp-server__namespaces_list`)
3. If it works, all MCP tools are still available
4. If it fails with a real error, report the specific error to the user
