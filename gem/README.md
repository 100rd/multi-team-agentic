# Gemini & Copilot Multi-Agent Squad

This directory contains the alternative Multi-Agent Squad implementation for **Gemini CLI** and **GitHub Copilot**.

## 📂 Structure
- `agents/`: Markdown personas for Copilot Custom Agents and Gemini context.
- `commands/`: Shell scripts and automation logic.
- `config/`: Gemini CLI configuration (`config.toml`).
- `hooks/`: Quality gates and SDLC enforcement scripts.
- `copilot-instructions.md`: Global instructions for GitHub Copilot.

## 🚀 Getting Started

### 1. Gemini CLI Setup
Point your Gemini CLI to the custom config:
```bash
alias gemini="gemini --config ./gem/config/gemini-config.toml"
```

### 2. Using Commands
- **Start a feature**: `gemini start-feature "user-auth"`
- **Run quality gates**: `gemini check`
- **Check status**: `gemini status`

### 3. GitHub Copilot Integration
Ensure `gem/copilot-instructions.md` is active in your workspace. You can also use the agents in `gem/agents/` as custom agent profiles if your Copilot version supports `.github/agents/` or local profiles.

## 🤖 The Squad
- **Senior Backend Engineer**: Handles API and logic implementation.
- **Architecture Lead**: Handles system design and scaffolding.
- **Product Manager**: Handles requirements and user stories.

## 🛠 Workflow Enforcement
The squad follows a **Strict SDLC**:
1. Requirements (PM)
2. Design (Architecture)
3. Tests First (Engineering)
4. Quality Gates (Hooks)
5. Review & Merge
