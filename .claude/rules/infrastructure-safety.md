---
paths:
  - "**/*.tf"
  - "**/*.hcl"
  - "**/terragrunt.hcl"
  - "**/*.tfvars"
  - "**/modules/**"
  - "**/environments/**"
---

# Infrastructure Development Rules

## Terraform/Terragrunt Safety (ENFORCED BY HOOKS)

1. **Apply/Destroy requires approval**
   - `terraform apply` triggers human checkpoint
   - `terraform destroy` triggers explicit warning
   - `terragrunt run-all apply` triggers approval

2. **State modifications are flagged**
   - `terraform state rm/mv/push` triggers backup reminder
   - `terraform import` triggers verification prompt

3. **Secrets are blocked**
   - Hardcoded secrets in commands are BLOCKED
   - Secrets in .tf files trigger warnings
   - Sensitive files (.env, .pem, .key) trigger commit warnings

## Infrastructure Workflow (Enhanced with Agent Teams)

```
1. /design-system "description"     <- Spawns full agent team
2. Architect designs                 <- Plan mode, requires approval
3. Security + Cost review design     <- Parallel review
4. Terraform + DevOps implement      <- Plan mode, requires approval
5. Security + Best Practices review  <- Parallel review
6. terraform plan                    <- Automated validation
7. /blast-radius                     <- Impact analysis
8. /cost-estimate                    <- Budget check
9. terraform apply (dev)             <- Human approval required
10. /validate-deployment             <- Automated health check
11. /promote-environment             <- Move to staging/prod
12. Commit + PR                      <- All changes on feature branch
```

## Environment Promotion Rules

```
dev -> staging -> prod
```

- **dev -> staging**: Requires passing tests + security scan
- **staging -> prod**: Requires human approval + change ticket
