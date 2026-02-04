---
name: create-agent
description: Create a new specialized agent for your project with rich experience and domain expertise
---

# Create Agent Command

Generate a new specialized agent tailored to your project's specific needs.

## What This Command Does

1. **Gathers Agent Requirements** - Role, expertise, experience level
2. **Selects Template** - Chooses appropriate base template
3. **Customizes for Project** - Adds project-specific context
4. **Generates Agent File** - Creates in `.claude/agents/`
5. **Registers Agent** - Updates agent registry

## Usage

- `/create-agent`
- "Create a new agent"
- "I need a [role] agent"

## Interactive Process

I'll ask you:

1. **Agent Role/Title** (e.g., "Database Performance Expert")
2. **Primary Responsibilities** (what they'll do)
3. **Experience Level** (5/10/15+ years)
4. **Domain Expertise** (specific technologies/industries)
5. **Tools Needed** (Read, Write, Bash, etc.)
6. **Unique Experiences** (war stories, specific achievements)

## Example Flow

```
You: /create-agent

Me: Let's create a new agent! What role or title should this agent have?

You: Blockchain Security Expert

Me: Great! What will be their primary responsibilities?

You: Audit smart contracts, identify vulnerabilities, ensure security best practices

Me: What experience level? (Junior: 5 years, Senior: 10 years, Principal: 15+ years)

You: Senior - 10 years

Me: What specific domain expertise should they have?

You: Solidity, Ethereum, DeFi protocols, past experience with major hacks

Me: Creating your Blockchain Security Expert...

✓ Generated: .claude/agents/security/blockchain-security-expert.md
✓ Added war stories from famous DeFi hacks
✓ Included audit checklist and tools
✓ Registered in agent manifest

Your new agent is ready! They bring:
- 10 years of blockchain security experience
- Expertise in Solidity and smart contract vulnerabilities
- Experience preventing attacks like the DAO hack
- Comprehensive audit methodology
```

## Agent Templates

Base templates available:
- **Developer** (Frontend/Backend/Full-Stack)
- **Architect** (Solution/System/Enterprise)
- **Manager** (Product/Project/Engineering)
- **Specialist** (Security/Performance/Data)
- **Quality** (QA/Testing/Automation)
- **Operations** (DevOps/SRE/Infrastructure)
- **Custom** (Any specialized role)

## Customization Options

Each agent can include:
- **Experience Level** - Years and company types
- **War Stories** - Real scenarios they've handled
- **Methodologies** - How they approach problems
- **Tools Mastery** - Specific tools and frameworks
- **Industry Knowledge** - Domain-specific expertise
- **Personality Traits** - Communication style
- **Output Formats** - How they structure deliverables

## Quick Creation

Specify details upfront:
```
/create-agent "ML Engineer" --experience=15 --speciality="Computer Vision"
/create-agent "Trading Systems Architect" --template=architect --domain=fintech
```

## Best Practices

1. **Be Specific** - "React Performance Expert" > "Frontend Developer"
2. **Add Context** - Include industry-specific knowledge
3. **Experience Matters** - War stories make better decisions
4. **Tool Selection** - Only include needed tools
5. **Clear Outputs** - Define how they should communicate

## Managing Agents

- **List Agents**: `/list-agents`
- **Update Agent**: `/update-agent [name]`
- **Remove Agent**: `/remove-agent [name]`

## Examples of Specialized Agents

- **Fintech**: "High-Frequency Trading Systems Expert"
- **Healthcare**: "HIPAA Compliance Specialist"
- **Gaming**: "Unity Performance Optimization Expert"
- **E-commerce**: "Conversion Rate Optimization Specialist"
- **Enterprise**: "Legacy System Migration Expert"