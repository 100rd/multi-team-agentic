# Auto-Approve Protocol

Defines what agents can and cannot do with Terraform operations, and what safety guardrails apply in all modes.

## Agent Execution Boundaries (CRITICAL)

Agents (including those in `/pipeline`, `/infra-team`, `/batch-issues`, and all autonomous modes) are **ONLY** permitted to run:

| Allowed | Purpose |
|---------|---------|
| `terraform plan` | Verify changes against real infrastructure |
| `terraform fmt` | Format code |
| `terraform validate` | Check syntax |
| `terraform init` | Initialize providers |
| `tflint` | Lint for best practices |
| `checkov` / `trivy` / `tfsec` | Security scanning |
| `terragrunt plan` | Verify Terragrunt changes |
| `terragrunt hcl format` | Format HCL |

Agents are **NEVER** permitted to run:

| Blocked | Reason |
|---------|--------|
| `terraform apply` | CI/CD only, from main branch after PR merge |
| `terraform destroy` | CI/CD only, from main branch after PR merge |
| `terragrunt apply` | CI/CD only, from main branch after PR merge |
| `terragrunt run-all apply` | CI/CD only, from main branch after PR merge |
| `terragrunt destroy` | CI/CD only, from main branch after PR merge |
| `terragrunt run-all destroy` | CI/CD only, from main branch after PR merge |

**This rule has NO exceptions, NO overrides, and NO auto-approve modes for apply/destroy.**

## Environment Rules for `terraform plan`

| Environment | terraform plan | terraform apply | terraform destroy |
|-------------|---------------|----------------|-------------------|
| **dev** | AUTO-APPROVED | BLOCKED (CI/CD only) | BLOCKED (CI/CD only) |
| **staging** | AUTO-APPROVED | BLOCKED (CI/CD only) | BLOCKED (CI/CD only) |
| **prod** | BLOCKED (human required) | BLOCKED (CI/CD only) | BLOCKED (CI/CD only) |
| **unknown** | CHECKPOINT | BLOCKED (CI/CD only) | BLOCKED (CI/CD only) |

### How Environment Is Detected

The hook script `scripts/terraform-env-check.sh` checks (in priority order):

1. **Working directory path**: `environments/dev/`, `environments/staging/`, `environments/prod/`
2. **Tfvars file name**: `dev.tfvars`, `staging.tfvars`, `prod.tfvars`
3. **-var-file argument**: `-var-file=dev.tfvars`
4. **Terragrunt directory**: `terragrunt/dev/`, `terragrunt/staging/`
5. **Terraform workspace**: `terraform workspace select dev`
6. If none match: defaults to `unknown` -> checkpoint

### What "AUTO-APPROVED" Means (for plan only)

- The agent can run `terraform plan` without human confirmation
- The plan output is captured for verification and PR description
- This does **NOT** permit `terraform apply` -- apply is CI/CD only
- The action is logged to project history

### What "CHECKPOINT" Means

- The agent **should pause** and confirm the action is correct
- For unknown environments: ask for human clarification
- Does not apply to apply/destroy (those are always BLOCKED)

### What "BLOCKED" Means

- The hook script exits with code 1 (hard block)
- The command is prevented from executing
- For apply/destroy: always blocked for agents, no exceptions
- For prod plan: human must explicitly approve

## Plan Approval Auto-Criteria

When operating autonomously (in a `/pipeline` team), the Lead can auto-approve teammate **implementation plans** (not terraform apply) if **ALL** of the following are true:

### Auto-Approve Plan When:
- [ ] Security considerations are explicitly addressed (encryption, IAM, network)
- [ ] Test strategy is included (unit tests, plan validation)
- [ ] No hardcoded secrets detected
- [ ] Cost is addressed (even if "no additional cost" or "within budget")
- [ ] Rollback plan is present
- [ ] File ownership boundaries are respected
- [ ] Scope matches the assigned task (no scope creep)

### Never Auto-Approve Plan When:
- Missing ANY of the above criteria
- Plan involves production changes
- Plan modifies IAM policies with wildcard permissions (`*`)
- Plan opens security groups to `0.0.0.0/0` on sensitive ports
- Plan involves data deletion or migration
- Plan costs exceed $1,000/month estimated
- Plan requires changes to state backend configuration
- Plan modifies DNS records for production domains

## Safety Guardrails (Always Apply)

### Hard Blocks (Cannot Override)

1. **No terraform apply/destroy from agents** -- CI/CD only from main branch
2. **No commits/merges to main/master** -- feature branches only
3. **No hardcoded secrets** in commands or files
4. **No push to main/master** -- must create PR
5. **No AI mentions** in commit messages
6. **Production terraform plan** requires human approval

### Soft Blocks (Logged)

1. **Dev/staging terraform plan** -- auto-approved, output logged
2. **Checkout main** -- warning issued, no block
3. **Sensitive file in commit** -- warning issued
4. **State modification** -- checkpoint, agent documents backup plan

### Logging Requirements for Auto-Approved Actions

Every auto-approved action MUST be logged to project history with:
```markdown
**Auto-Approved Action**:
- Action: terraform plan
- Environment: dev
- Auto-Approve Rule: Non-production plan (auto-approve-protocol.md)
- Plan Output: [summary of what would change]
```

## Pipeline-Specific Behavior

When running in a `/pipeline` team:

1. Agents run `terraform plan` to verify their code produces expected changes
2. Plan output is included in the Draft PR description
3. Agents **NEVER** run `terraform apply` -- even in dev/staging
4. Apply happens automatically via CI/CD after PR is merged to main
5. The Lead verifies CI pipeline status after Draft PR is created

## The Correct Workflow

```
Agent writes code
    |
    v
Agent runs verification loop:
  terraform fmt -> validate -> tflint -> checkov -> plan
    |
    v
Agent creates Draft PR with plan output
    |
    v
CI/CD runs checks on PR (fmt, lint, plan, security scan)
    |
    v
Fix if CI fails, push, CI re-runs
    |
    v
PR approved + merged to main
    |
    v
CI/CD on main runs terraform apply (NOT the agent)
    |
    v
Agent validates deployment health post-apply
```

## Integration with Existing Safety Hooks

This protocol works alongside (not replaces) these existing hooks in `settings.json`:
- **terraform apply/destroy hard block** -- `exit 1` before env-check is reached
- **Secret detection** -- still blocks hardcoded secrets
- **Git protection** -- still blocks push/merge to main
- **State modification checkpoint** -- still reminds about backups
- **Post-write validation** -- still checks .tf files for secrets
