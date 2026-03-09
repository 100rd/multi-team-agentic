# Auto-Approve Protocol

Defines when and how terraform apply/destroy operations can be auto-approved without human intervention, and what safety guardrails still apply in autonomous mode.

## Environment Auto-Approve Rules

| Environment | terraform apply | terraform destroy | Plan Approval |
|-------------|----------------|-------------------|---------------|
| **dev** | AUTO-APPROVED | AUTO-APPROVED | Lead decides |
| **staging** | AUTO-APPROVED | CHECKPOINT (document reason) | Lead decides |
| **prod** | BLOCKED (human required) | BLOCKED (human required) | BLOCKED (human required) |
| **unknown** | CHECKPOINT (agent should pause) | CHECKPOINT (agent should pause) | Lead decides |

### How Environment Is Detected

The hook script `scripts/terraform-env-check.sh` checks (in priority order):

1. **Working directory path**: `environments/dev/`, `environments/staging/`, `environments/prod/`
2. **Tfvars file name**: `dev.tfvars`, `staging.tfvars`, `prod.tfvars`
3. **-var-file argument**: `-var-file=dev.tfvars`
4. **Terragrunt directory**: `terragrunt/dev/`, `terragrunt/staging/`
5. **Terraform workspace**: `terraform workspace select dev`
6. If none match: defaults to `unknown` → manual approval (safe default)

### What "AUTO-APPROVED" Means

- The hook script exits with code 0 (no block)
- An `AUTO_APPROVED` message is echoed for logging
- The agent proceeds **without** waiting for human input
- The action is logged to project history with auto-approve reference

### What "CHECKPOINT" Means

- The hook script exits with code 0 (no hard block)
- A `CHECKPOINT` message is echoed
- The agent **should pause** and confirm the action is correct
- For unknown environments: the agent should try to determine the environment and if uncertain, ask for human approval

### What "BLOCKED" Means

- The hook script exits with code 1 (hard block)
- A `BLOCKED` message is echoed
- The command is prevented from executing
- Human must explicitly approve before retrying

## Plan Approval Auto-Criteria

When operating autonomously (in a `/pipeline` team), the Lead can auto-approve teammate plans if **ALL** of the following are true:

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

## Safety Guardrails (Always Apply, Even in Autonomous Mode)

### Hard Blocks (Cannot Override Even in Pipeline)

1. **No commits/merges to main/master** — feature branches only
2. **No hardcoded secrets** in commands or files
3. **No push to main/master** — must create PR
4. **No AI mentions** in commit messages
5. **Production terraform apply/destroy** requires human approval
6. **Production plan approval** requires human approval

### Soft Blocks (Auto-approved with Logging)

1. **Dev/staging terraform apply** — auto-approved, logged to history
2. **Staging terraform destroy** — checkpoint, agent documents reason
3. **Checkout main** — warning issued, no block
4. **Sensitive file in commit** — warning issued
5. **State modification** — checkpoint, agent documents backup plan

### Logging Requirements for Auto-Approved Actions

Every auto-approved action MUST be logged to project history with:
```markdown
**Auto-Approved Action**:
- Action: terraform apply
- Environment: dev
- Auto-Approve Rule: Non-production environment (auto-approve-protocol.md)
- Terraform Plan Output: [summary of what will change]
```

## Pipeline-Specific Auto-Approve

When running in a `/pipeline` team:

1. The pipeline command passes `--auto-approve dev,staging` as default
2. The Lead includes auto-approve scope in teammate spawn prompts
3. Teammates read this protocol before executing terraform operations
4. When executing terraform apply:
   - The hook script (`scripts/terraform-env-check.sh`) handles the approval automatically
   - The agent logs the auto-approval to project history
   - The agent continues without waiting for human input

### What Is NOT Auto-Approved in Pipeline
- Production terraform apply/destroy — ALWAYS requires human
- Git commits — always allowed but must follow conventions
- Plan approvals that fail auto-criteria — Lead must reject and request revision
- Any action outside the pipeline's defined scope

## Manual Override

Users can override auto-approve settings when launching a pipeline:

```bash
# Force manual approval for all environments
/pipeline "..." --auto-approve none

# Auto-approve only dev
/pipeline "..." --auto-approve dev

# Auto-approve dev + staging (default)
/pipeline "..." --auto-approve dev,staging
```

## Integration with Existing Safety Hooks

This protocol works alongside (not replaces) these existing hooks in `settings.json`:
- **Secret detection** — still blocks hardcoded secrets
- **Git protection** — still blocks push/merge to main
- **Terraform destroy warning** (line 60-62) — still fires as additional warning for all environments
- **State modification checkpoint** — still reminds about backups
- **Post-write validation** — still checks .tf files for secrets
