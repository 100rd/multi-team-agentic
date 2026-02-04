---
name: terraform-migration
description: Orchestrate parallel CloudFormation to Terraform migration with validation gates
---

# Terraform Migration Orchestrator

Execute a parallel CFN→Terraform migration campaign.

## Input Required
- `source_dir`: Path to CloudFormation templates
- `target_dir`: Path for Terraform output
- `parallelism`: Number of parallel agents (default: 4)
- `phase`: analysis|convert|plan|apply|all

## Execution Flow

### When user runs `/terraform-migration`

1. **Discovery Phase**
   - Scan source_dir for CFN templates (*.yaml, *.json)
   - Build dependency graph from CFN Exports/Imports
   - Partition into parallelizable groups

2. **Spawn Parallel Agents**
   For each partition group, launch terraform-migration-engineer:
   ```
   Task(subagent_type="terraform-migration-engineer",
        run_in_background=true,
        prompt="Convert {template} to Terraform in {target_dir}/{module}")
   ```

3. **Validation Gate**
   After all conversions complete:
   - Run parallel `terraform validate` on all modules
   - Run parallel `terraform plan` on all modules
   - Aggregate results, flag any failures

4. **Human Checkpoint**
   Present summary:
   - Modules converted: X
   - Plans clean: Y
   - Plans with changes: Z
   - Require approval to proceed to apply

5. **Apply Phase** (after approval)
   Execute applies in dependency order (not parallel)

## Usage Examples

### Full Migration
```
/terraform-migration source=cfn/ target=terraform/ parallelism=4
```

### Analysis Only
```
/terraform-migration source=cfn/ phase=analysis
```

### Plan Validation
```
/terraform-migration target=terraform/ phase=plan
```

### Sequential Apply
```
/terraform-migration target=terraform/ phase=apply
```

## Orchestrator Behavior

### Discovery
```python
# Pseudocode for template discovery
templates = glob("source_dir/**/*.yaml") + glob("source_dir/**/*.json")
for template in templates:
    exports = extract_cfn_exports(template)
    imports = extract_cfn_imports(template)
    dependency_graph.add(template, depends_on=imports, provides=exports)

partitions = dependency_graph.partition(max_parallel=parallelism)
```

### Agent Spawning
For each independent partition:
1. Create worktree or isolated directory
2. Spawn terraform-migration-engineer agent
3. Track agent ID in `.migration/agent-status.log`
4. Monitor via TaskOutput for completion

### Result Aggregation
After all agents complete:
1. Collect all `.tf` files generated
2. Run `terraform fmt -recursive`
3. Run `terraform validate` per module
4. Run `terraform plan` per module (parallel safe)
5. Generate aggregate report

### Apply Sequencing
Read `.migration/apply-order.txt` and execute:
```bash
for module in $(cat .migration/apply-order.txt); do
    cd terraform/$module
    terraform apply -auto-approve
    # Wait for completion before next
done
```

## State Files

The orchestrator maintains state in `.migration/`:

| File | Purpose |
|------|---------|
| `manifest.json` | Source→target mapping |
| `dependency-graph.json` | CFN dependencies |
| `apply-order.txt` | Sequenced apply order |
| `expected-agents.txt` | Count of spawned agents |
| `agent-status.log` | Completion tracking |
| `aggregate-plan.txt` | Combined plan output |
| `apply-log.txt` | Completed applies |

## Error Handling

- If agent fails: log error, continue others, report at end
- If validation fails: block apply, require manual fix
- If apply fails: stop sequence, preserve state, report issue

## Human Checkpoints

Require explicit approval before:
- Running `terraform apply` on any module
- Proceeding after validation errors
- Applying to production workspaces
