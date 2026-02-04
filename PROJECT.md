# Project Configuration

## Active Projects

### 1. SimplePage
**Name**: SimplePage - IP Address Display
**Type**: Web Application (Node.js)
**Status**: Active Development
**Created**: 2025-11-27
**Location**: `project/simplePage/`

**Description**: A simple, elegant web application that displays the client's IP address with a modern UI.

**Tech Stack**:
- Backend: Node.js + Express
- Frontend: Vanilla HTML, CSS, JavaScript
- No database required

### 2. GenAI Enablement
**Name**: GenAI Enablement - DevOps/SRE Adoption Program
**Type**: Implementation Plan & Knowledge Repository
**Status**: Active Development
**Created**: 2025-12-02
**Location**: `project/genai-enablement/`

**Description**: Comprehensive implementation plan and research repository for GenAI Adoption Leader role focused on DevOps/SRE workflows. Enables project teams to use AI in real SDLC/SRE workflows with proven patterns and measurable impact.

**Key Components**:
- Market research: 40+ GenAI DevOps/SRE solutions analyzed
- Implementation roadmap: Phased adoption plan
- Tool comparison: Decision guides for technology stack selection
- Playbooks & templates: Reusable patterns and frameworks
- Case studies: Real-world adoption examples

**Expected Impact**:
- 50-70% MTTR reduction
- 30-40% faster deployments
- 60-80% reduction in false positives
- Measurable reduction in on-call pain and toil

### 3. Snips Core DevOps Infrastructure
**Name**: Snips Core DevOps Infrastructure
**Type**: Enterprise Cloud Infrastructure (AWS + Kubernetes)
**Status**: Active Development
**Created**: 2025-01-14
**Location**: `project/snips/core-devops-infra/`

**Description**: Enterprise-grade cloud infrastructure for the Snips project with:
- EKS 1.33.3 with Karpenter v21.1.5 autoscaling
- Multi-environment support (dev/prod)
- RDS PostgreSQL 17.6 and ElastiCache Redis
- GitOps deployments with ArgoCD
- Comprehensive CI/CD with GitHub Actions

**Tech Stack**:
- Terraform >= 1.5.0, AWS Provider ~> 5.0
- 22 reusable Terraform modules
- 6 GitHub Actions workflows
- Helm charts and Helmfile
- 30+ documentation guides

**Environments**:
- Dev: 172.18.32.0/20 - ✅ Production Ready
- Prod: 172.24.32.0/20 - ⏳ Ready for Deployment

### 4. AWS EKS Infrastructure (Legacy)
**Name**: AWS EKS Infrastructure with Karpenter
**Type**: Infrastructure as Code (Terraform)
**Status**: Maintenance
**Created**: 2025-11-01
**Location**: `project/platform-design/`

**Description**: Building production-ready AWS EKS cluster infrastructure with:
- Latest EKS version deployment via Terraform
- Karpenter for intelligent autoscaling
- Multi-architecture support (x86 and ARM64/Graviton)
- Spot instance integration for cost optimization
- Dedicated VPC with proper networking

## Project Structure
```
project/
├── snips/                # Snips organization projects
│   └── core-devops-infra/    # Main infrastructure repo
│       ├── terraform/        # IaC (22 modules)
│       ├── helm/             # Kubernetes packages
│       ├── docs/             # 30+ documentation files
│       ├── .github/workflows/# CI/CD pipelines
│       └── .claude/agents/   # Specialized AI agents
├── simplePage/           # SimplePage web application
│   ├── src/
│   │   └── server.js    # Express server
│   ├── public/
│   │   └── index.html   # Frontend UI
│   └── package.json
├── genai-enablement/     # GenAI Enablement program
│   ├── README.md         # Main project documentation
│   ├── docs/             # Role definitions, roadmaps
│   ├── research/         # Market analysis
│   └── templates/        # Reusable playbooks
├── platform-design/      # AWS EKS Infrastructure (Legacy)
│   ├── terraform/
│   │   └── modules/     # VPC, EKS, Karpenter modules
│   └── ...
```

## Task Tracking
**Method**: Markdown files (TODO.md)
**Location**: `project/TODO.md`

## Specialized Agents

### DevOps Engineer
**Role**: AWS, Terraform, and Kubernetes expertise
**Responsibilities**:
- Terraform module development
- EKS cluster configuration
- Karpenter setup and optimization
- AWS service integration
- CI/CD pipeline development

### Solution Architect
**Role**: Infrastructure design and best practices
**Responsibilities**:
- Architecture design and review
- Scalability and reliability planning
- Cost optimization strategies
- Multi-architecture design patterns
- Technology evaluation

### Security Expert
**Role**: AWS security and compliance
**Responsibilities**:
- IAM roles and policies
- Security groups and network ACLs
- Cluster security configuration
- Security scanning and hardening
- Secret management

### Site Reliability Engineer (SRE)
**Role**: Reliability and observability
**Responsibilities**:
- Monitoring and alerting setup
- Incident response procedures
- SLO/SLI definition
- Performance optimization
- Runbook development

## Automations

### Pre-commit Hooks
- Terraform fmt (formatting)
- Terraform validate (syntax checking)
- Security scanning (tfsec/checkov)
- Documentation linting

### CI/CD Checks
- Cost estimation (Infracost)
- Security scanning
- Terraform plan validation
- Documentation updates

### Script Utilities
- `scripts/validate.sh` - Run all validations
- `scripts/security-scan.sh` - Security checks
- `scripts/cost-estimate.sh` - Cost analysis

## Technology Stack
- **IaC**: Terraform (latest)
- **Cloud**: AWS
- **Container Orchestration**: Kubernetes (EKS)
- **Autoscaling**: Karpenter
- **Compute**: EC2 (x86 + Graviton), Spot Instances
- **Networking**: VPC, Subnets, NAT Gateway

## Goals & Success Criteria
- ✅ Terraform code deploys working EKS cluster
- ✅ Karpenter successfully provisions nodes
- ✅ Support for both x86 and ARM64 workloads
- ✅ Spot instances integrated for cost savings
- ✅ Clear documentation for developers
- ✅ Working examples demonstrate multi-arch deployment

## Git Repository
**Current**: /Users/lo/Develop/multi-agent-squad
**Branch**: main
**Remote**: (to be configured)

## Next Steps
1. Create Terraform modules (VPC, EKS, Karpenter)
2. Develop node pool configurations
3. Create Kubernetes example deployments
4. Write comprehensive README
5. Test end-to-end deployment
6. Set up automation scripts
