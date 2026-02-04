# Terragrunt Configuration Skill

> Best practices for writing Terragrunt infrastructure-as-code configurations.
> Roles: architect, devops, terragrunt-agent

## Overview

This skill defines how to write production-ready Terragrunt configurations following Gruntwork best practices. The agent MUST follow these conventions when creating or modifying Terragrunt code.

---

## 1. Repository Structure

### 1.1 Two-Repository Pattern

**ALWAYS** separate infrastructure code into two repositories:

```
infrastructure-live/     # Live configurations (this skill)
infrastructure-catalog/  # Reusable Terraform modules (versioned)
```

### 1.2 Live Repository Structure (prod/non-prod)

```
infrastructure-live/
├── root.hcl                           # Root configuration (inherited by ALL units)
├── mise.toml                          # Tool versions (terragrunt, tofu/terraform)
├── .gitignore
│
├── prod/                              # Production account
│   ├── account.hcl                    # Account-level config
│   ├── _global/                       # Account-wide resources (IAM, Route53 zones)
│   │   └── iam/
│   │       └── terragrunt.hcl
│   ├── us-east-1/                     # Region
│   │   ├── region.hcl                 # Region-level config
│   │   ├── _global/                   # Region-wide resources (ECR, SNS)
│   │   │   └── ecr/
│   │   │       └── terragrunt.hcl
│   │   └── app-cluster/               # Stack or service
│   │       ├── terragrunt.stack.hcl   # Stack definition (recommended)
│   │       └── vpc/
│   │           └── terragrunt.hcl
│   └── eu-west-1/
│       └── region.hcl
│
├── non-prod/                          # Non-production account
│   ├── account.hcl
│   ├── us-east-1/
│   │   ├── region.hcl
│   │   ├── dev/                       # Environment (optional level)
│   │   │   └── app-cluster/
│   │   │       └── terragrunt.stack.hcl
│   │   └── staging/
│   │       └── app-cluster/
│   │           └── terragrunt.stack.hcl
│   └── eu-west-1/
│       └── region.hcl
│
└── mgmt/                              # Management account (CI/CD, logging)
    ├── account.hcl
    └── us-east-1/
        ├── region.hcl
        └── ci-cd/
            └── terragrunt.hcl
```

### 1.3 Hierarchy Rules

| Level | Directory | Purpose |
|-------|-----------|---------|
| 1 | Account (`prod/`, `non-prod/`, `mgmt/`) | AWS account separation |
| 2 | `_global/` | Resources spanning all regions |
| 3 | Region (`us-east-1/`, `eu-west-1/`) | Regional deployment |
| 4 | `_global/` (region) | Resources spanning all envs in region |
| 5 | Environment (`dev/`, `staging/`) | Optional, if multi-env per account |
| 6 | Stack/Service | Actual infrastructure |

---

## 2. Configuration Files

### 2.1 root.hcl (Repository Root)

**Purpose:** Common configuration inherited by ALL units.

```hcl
# root.hcl

locals {
  # Parse account and region from directory path
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  account_name   = local.account_vars.locals.account_name
  account_id     = local.account_vars.locals.aws_account_id
  aws_region     = local.region_vars.locals.aws_region

  # ═══════════════════════════════════════════════════════════════════════════
  # TAGGING STRATEGY - Default tags applied to ALL resources
  # ═══════════════════════════════════════════════════════════════════════════
  
  # Load optional override tags from unit directory
  override_tags = try(yamldecode(file("${get_terragrunt_dir()}/tags.yml")), {})

  # Standard tags (Gruntwork recommended)
  default_tags = {
    # ─── Required Tags ───────────────────────────────────────────────────────
    "Environment"     = local.account_vars.locals.environment
    "ManagedBy"       = "Terragrunt"
    "Owner"           = local.account_vars.locals.owner
    "Team"            = local.account_vars.locals.team
    
    # ─── Cost Allocation Tags ────────────────────────────────────────────────
    "CostCenter"      = local.account_vars.locals.cost_center
    "Project"         = try(local.region_vars.locals.project, "infrastructure")
    
    # ─── Automation Tags ─────────────────────────────────────────────────────
    "TerragruntPath"  = path_relative_to_include()
    "Repository"      = "infrastructure-live"
    
    # ─── Compliance Tags ─────────────────────────────────────────────────────
    "DataClassification" = try(local.account_vars.locals.data_classification, "internal")
  }

  # Final merged tags
  tags = merge(local.default_tags, local.override_tags)
}

# ═══════════════════════════════════════════════════════════════════════════════
# REMOTE STATE - S3 Backend Configuration
# ═══════════════════════════════════════════════════════════════════════════════

remote_state {
  backend = "s3"
  
  config = {
    encrypt        = true
    bucket         = "${get_env("TG_BUCKET_PREFIX", "tfstate")}-${local.account_name}-${local.aws_region}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    dynamodb_table = "terraform-locks"

    # S3 bucket configuration
    skip_bucket_versioning         = false
    skip_bucket_ssencryption       = false
    skip_bucket_public_access_block = false
    skip_bucket_root_access        = false
    
    # Use KMS encryption
    # bucket_sse_kms_key_id = "alias/terraform-state"
  }

  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# PROVIDER GENERATION - AWS Provider with Default Tags
# ═══════════════════════════════════════════════════════════════════════════════

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<-EOF
    provider "aws" {
      region = "${local.aws_region}"

      # Assume role for cross-account access (optional)
      # assume_role {
      #   role_arn = "arn:aws:iam::${local.account_id}:role/TerragruntDeployRole"
      # }

      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }

    provider "aws" {
      alias  = "us_east_1"
      region = "us-east-1"

      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }
  EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# TERRAFORM/TOFU VERSION CONSTRAINTS
# ═══════════════════════════════════════════════════════════════════════════════

generate "versions" {
  path      = "versions.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<-EOF
    terraform {
      required_version = ">= 1.5.0"

      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = ">= 5.0"
        }
      }
    }
  EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# INPUTS - Pass to all modules
# ═══════════════════════════════════════════════════════════════════════════════

inputs = merge(
  local.account_vars.locals,
  local.region_vars.locals,
  {
    tags = local.tags
  }
)
```

### 2.2 account.hcl (Account Level)

```hcl
# prod/account.hcl

locals {
  account_name   = "prod"
  aws_account_id = "111111111111"
  environment    = "production"
  
  # ─── Tagging ───────────────────────────────────────────────────────────────
  owner               = "platform-team"
  team                = "infrastructure"
  cost_center         = "CC-1001"
  data_classification = "confidential"
  
  # ─── Account-specific settings ─────────────────────────────────────────────
  enable_deletion_protection = true
  log_retention_days         = 365
}
```

```hcl
# non-prod/account.hcl

locals {
  account_name   = "non-prod"
  aws_account_id = "222222222222"
  environment    = "development"
  
  owner               = "platform-team"
  team                = "infrastructure"
  cost_center         = "CC-1002"
  data_classification = "internal"
  
  enable_deletion_protection = false
  log_retention_days         = 30
}
```

### 2.3 region.hcl (Region Level)

```hcl
# prod/us-east-1/region.hcl

locals {
  aws_region = "us-east-1"
  
  # Region-specific settings
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  # Optional project override
  project = "main-platform"
}
```

### 2.4 terragrunt.hcl (Unit Level)

```hcl
# prod/us-east-1/networking/vpc/terragrunt.hcl

include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

terraform {
  source = "git::git@github.com:acme/infrastructure-catalog.git//modules/vpc?ref=v1.2.0"
}

locals {
  # Access parent configs
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  
  env        = local.account_vars.locals.environment
  aws_region = local.region_vars.locals.aws_region
  azs        = local.region_vars.locals.availability_zones
}

inputs = {
  name = "main-vpc-${local.env}"
  cidr = "10.0.0.0/16"

  azs             = local.azs
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = local.env != "production"
  enable_dns_hostnames   = true
  enable_dns_support     = true

  # Tags are automatically merged from root.hcl
  # Additional tags specific to this resource:
  tags = {
    Component = "networking"
    Service   = "vpc"
  }
}
```

---

## 3. Stacks (terragrunt.stack.hcl)

**PREFER stacks** for deploying related infrastructure components together.

### 3.1 Stack Definition

```hcl
# prod/us-east-1/app-cluster/terragrunt.stack.hcl

locals {
  # Stack-wide variables
  name        = "app-cluster"
  environment = "production"
  
  # Database credentials (use secrets manager in production!)
  db_username = "admin"
  db_password = get_env("DB_PASSWORD", "changeme")
}

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKING
# ═══════════════════════════════════════════════════════════════════════════════

unit "vpc" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/vpc?ref=v1.0.0"
  path   = "vpc"

  values = {
    name               = local.name
    cidr               = "10.10.0.0/16"
    availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECURITY GROUPS
# ═══════════════════════════════════════════════════════════════════════════════

unit "alb_sg" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/security-group?ref=v1.0.0"
  path   = "sgs/alb"

  values = {
    name        = "${local.name}-alb"
    description = "Security group for ALB"
    vpc_path    = "../vpc"
    
    ingress_rules = [
      {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      }
    ]
  }
}

unit "app_sg" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/security-group?ref=v1.0.0"
  path   = "sgs/app"

  values = {
    name        = "${local.name}-app"
    description = "Security group for application"
    vpc_path    = "../vpc"
    
    ingress_security_groups = [
      {
        from_port       = 8080
        to_port         = 8080
        protocol        = "tcp"
        security_group_path = "../alb"
      }
    ]
  }
}

unit "db_sg" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/security-group?ref=v1.0.0"
  path   = "sgs/db"

  values = {
    name        = "${local.name}-db"
    description = "Security group for database"
    vpc_path    = "../vpc"
    
    ingress_security_groups = [
      {
        from_port       = 5432
        to_port         = 5432
        protocol        = "tcp"
        security_group_path = "../app"
      }
    ]
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

unit "database" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/rds-postgres?ref=v1.0.0"
  path   = "database"

  values = {
    name            = "${local.name}-db"
    engine_version  = "15.4"
    instance_class  = "db.r6g.large"
    
    vpc_path        = "../vpc"
    sg_path         = "../sgs/db"
    
    db_name         = replace(local.name, "-", "_")
    master_username = local.db_username
    master_password = local.db_password
    
    multi_az                = true
    deletion_protection     = true
    backup_retention_period = 30
  }
}

# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

unit "service" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/ecs-service?ref=v1.0.0"
  path   = "service"

  values = {
    name          = local.name
    
    vpc_path      = "../vpc"
    alb_sg_path   = "../sgs/alb"
    app_sg_path   = "../sgs/app"
    db_path       = "../database"
    
    container_port = 8080
    cpu            = 512
    memory         = 1024
    desired_count  = 3
    
    environment_variables = {
      NODE_ENV = local.environment
    }
  }
}
```

### 3.2 Stack Commands

```bash
# Generate stack units
terragrunt stack generate

# Plan entire stack
terragrunt stack run plan

# Apply entire stack
terragrunt stack run apply

# Get stack outputs
terragrunt stack output
```

---

## 4. Tags and Labels Strategy

### 4.1 Recommended Tags

| Tag Key | Description | Example | Required |
|---------|-------------|---------|----------|
| `Environment` | Deployment environment | `production`, `staging`, `development` | ✅ |
| `ManagedBy` | IaC tool | `Terragrunt` | ✅ |
| `Owner` | Team/person responsible | `platform-team` | ✅ |
| `Team` | Owning team | `infrastructure` | ✅ |
| `CostCenter` | Billing code | `CC-1001` | ✅ |
| `Project` | Project name | `main-platform` | ✅ |
| `Service` | Service name | `api-gateway` | ⚠️ |
| `Component` | Component type | `networking`, `compute`, `storage` | ⚠️ |
| `TerragruntPath` | Path in repo | `prod/us-east-1/vpc` | ⚠️ |
| `Repository` | Git repository | `infrastructure-live` | ⚠️ |
| `DataClassification` | Data sensitivity | `public`, `internal`, `confidential` | ⚠️ |

### 4.2 Tag Override with tags.yml

Create `tags.yml` in any unit directory to override default tags:

```yaml
# prod/us-east-1/app-cluster/database/tags.yml
DataClassification: confidential
BackupRetention: "30days"
Compliance: "SOC2"
```

### 4.3 Auto Scaling Group Tags

ASG requires special handling (default_tags don't apply):

```hcl
# In module
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_autoscaling_group" "this" {
  # ... configuration ...

  dynamic "tag" {
    for_each = var.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}
```

---

## 5. Dependencies

### 5.1 Using dependency Block

```hcl
# prod/us-east-1/app/terragrunt.hcl

include "root" {
  path = find_in_parent_folders("root.hcl")
}

dependency "vpc" {
  config_path = "../networking/vpc"

  # Mock outputs for plan without applying dependencies
  mock_outputs = {
    vpc_id             = "vpc-mock"
    private_subnet_ids = ["subnet-mock-1", "subnet-mock-2"]
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

dependency "sg" {
  config_path = "../security/app-sg"

  mock_outputs = {
    security_group_id = "sg-mock"
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

inputs = {
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids
  sg_ids     = [dependency.sg.outputs.security_group_id]
}
```

### 5.2 Dependencies in Stacks

In stacks, use relative paths:

```hcl
unit "service" {
  source = "..."
  path   = "service"

  values = {
    vpc_path = "../vpc"  # Relative to stack directory
    db_path  = "../database"
  }
}
```

---

## 6. Multi-Region Deployment

### 6.1 Region Configuration

```hcl
# root.hcl - Multi-region provider

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<-EOF
    provider "aws" {
      region = "${local.aws_region}"
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }

    # Secondary region for DR
    provider "aws" {
      alias  = "secondary"
      region = "${local.secondary_region}"
      default_tags {
        tags = ${jsonencode(merge(local.tags, { Region = local.secondary_region }))}
      }
    }

    # Global resources (us-east-1 for CloudFront, ACM, etc.)
    provider "aws" {
      alias  = "global"
      region = "us-east-1"
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }
  EOF
}
```

---

## 7. Environment Promotion

### 7.1 Version Pinning Strategy

```
non-prod/
  └── us-east-1/
      └── app/
          └── terragrunt.hcl  # source = "...?ref=v1.2.0"

prod/
  └── us-east-1/
      └── app/
          └── terragrunt.hcl  # source = "...?ref=v1.1.0" (proven stable)
```

### 7.2 Promotion Workflow

1. Deploy to `dev` with latest tag
2. Test and validate
3. Promote to `staging` (update ref)
4. Run integration tests
5. Promote to `prod` (update ref)

---

## 8. Common Patterns

### 8.1 Conditional Resources

```hcl
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  is_prod      = local.account_vars.locals.environment == "production"
}

inputs = {
  instance_count = local.is_prod ? 3 : 1
  instance_type  = local.is_prod ? "r6g.xlarge" : "t3.small"
  
  # Enable features only in prod
  enable_multi_az     = local.is_prod
  enable_autoscaling  = local.is_prod
  enable_waf          = local.is_prod
}
```

### 8.2 Shared Data Sources

```hcl
# _envcommon/data.hcl

locals {
  # Shared AMI lookup
  ami_filter = {
    name   = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
    owners = ["099720109477"]  # Canonical
  }
  
  # Shared certificate ARN
  certificate_arn = "arn:aws:acm:us-east-1:${local.account_id}:certificate/xxx"
}
```

### 8.3 Skip Patterns

```hcl
# Skip in certain environments
skip = local.account_vars.locals.environment == "development"
```

---

## 9. Agent Rules

### 9.1 MUST Do

- ✅ Always use `include "root"` with labeled includes
- ✅ Always pin module versions (`?ref=v1.2.0`)
- ✅ Always define `mock_outputs` for dependencies
- ✅ Always use `jsonencode()` for tags in generate blocks
- ✅ Always use `path_relative_to_include()` for state keys
- ✅ Always separate prod/non-prod at account level

### 9.2 MUST NOT Do

- ❌ Never use bare includes (`include {}`)
- ❌ Never hardcode AWS credentials
- ❌ Never use Terraform workspaces
- ❌ Never commit `.terraform.lock.hcl` (add to `.gitignore`)
- ❌ Never put secrets in terragrunt files (use secrets manager)
- ❌ Never use `latest` or `main` as module refs in production

### 9.3 SHOULD Do

- ⚡ Prefer stacks over individual units for related resources
- ⚡ Use `_global` directories for cross-region/env resources
- ⚡ Use YAML files for environment-specific overrides
- ⚡ Use `read_terragrunt_config()` over `file()` for HCL
- ⚡ Group related resources in subdirectories

---

## 10. Validation Commands

```bash
# Validate all configurations
terragrunt run --all validate

# Format all files
terragrunt hclfmt

# Show dependency graph
terragrunt graph-dependencies

# Plan with debug output
terragrunt plan --terragrunt-log-level debug

# Show all inputs
terragrunt render-json
```

---

## 11. File Templates

When creating new infrastructure, use these templates:

### New Account
```bash
mkdir -p {account_name}/{us-east-1,eu-west-1}
touch {account_name}/account.hcl
touch {account_name}/us-east-1/region.hcl
touch {account_name}/eu-west-1/region.hcl
```

### New Stack
```bash
mkdir -p {account}/{region}/{stack_name}
touch {account}/{region}/{stack_name}/terragrunt.stack.hcl
```

### New Unit
```bash
mkdir -p {account}/{region}/{service}
touch {account}/{region}/{service}/terragrunt.hcl
```

---

## 12. CIS AWS Foundations Benchmark Compliance

### Overview

When deploying infrastructure with Terragrunt, ensure CIS AWS Foundations Benchmark v1.4.0 compliance. The benchmark has **5 control categories** across **2 levels** (Level 1 = baseline, Level 2 = high-security).

### Account Baseline Pattern

Deploy CIS-compliant account baselines across all accounts:

```
infrastructure-live/
├── prod/
│   ├── _global/
│   │   └── account-baseline/        # CIS controls for prod account
│   │       └── terragrunt.hcl
├── non-prod/
│   ├── _global/
│   │   └── account-baseline/        # CIS controls for non-prod
│   │       └── terragrunt.hcl
├── mgmt/
│   ├── _global/
│   │   └── account-baseline/        # CIS controls for mgmt (root baseline)
│   │       └── terragrunt.hcl
└── logs/
    ├── _global/
    │   └── account-baseline/        # Centralized logging
    │       └── terragrunt.hcl
```

### Account Baseline Unit

```hcl
# prod/_global/account-baseline/terragrunt.hcl
include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

terraform {
  source = "git::git@github.com:gruntwork-io/terraform-aws-cis-service-catalog.git//modules/landingzone/account-baseline-app?ref=v0.27.0"
}

locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
}

inputs = {
  # ─── CloudTrail (CIS 3.1-3.7, 3.10-3.11) ─────────────────────────────
  enable_cloudtrail              = true
  cloudtrail_is_multi_region     = true     # CIS 3.1
  cloudtrail_log_file_validation = true     # CIS 3.2
  cloudtrail_kms_key_arn         = dependency.kms.outputs.key_arn  # CIS 3.7
  cloudtrail_s3_bucket_name      = "logs-cloudtrail-${local.account_vars.locals.aws_account_id}"

  # ─── AWS Config (CIS 3.5) ──────────────────────────────────────────────
  enable_config         = true
  config_s3_bucket_name = "logs-config-${local.account_vars.locals.aws_account_id}"

  # ─── GuardDuty ─────────────────────────────────────────────────────────
  enable_guardduty = true

  # ─── Security Hub (CIS auto-checks) ────────────────────────────────────
  enable_security_hub = true

  # ─── IAM Access Analyzer (CIS 1.20) ────────────────────────────────────
  enable_iam_access_analyzer = true
}

dependency "kms" {
  config_path = "../kms"
  mock_outputs = {
    key_arn = "arn:aws:kms:us-east-1:123456789012:key/mock-key-id"
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}
```

### CIS-Compliant VPC Pattern

```hcl
# prod/us-east-1/vpc/terragrunt.hcl
include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

terraform {
  source = "git::git@github.com:company/infrastructure-catalog.git//modules/networking/vpc?ref=v1.2.0"
}

inputs = {
  # ─── CIS 5.1: No public SSH/RDP ───────────────────────────────────────
  # No security groups with 0.0.0.0/0 on ports 22 or 3389
  # Use SSM Session Manager instead of SSH

  # ─── CIS 3.9: VPC Flow Logs ───────────────────────────────────────────
  enable_flow_logs         = true
  flow_log_destination     = "cloud-watch-logs"
  flow_log_retention_days  = 365

  # ─── CIS 5.4: Private subnets for workloads ───────────────────────────
  create_private_subnets = true
  create_public_subnets  = true  # Only for ALB/NLB
  nat_gateway_enabled    = true

  # ─── CIS 5.2: Restrict default security group ─────────────────────────
  manage_default_security_group = true
  default_security_group_ingress = []
  default_security_group_egress  = []
}
```

### CIS-Compliant S3 Pattern

```hcl
# Ensure all S3 buckets meet CIS 2.1.x controls
inputs = {
  # CIS 2.1.3-2.1.5: Block all public access
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  # CIS 2.1.1: Enforce TLS
  enforce_tls = true

  # Encryption with KMS
  sse_algorithm     = "aws:kms"
  kms_master_key_id = dependency.kms.outputs.key_arn

  # Versioning
  versioning_enabled = true
}
```

### CloudWatch Metric Filters (CIS 4.1-4.15)

```hcl
# prod/us-east-1/monitoring/terragrunt.hcl
inputs = {
  # All 15 CIS-required CloudWatch metric filters
  metric_filters = {
    unauthorized_api_calls    = { pattern = "{ ($.errorCode = \"*UnauthorizedAccess*\") || ($.errorCode = \"AccessDenied*\") }" }
    console_signin_no_mfa     = { pattern = "{ ($.eventName = \"ConsoleLogin\") && ($.additionalEventData.MFAUsed != \"Yes\") }" }
    root_account_usage        = { pattern = "{ $.userIdentity.type = \"Root\" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != \"AwsServiceEvent\" }" }
    iam_policy_changes        = { pattern = "{ ($.eventName=DeleteGroupPolicy) || ($.eventName=DeleteRolePolicy) || ($.eventName=DeleteUserPolicy) || ($.eventName=PutGroupPolicy) || ($.eventName=PutRolePolicy) || ($.eventName=PutUserPolicy) || ($.eventName=CreatePolicy) || ($.eventName=DeletePolicy) || ($.eventName=CreatePolicyVersion) || ($.eventName=DeletePolicyVersion) || ($.eventName=AttachRolePolicy) || ($.eventName=DetachRolePolicy) || ($.eventName=AttachUserPolicy) || ($.eventName=DetachUserPolicy) || ($.eventName=AttachGroupPolicy) || ($.eventName=DetachGroupPolicy) }" }
    cloudtrail_changes        = { pattern = "{ ($.eventName = CreateTrail) || ($.eventName = UpdateTrail) || ($.eventName = DeleteTrail) || ($.eventName = StartLogging) || ($.eventName = StopLogging) }" }
    console_auth_failures     = { pattern = "{ ($.eventName = ConsoleLogin) && ($.errorMessage = \"Failed authentication\") }" }
    cmk_deletion              = { pattern = "{ ($.eventSource = kms.amazonaws.com) && (($.eventName=DisableKey) || ($.eventName=ScheduleKeyDeletion)) }" }
    s3_policy_changes         = { pattern = "{ ($.eventSource = s3.amazonaws.com) && (($.eventName = PutBucketAcl) || ($.eventName = PutBucketPolicy) || ($.eventName = PutBucketCors) || ($.eventName = PutBucketLifecycle) || ($.eventName = PutBucketReplication) || ($.eventName = DeleteBucketPolicy) || ($.eventName = DeleteBucketCors) || ($.eventName = DeleteBucketLifecycle) || ($.eventName = DeleteBucketReplication)) }" }
    config_changes            = { pattern = "{ ($.eventSource = config.amazonaws.com) && (($.eventName=StopConfigurationRecorder) || ($.eventName=DeleteDeliveryChannel) || ($.eventName=PutDeliveryChannel) || ($.eventName=PutConfigurationRecorder)) }" }
    security_group_changes    = { pattern = "{ ($.eventName = AuthorizeSecurityGroupIngress) || ($.eventName = AuthorizeSecurityGroupEgress) || ($.eventName = RevokeSecurityGroupIngress) || ($.eventName = RevokeSecurityGroupEgress) || ($.eventName = CreateSecurityGroup) || ($.eventName = DeleteSecurityGroup) }" }
    nacl_changes              = { pattern = "{ ($.eventName = CreateNetworkAcl) || ($.eventName = CreateNetworkAclEntry) || ($.eventName = DeleteNetworkAcl) || ($.eventName = DeleteNetworkAclEntry) || ($.eventName = ReplaceNetworkAclEntry) || ($.eventName = ReplaceNetworkAclAssociation) }" }
    network_gateway_changes   = { pattern = "{ ($.eventName = CreateCustomerGateway) || ($.eventName = DeleteCustomerGateway) || ($.eventName = AttachInternetGateway) || ($.eventName = CreateInternetGateway) || ($.eventName = DeleteInternetGateway) || ($.eventName = DetachInternetGateway) }" }
    route_table_changes       = { pattern = "{ ($.eventName = CreateRoute) || ($.eventName = CreateRouteTable) || ($.eventName = ReplaceRoute) || ($.eventName = ReplaceRouteTableAssociation) || ($.eventName = DeleteRouteTable) || ($.eventName = DeleteRoute) || ($.eventName = DisassociateRouteTable) }" }
    vpc_changes               = { pattern = "{ ($.eventName = CreateVpc) || ($.eventName = DeleteVpc) || ($.eventName = ModifyVpcAttribute) || ($.eventName = AcceptVpcPeeringConnection) || ($.eventName = CreateVpcPeeringConnection) || ($.eventName = DeleteVpcPeeringConnection) || ($.eventName = RejectVpcPeeringConnection) || ($.eventName = AttachClassicLinkVpc) || ($.eventName = DetachClassicLinkVpc) || ($.eventName = DisableVpcClassicLink) || ($.eventName = EnableVpcClassicLink) }" }
    organizations_changes     = { pattern = "{ ($.eventSource = organizations.amazonaws.com) && (($.eventName = \"AcceptHandshake\") || ($.eventName = \"AttachPolicy\") || ($.eventName = \"CreateAccount\") || ($.eventName = \"CreateOrganizationalUnit\") || ($.eventName = \"CreatePolicy\") || ($.eventName = \"DeclineHandshake\") || ($.eventName = \"DeleteOrganization\") || ($.eventName = \"DeleteOrganizationalUnit\") || ($.eventName = \"DeletePolicy\") || ($.eventName = \"DetachPolicy\") || ($.eventName = \"DisablePolicyType\") || ($.eventName = \"EnablePolicyType\") || ($.eventName = \"InviteAccountToOrganization\") || ($.eventName = \"LeaveOrganization\") || ($.eventName = \"MoveAccount\") || ($.eventName = \"RemoveAccountFromOrganization\") || ($.eventName = \"UpdatePolicy\") || ($.eventName = \"UpdateOrganizationalUnit\")) }" }
  }

  sns_topic_arn = dependency.sns.outputs.topic_arn
}
```

### CIS Compliance Scanning Integration

Add to CI/CD or run manually:

```bash
# Enable CIS v1.4.0 in Security Hub (Terraform)
# aws_securityhub_standards_subscription with:
#   standards_arn = "arn:aws:securityhub:::standards/cis-aws-foundations-benchmark/v/1.4.0"

# Prowler scan
prowler aws --compliance cis_1.4_aws --output-formats json,html

# Checkov with CIS framework
checkov -d . --framework terraform --check CIS*

# Steampipe benchmark
steampipe check benchmark.cis_v140
```

### CIS Control Quick Reference

| Category | Controls | Key Requirement |
|----------|----------|----------------|
| IAM | 1.1-1.21 | Least privilege, MFA, key rotation, Access Analyzer |
| Storage | 2.1-2.3 | Encryption, no public access, TLS enforced |
| Logging | 3.1-3.11 | CloudTrail multi-region, Config, Flow Logs, KMS |
| Monitoring | 4.1-4.15 | 15 CloudWatch metric filters with SNS alerts |
| Networking | 5.1-5.4 | No public SSH/RDP, default SG locked, private subnets |

---

## References

- [Terragrunt Documentation](https://terragrunt.gruntwork.io/docs/)
- [infrastructure-live-stacks-example](https://github.com/gruntwork-io/terragrunt-infrastructure-live-stacks-example)
- [infrastructure-catalog-example](https://github.com/gruntwork-io/terragrunt-infrastructure-catalog-example)
- [Gruntwork Labels and Tags](https://docs.gruntwork.io/2.0/docs/overview/concepts/labels-tags/)
- [Gruntwork CIS Compliance Guide](https://docs.gruntwork.io/guides/build-it-yourself/achieve-compliance/)
- [CIS AWS Foundations Benchmark v1.4.0 (AWS Security Hub)](https://docs.aws.amazon.com/securityhub/latest/userguide/cis-aws-foundations-benchmark.html)
- [CIS AWS v1.4.0 Steampipe Benchmark](https://hub.steampipe.io/mods/turbot/aws_compliance/controls/benchmark.cis_v140)
