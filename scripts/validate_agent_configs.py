#!/usr/bin/env python3
"""
Agent Configuration Validator

Validates Claude Code agent .md files for proper structure, YAML frontmatter,
Task() patterns, and coordination documentation.
"""

import re
from pathlib import Path
from typing import List, Tuple


class AgentConfigValidator:
    """Validator for Claude Code agent configuration files."""

    def __init__(self, agents_dir: str = ".claude/agents"):
        self.agents_dir = Path(agents_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all_agents(self) -> Tuple[bool, List[str], List[str]]:
        """Validate all agent configuration files."""
        print("=== Claude Code Agent Configuration Validator ===")
        print(f"Validating agents in: {self.agents_dir}")

        if not self.agents_dir.exists():
            self.errors.append(f"Agents directory not found: {self.agents_dir}")
            return False, self.errors, self.warnings

        agent_files = list(self.agents_dir.glob("*.md"))
        print(f"Found {len(agent_files)} agent files")

        for agent_file in agent_files:
            if agent_file.name != "secondary":  # Skip secondary directory
                self.validate_agent_file(agent_file)

        success = len(self.errors) == 0
        print("\n=== Validation Results ===")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")

        return success, self.errors, self.warnings

    def validate_agent_file(self, file_path: Path) -> None:
        """Validate a single agent configuration file."""
        print(f"\nValidating: {file_path.name}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(f"{file_path.name}: Cannot read file - {e}")
            return

        # Validate YAML frontmatter
        self.validate_yaml_frontmatter(file_path.name, content)

        # Validate Task() patterns
        self.validate_task_patterns(file_path.name, content)

        # Validate content structure
        self.validate_content_structure(file_path.name, content)

    def validate_yaml_frontmatter(self, filename: str, content: str) -> None:
        """Validate YAML frontmatter structure."""
        yaml_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)

        if not yaml_match:
            self.errors.append(f"{filename}: Missing YAML frontmatter")
            return

        yaml_text = yaml_match.group(1)

        # Check required fields using simple regex patterns
        required_fields = {
            "name": r"name:\s*(.+)",
            "description": r"description:\s*(.+)",
            "tools": r"tools:\s*(.+)",
        }

        yaml_data = {}
        for field, pattern in required_fields.items():
            match = re.search(pattern, yaml_text)
            if match:
                yaml_data[field] = match.group(1).strip()
            else:
                self.errors.append(
                    f"{filename}: Missing required field '{field}' in YAML"
                )

        # Validate name matches filename
        if "name" in yaml_data:
            expected_name = filename.replace(".md", "")
            if yaml_data["name"] != expected_name:
                self.errors.append(
                    f"{filename}: Name '{yaml_data['name']}' doesn't match filename '{expected_name}'"
                )

        # Check tools field format
        if "tools" in yaml_data:
            tools = yaml_data["tools"]
            # Check if primary agents have Task tool
            if "Task" not in tools and filename != "secondary":
                self.warnings.append(f"{filename}: Primary agent missing 'Task' tool")

        if len(self.errors) == 0:
            print("  ✅ YAML frontmatter valid")

    def validate_task_patterns(self, filename: str, content: str) -> None:
        """Validate Task() execution patterns."""
        task_patterns = re.findall(r"Task\(", content)
        task_count = len(task_patterns)

        # Primary agents should have Task() patterns
        if task_count == 0:
            self.warnings.append(
                f"{filename}: No Task() patterns found (expected for primary agents)"
            )
        elif task_count < 5:
            self.warnings.append(
                f"{filename}: Only {task_count} Task() patterns found (recommended: 5+)"
            )
        else:
            print(f"  ✅ {task_count} Task() patterns found")

        # Validate Task() pattern structure
        task_blocks = re.findall(
            r'Task\(\s*subagent_type="([^"]+)"\s*,\s*description="([^"]+)"\s*,\s*prompt="([^"]+)"\s*\)',
            content,
            re.DOTALL,
        )

        for i, (subagent_type, description, prompt) in enumerate(task_blocks):
            if not subagent_type.strip():
                self.errors.append(
                    f"{filename}: Task() pattern {i+1} missing subagent_type"
                )
            if not description.strip() or len(description.strip()) < 10:
                self.errors.append(
                    f"{filename}: Task() pattern {i+1} description too short"
                )
            if not prompt.strip() or len(prompt.strip()) < 20:
                self.errors.append(f"{filename}: Task() pattern {i+1} prompt too short")

    def validate_content_structure(self, filename: str, content: str) -> None:
        """Validate agent content structure."""
        # Check for required sections
        required_sections = [
            r"# .+ Agent",  # Agent title
            r"## Core Responsibilities",  # Core responsibilities
            r"### UltraThink Analysis",  # UltraThink section
        ]

        for section_pattern in required_sections:
            if not re.search(section_pattern, content):
                self.warnings.append(
                    f"{filename}: Missing recommended section matching '{section_pattern}'"
                )

        # Check file length (recommended max 500 lines)
        line_count = len(content.split("\n"))
        if line_count > 500:
            self.warnings.append(
                f"{filename}: File has {line_count} lines (recommended max: 500)"
            )
        elif line_count < 50:
            self.warnings.append(
                f"{filename}: File has only {line_count} lines (seems too short)"
            )
        else:
            print(f"  ✅ Content structure valid ({line_count} lines)")


def main():
    """Main validation function."""
    validator = AgentConfigValidator()
    success, errors, warnings = validator.validate_all_agents()

    if errors:
        print("\n🔴 ERRORS:")
        for error in errors:
            print(f"  - {error}")

    if warnings:
        print("\n🟡 WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")

    if success:
        print("\n✅ All agent configurations are valid!")
        return 0
    else:
        print(f"\n❌ Validation failed with {len(errors)} errors")
        return 1


if __name__ == "__main__":
    exit(main())
