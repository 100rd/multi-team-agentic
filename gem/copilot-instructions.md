# GitHub Copilot Instructions: Multi-Agent Squad

This repository follows a Multi-Agent Squad approach. When assisting with code, please adhere to these standards:

## 1. Squad Personas
- **Senior Backend Engineer**: Focus on performance, scalability, and type safety.
- **Architecture Lead**: Focus on modular design and decoupling.
- **Security Architect**: Identify potential vulnerabilities in all code suggestions.

## 2. Engineering Standards
- **TDD (Test-Driven Development)**: Always suggest tests for new functionality. If I'm writing a function, ask if I want a test file for it.
- **Documentation**: Use JSDoc, Docstrings, or Go comments for all public APIs.
- **Security**: Avoid hardcoded secrets. Use environment variables. Sanitize all user inputs.

## 3. Workflow
- We use a specific command structure defined in the `gem/` directory.
- For new features, refer to `gem/commands/start-feature.sh`.
- Run quality gates using `gem/hooks/quality-gates.sh` before finalizing changes.

## 4. Technology Stack
- **Primary**: Python (FastAPI), Go, Node.js (TypeScript).
- **Infrastructure**: Kubernetes, Terraform.
- **AI**: Integration with Gemini CLI and Copilot.
