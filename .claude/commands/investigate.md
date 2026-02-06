---
name: investigate
description: Launch competing hypothesis investigation with multiple agents testing different theories in parallel
args: "<problem-description> [--hypotheses N] [--adversarial]"
---

# Competing Hypothesis Investigation Command

Spawns multiple agents to investigate a problem from different angles simultaneously. Agents actively try to disprove each other's theories, converging on the most likely root cause.

## Why This Pattern

Single-agent investigation suffers from **anchoring bias**: once one theory is explored, subsequent investigation is biased toward it. With multiple independent investigators actively challenging each other, the theory that survives is much more likely to be the actual root cause.

## What This Command Does

1. **Analyzes the problem** to generate N competing hypotheses
2. **Spawns one agent per hypothesis** (default: 3-5)
3. **Each agent investigates** their assigned theory
4. **Agents message each other** to challenge findings
5. **Lead synthesizes** the surviving theory into a diagnosis
6. **Creates action plan** based on the proven root cause

## Arguments

- `problem-description`: Description of the issue to investigate
- `--hypotheses N`: Number of hypotheses to test (default: 3, max: 5)
- `--adversarial`: Enable adversarial mode where agents explicitly try to disprove each other (default: true)

## Execution Flow

### Phase 1: Hypothesis Generation

The Lead analyzes the problem and generates N distinct hypotheses:

```markdown
## Problem: [description]

### Hypothesis 1: [Theory A]
Investigation approach: [what to check]
Expected evidence if true: [what we'd find]
Expected evidence if false: [what we'd find]

### Hypothesis 2: [Theory B]
...

### Hypothesis 3: [Theory C]
...
```

### Phase 2: Parallel Investigation

Each agent is spawned with:
```
You are Investigator {N} on a competing hypothesis team.

PROBLEM: {problem_description}

YOUR HYPOTHESIS: {hypothesis}
COMPETING HYPOTHESES: {list of all others}

YOUR JOB:
1. Investigate YOUR hypothesis thoroughly
2. Look for evidence that SUPPORTS it
3. Look for evidence that DISPROVES it
4. Actively challenge other investigators' findings
5. If you find evidence against a competing hypothesis, message that investigator

INVESTIGATION CHECKLIST:
- [ ] Check relevant logs and error messages
- [ ] Review recent changes (git log, terraform state)
- [ ] Examine configuration files
- [ ] Run diagnostic commands
- [ ] Test the hypothesis with a minimal reproduction
- [ ] Document all evidence (for AND against)

COMMUNICATION:
- Message other investigators when you find evidence against their theory
- Message the Lead with your findings
- Be honest: if your hypothesis is disproven, say so

REPORT FORMAT:
FINDING: hypothesis={N} status=[confirmed|disproven|inconclusive]
EVIDENCE_FOR: [list]
EVIDENCE_AGAINST: [list]
CONFIDENCE: [0-100]%
RECOMMENDATION: [action to take if this is the cause]
```

### Phase 3: Adversarial Debate

Once initial investigation is complete:
1. Each agent shares their findings
2. Agents challenge each other's evidence
3. Agents can run additional checks to verify/disprove
4. Lead monitors the debate and asks pointed questions

### Phase 4: Convergence

The Lead synthesizes findings:
```markdown
## Investigation Results

### Surviving Hypothesis: [the winner]
Confidence: [X]%
Key Evidence: [what proved it]
Disproven Alternatives: [and why]

### Root Cause Analysis
[Detailed explanation]

### Action Plan
1. [Immediate fix]
2. [Preventive measure]
3. [Monitoring to add]

### Lessons Learned
[What to document for future reference]
```

## Use Cases

### Infrastructure Debugging
```
/investigate "EKS pods are OOMKilled after 2 hours of running"
```
Hypotheses generated:
1. Memory leak in application code
2. Insufficient resource limits/requests
3. Sidecar container consuming excessive memory
4. Node memory pressure from DaemonSets
5. JVM heap misconfiguration

### Terraform State Issues
```
/investigate "terraform plan shows 15 resources to recreate that shouldn't change"
```
Hypotheses generated:
1. State file corruption or drift
2. Provider version change with breaking defaults
3. Module source updated with different resource naming
4. Backend configuration mismatch

### Performance Degradation
```
/investigate "API latency increased 3x after last deployment" --hypotheses 4
```
Hypotheses generated:
1. N+1 query introduced in new code
2. Connection pool exhaustion
3. SSL certificate re-negotiation on every request
4. Auto-scaling not responding to load pattern

### Network Issues
```
/investigate "Intermittent 503 errors on production ALB" --adversarial
```
Hypotheses generated:
1. Backend health check failing intermittently
2. Security group rule blocking specific traffic
3. Target group deregistration during rolling update
4. DNS caching causing stale endpoint resolution

## Integration with Infrastructure Team

After investigation completes, if a fix is identified:
```
/investigate found root cause → /infra-team implement the fix
```

The investigation findings are passed to the infrastructure team as context.

## Agent Types Used

| Role | Agent Type | Why |
|------|-----------|-----|
| Lead | prime-orchestrator | Coordinates investigation, synthesizes results |
| Investigators | Varies by domain: | |
| - Infra issues | devops-engineer | K8s, network, cloud expertise |
| - Terraform issues | terraform-engineer | State, modules, providers |
| - Security issues | security-expert | IAM, network, compliance |
| - Architecture issues | solution-architect | Design, scaling, patterns |
| - General issues | general-purpose | Broad investigation |

## Best Practices

1. **Be specific about the problem**: Include error messages, timeframes, affected systems
2. **3-5 hypotheses is optimal**: Fewer misses possibilities, more wastes tokens
3. **Enable adversarial mode**: The debate is where truth emerges
4. **Don't anchor**: Let agents form their own conclusions before sharing
5. **Follow up**: The winning hypothesis should lead to a concrete action
