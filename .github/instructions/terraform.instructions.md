---
applyTo: "**/*.tf,**/*.tfvars,**/terragrunt.hcl,**/*.hcl"
---

## Terraform & Terragrunt Standards

### Code Style
- Run `terraform fmt` before committing
- Run `terragrunt hclfmt` for HCL files
- Use snake_case for resource names and variables
- Group resources logically (networking, compute, security)

### Module Design
- Pin provider versions with `~>` constraints
- Pin module versions with exact refs (`?ref=v1.2.0`)
- Define `description` for all variables and outputs
- Use `validation` blocks for input variables
- Include `default` values where sensible
- Add `type` constraints for all variables

### Security Requirements
- Enable encryption at rest for all storage resources
- Use private subnets for compute resources
- Follow least-privilege IAM policies
- No hardcoded secrets - use `data "aws_secretsmanager_secret"` or variables
- Enable logging (CloudTrail, VPC Flow Logs, access logs)
- Use security groups with explicit ingress/egress rules

### Terragrunt Patterns
- Use labeled includes: `include "root" { path = find_in_parent_folders("root.hcl") }`
- Pin module versions: `source = "git::...?ref=v1.2.0"`
- Define `mock_outputs` for all dependencies
- Use `path_relative_to_include()` for state keys
- Encrypt state (S3 SSE + DynamoDB locking)

### Testing
- Write Terratest or terraform-test for modules
- Validate with `terraform validate` before planning
- Run `checkov -d .` for security scanning
- Use `terraform plan -detailed-exitcode` for drift detection

### Naming Conventions
```hcl
# Resources: <provider>_<resource>.<descriptor>
resource "aws_instance" "web_server" {}

# Variables: descriptive, snake_case
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

# Outputs: descriptive, matches resource
output "cluster_endpoint" {
  description = "EKS cluster API endpoint"
  value       = aws_eks_cluster.main.endpoint
}
```
