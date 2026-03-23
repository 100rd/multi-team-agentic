---
paths:
  - "**"
---

# Critical Decisions

Always ask for approval before:
- Deploying to production
- Deleting data or resources
- Modifying production configs
- Merging to main branch
- Creating public endpoints
- Changing security settings
- `terraform apply` or `terraform destroy`

Show decision format:
```
CRITICAL DECISION: [Action]
---
What: [Details]
Why: [Reasoning]
Risk: [Potential issues]

Do you approve? (y/n):
```
