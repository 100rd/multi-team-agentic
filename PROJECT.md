# Project Configuration

## Active Projects

### 1. GenAI Enablement
**Name**: GenAI Enablement - DevOps/SRE Adoption Program
**Type**: Implementation Plan & Knowledge Repository
**Status**: Research & Planning
**Created**: 2025-12-02
**Location**: `project/genai-enablement/`
**Remote**: https://github.com/100rd/genai-enablement

**Description**: Comprehensive GenAI adoption program for DevOps/SRE workflows. Enables project teams to use AI in real SDLC/SRE workflows through proven patterns, reusable playbooks, and measurable impact.

**Tech Stack**:
- Python (LangGraph for AI agents)
- AWS (Bedrock, CloudWatch, EventBridge)
- Terraform / Kubernetes
- Observability: Datadog / New Relic

**Key Workstreams**:
- Market research & tool analysis (40+ solutions) - Complete
- AI Incident Agent (LangGraph) - In Progress
- Playbooks & templates library - Not Started
- Team enablement workshops - Not Started

### 2. Platform Design (100rd/platform-design)
**Name**: Platform Design — Production-Grade Multi-Account AWS Platform
**Type**: Infrastructure as Code + GitOps Platform
**Status**: Active Development
**Created**: 2025-11-02
**Location**: `project/platform-design/`
**Remote**: https://github.com/100rd/platform-design

**Description**: Production-grade, multi-account AWS platform with EKS, Karpenter autoscaling, GitOps delivery via ArgoCD + Kargo, and full observability. Multi-region (4 EU regions) with Transit Gateway networking, Cilium CNI, OPA/Gatekeeper policies, and DNS failover controllers.

**Tech Stack**:
- Terraform + Terragrunt (multi-account, multi-region)
- EKS 1.34 + Karpenter 1.8.1 + Cilium 1.17.1
- ArgoCD + Kargo (progressive delivery)
- Prometheus + Grafana + Loki + Tempo + OpenTelemetry + Pyroscope
- OPA/Gatekeeper + Kyverno + External Secrets Operator

**Key Workstreams**:
- Foundation (VPC, EKS, Karpenter) — Complete
- Security baseline (OPA, secrets, network policies) — Complete
- Observability stack — Complete
- DNS failover controllers (Go) — Complete
- AWS provider version compatibility audit — Pending
- IAM/IRSA validation — Pending

### 3. Infrastructure (qbiq-ai/infra)
**Name**: qbiq-ai Infrastructure - AWS Control Tower Landing Zone
**Type**: Infrastructure as Code
**Status**: Active Development
**Location**: `project/infra/`

**Description**: AWS Control Tower multi-account landing zone managed with Terraform and Terragrunt. 9 accounts across 5 OUs (Management, Security, Infrastructure, Workloads, Sandbox). EKS 1.35 + Cilium 1.19 + ArgoCD 3.3 GitOps. CIS AWS Foundations Benchmark v3.0 compliance.

**Tech Stack**:
- Terraform 1.14.x + Terragrunt 0.99.x
- AWS Provider ~> 5.90
- EKS 1.35 + Cilium CNI 1.19 + ArgoCD 3.3
- GitHub Actions CI/CD
- Region: eu-west-1

**Phases**:
- Phase 0: Bootstrap & Foundation (#1, #2, #3)
- Phase 1: Control Tower & Landing Zone (#4, #5, #6)
- Phase 2: Network Architecture (#7, #8, #9, #38)
- Phase 3: Security Baseline (#10–#14, #37)
- Phase 4: Shared Services (#15–#17, #39, #40, #49)
- Phase 5: EKS & Cilium (#18–#20, #30–#32, #41–#43, #46–#48)
- Phase 6: ArgoCD & GitOps (#21, #22, #45)
- Phase 7: CI/CD Pipelines (#23, #24, #29)
- Phase 8: Observability (#25, #26, #44)
- Phase 9: Cost Optimization (#27, #28)

**Total Issues**: 46 (14 Critical, 21 High, 6 Medium) + #51 Version Matrix

## Project Structure
```
project/
├── your-project/         # Your project directory
│   ├── src/              # Source code
│   ├── tests/            # Test files
│   ├── docs/             # Project documentation
│   └── ...
```

## Task Tracking
**Method**: Markdown files (TODO.md) or GitHub Issues
**Location**: `project/TODO.md`

## Specialized Agents

Agents are defined in `.claude/agents/` (Claude Code) and `.github/agents/` (GitHub Copilot).

Available agent roles:
- **Solution Architect** - System design and best practices
- **Backend Engineer** - API and backend development
- **Frontend Engineer** - UI/UX implementation
- **DevOps Engineer** - CI/CD, infrastructure, deployment
- **Security Expert** - Security auditing and compliance
- **QA Engineer** - Testing and quality assurance
- **Product Manager** - Requirements and planning

## Automations

### Pre-commit Hooks
- Code formatting
- Linting and validation
- Security scanning
- Documentation linting

### CI/CD Checks
- Cost estimation (Infracost)
- Security scanning
- Plan validation
- Documentation updates

### Script Utilities
- `scripts/setup-git-hooks.sh` - Git hook configuration
- `scripts/generate-hooks.py` - Dynamic hook generation
- `scripts/discover-project.py` - Project discovery

## Git Repository
**Branch**: main
**Remote**: (to be configured)
