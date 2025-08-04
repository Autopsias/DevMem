---
description: Automatically stage changes and generate best practice CI commit messages with quality validation and conventional commit format
allowed-tools: [Bash, Read, Grep, Glob]
argument-hint: "[optional: file paths or --quality-check or --auto-fix] - Stage specific files, run quality validation, or attempt automatic fixes"
---

# Git Commit Assistant with Quality Validation

Automatically validate code quality, stage changes, and generate professional commit messages: ${ARGUMENTS:-all changes with quality validation}

This command handles Git operations with quality validation, naturally engaging specialized commit management expertise.

**Enhanced Core Functions:**
- **Quality Gate Enforcement**: Run pre-commit hooks and code guidelines validation BEFORE staging
- **Violation Prevention**: Block commits that would fail during push due to quality issues
- **Smart Auto-Fixing**: Automatically fix simple formatting, linting, and import issues
- **Agent Coordination**: Recommend specialist agents for complex quality violations
- **Intelligent Staging**: Stage changes only after all quality checks pass
- **Professional Messages**: Generate conventional commit messages with proper formatting

**Quality Validation Features:**
- **Pre-Commit Hook Execution**: Run `pre-commit run --all-files` before staging
- **Code Guidelines Check**: Validate function length (50 lines), file length (750/1000 lines), naming conventions
- **Working Directory Analysis**: Check for unstaged changes and mixed commit states
- **Violation Remediation**: Provide specific fix recommendations and agent coordination suggestions

**Commit Message Standards:**
- Conventional commit format: `type(scope): description`
- Enhanced types: feat, fix, chore, docs, test, refactor, style, ci
- Claude Code footer: `🤖 Generated with [Claude Code](https://claude.ai/code)`
- Co-Authored-By attribution when appropriate
- Subject line under 72 characters with imperative mood

**Usage Examples:**
- `/commit` - Run quality validation, stage all changes, and generate commit message
- `/commit --quality-check` - Run comprehensive quality validation before staging
- `/commit --auto-fix` - Attempt to automatically fix quality violations
- `/commit --staged` - Generate message for already staged changes (skip validation)
- `/commit src/api.py tests/test_api.py` - Validate and stage specific files only
- `/commit --help` - Show detailed usage and quality validation examples

**Quality Failure Handling:**
- **Violation Detection**: Identify specific code guideline violations with file locations
- **Fix Recommendations**: Provide actionable guidance for resolving each violation type
- **Agent Suggestions**: Recommend appropriate specialist agents for complex issues:
  - `code-quality-specialist` for systematic quality improvements
  - `linting-engineer` for comprehensive style enforcement
  - `refactoring-coordinator` for large-scale function extraction

**Expected Output:**
Complete git commit command ready for execution with professional, descriptive commit message following project standards, conventional commit practices, and guaranteed to pass pre-commit hooks during push.

**Push Failure Prevention:**
This enhanced workflow prevents the common "failed to push some refs" error by catching and resolving code quality violations locally before they reach the remote repository. Quality validation ensures commits are CI-ready and comply with all project standards.

**Integration:**
Seamlessly integrates with existing git workflow, CI/CD pipeline preparation, and the project's agent ecosystem for comprehensive code quality enforcement and collaborative development practices.