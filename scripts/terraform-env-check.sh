#!/usr/bin/env bash
# terraform-env-check.sh
# Called by .claude/settings.json hooks to determine environment and approve/block terraform operations.
#
# Usage: terraform-env-check.sh <action>
#   action: "plan", "apply", or "destroy"
#   Reads CLAUDE_TOOL_INPUT from environment (set by Claude Code hooks)
#
# Exit codes:
#   0 = allowed (auto-approved for plan in dev/staging)
#   1 = blocked (apply/destroy always blocked for agents; plan blocked for prod)
#
# POLICY: Agents can ONLY run terraform plan. Apply/destroy is CI/CD only (from main).
#
# Environment detection priority:
#   1. Working directory path patterns (environments/dev/, env/staging/, etc.)
#   2. Tfvars file names (dev.tfvars, staging.tfvars, etc.)
#   3. -var-file argument patterns
#   4. Terragrunt directory patterns
#   5. Falls back to "unknown" (checkpoint, not blocked)

set -euo pipefail

ACTION="${1:-apply}"
INPUT="${CLAUDE_TOOL_INPUT:-}"

detect_env() {
  local input="$1"

  # 1. Check working directory path patterns
  if echo "$input" | grep -qiE '(environments?/|env/)(dev|development)(/|[[:space:]]|"|$)'; then
    echo "dev"; return
  fi
  if echo "$input" | grep -qiE '(environments?/|env/)(stag|staging)(/|[[:space:]]|"|$)'; then
    echo "staging"; return
  fi
  if echo "$input" | grep -qiE '(environments?/|env/)(prod|production)(/|[[:space:]]|"|$)'; then
    echo "prod"; return
  fi

  # 2. Check tfvars file names
  if echo "$input" | grep -qiE 'dev(elopment)?\.tfvars'; then
    echo "dev"; return
  fi
  if echo "$input" | grep -qiE 'stag(ing)?\.tfvars'; then
    echo "staging"; return
  fi
  if echo "$input" | grep -qiE 'prod(uction)?\.tfvars'; then
    echo "prod"; return
  fi

  # 3. Check -var-file arguments
  if echo "$input" | grep -qiE '\-var-file[= ]*[^ ]*dev'; then
    echo "dev"; return
  fi
  if echo "$input" | grep -qiE '\-var-file[= ]*[^ ]*stag'; then
    echo "staging"; return
  fi
  if echo "$input" | grep -qiE '\-var-file[= ]*[^ ]*prod'; then
    echo "prod"; return
  fi

  # 4. Check terragrunt directory patterns
  if echo "$input" | grep -qiE 'terragrunt.*/(dev|development)/'; then
    echo "dev"; return
  fi
  if echo "$input" | grep -qiE 'terragrunt.*/(stag|staging)/'; then
    echo "staging"; return
  fi
  if echo "$input" | grep -qiE 'terragrunt.*/(prod|production)/'; then
    echo "prod"; return
  fi

  # 5. Check TF_VAR or workspace patterns
  if echo "$input" | grep -qiE 'terraform workspace select (dev|development)'; then
    echo "dev"; return
  fi
  if echo "$input" | grep -qiE 'terraform workspace select (stag|staging)'; then
    echo "staging"; return
  fi
  if echo "$input" | grep -qiE 'terraform workspace select (prod|production)'; then
    echo "prod"; return
  fi

  echo "unknown"
}

ENV=$(detect_env "$INPUT")

# HARD BLOCK: apply/destroy is NEVER allowed from agents (CI/CD only from main)
if [ "$ACTION" = "apply" ] || [ "$ACTION" = "destroy" ]; then
  echo "BLOCKED: type=terraform_${ACTION} env=${ENV} action=CI_CD_ONLY severity=critical detail=Agents cannot terraform ${ACTION}. Apply/destroy only from CI/CD pipelines on main branch after PR merge. Use terraform plan instead."
  exit 1
fi

# PLAN: allowed for dev/staging, blocked for prod
case "$ENV" in
  dev)
    echo "AUTO_APPROVED: type=terraform_plan env=dev detail=Development plan auto-approved for verification"
    exit 0
    ;;
  staging)
    echo "AUTO_APPROVED: type=terraform_plan env=staging detail=Staging plan auto-approved for verification"
    exit 0
    ;;
  prod|production)
    echo "BLOCKED: type=terraform_plan env=prod action=HUMAN_APPROVAL_REQUIRED severity=critical detail=Production plan requires explicit human approval"
    exit 1
    ;;
  *)
    echo "CHECKPOINT: type=terraform_plan env=unknown action=human_approval_recommended severity=high detail=Could not determine environment. Defaulting to checkpoint."
    exit 0
    ;;
esac
