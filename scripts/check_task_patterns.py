#!/usr/bin/env python3
"""
Task Pattern Checker

Specifically validates Task() execution patterns in Claude Code agent files.
"""

import re
from pathlib import Path
from typing import Dict


class TaskPatternChecker:
    """Checker for Task() execution patterns in agent files."""

    def __init__(self, agents_dir: str = ".claude/agents"):
        self.agents_dir = Path(agents_dir)
        self.results: Dict[str, Dict] = {}

    def check_all_agents(self) -> Dict[str, Dict]:
        """Check Task() patterns in all agent files."""
        print("=== Task() Pattern Checker ===")
        print(f"Checking agents in: {self.agents_dir}")

        if not self.agents_dir.exists():
            print(f"❌ Agents directory not found: {self.agents_dir}")
            return {}

        agent_files = list(self.agents_dir.glob("*.md"))
        print(f"Found {len(agent_files)} agent files\n")

        for agent_file in agent_files:
            if agent_file.name != "secondary":  # Skip secondary directory
                result = self.check_agent_file(agent_file)
                self.results[agent_file.name] = result

        self.print_summary()
        return self.results

    def check_agent_file(self, file_path: Path) -> Dict:
        """Check Task() patterns in a single agent file."""
        agent_name = file_path.name.replace(".md", "")
        print(f"Checking: {agent_name}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            error_result = {
                "task_count": 0,
                "valid_patterns": 0,
                "errors": [f"Cannot read file: {e}"],
                "warnings": [],
                "status": "❌ ERROR",
            }
            print(f"  ❌ Cannot read file: {e}")
            return error_result

        # Count Task() occurrences
        task_patterns = re.findall(r"Task\(", content)
        task_count = len(task_patterns)

        # Find complete Task() blocks
        task_blocks = re.findall(
            r'Task\(\s*subagent_type="([^"]+)"\s*,\s*description="([^"]+)"\s*,\s*prompt="([^"]+)"\s*\)',
            content,
            re.DOTALL,
        )

        valid_patterns = len(task_blocks)
        errors = []
        warnings = []

        # Validate each Task() block
        for i, (subagent_type, description, prompt) in enumerate(task_blocks):
            block_num = i + 1

            # Validate subagent_type
            if not subagent_type.strip():
                errors.append(f"Task {block_num}: Empty subagent_type")
            elif not re.match(r"^[a-z-]+$", subagent_type):
                warnings.append(
                    f"Task {block_num}: Subagent type '{subagent_type}' should use lowercase with hyphens"
                )

            # Validate description
            if not description.strip():
                errors.append(f"Task {block_num}: Empty description")
            elif len(description.strip()) < 10:
                warnings.append(
                    f"Task {block_num}: Description too short ({len(description)} chars)"
                )

            # Validate prompt
            if not prompt.strip():
                errors.append(f"Task {block_num}: Empty prompt")
            elif len(prompt.strip()) < 20:
                warnings.append(
                    f"Task {block_num}: Prompt too short ({len(prompt)} chars)"
                )

        # Check for coordination language patterns
        coordination_patterns = [
            r"I\'ll coordinate .*? using \d+ tasks in parallel",
            r"Coordinating .*? using \d+ tasks in parallel",
            r"Analyzing .*? using parallel .*? across \d+ domains",
        ]

        coordination_found = False
        for pattern in coordination_patterns:
            if re.search(pattern, content):
                coordination_found = True
                break

        if not coordination_found and task_count > 0:
            warnings.append("No coordination language patterns found")

        # Determine status
        if errors:
            status = "❌ ERRORS"
        elif task_count == 0:
            status = "⚠️  NO TASKS"
        elif warnings:
            status = "🟡 WARNINGS"
        else:
            status = "✅ VALID"

        # Print results
        print(f"  Task() patterns: {task_count}")
        print(f"  Valid blocks: {valid_patterns}")
        print(f"  Status: {status}")

        if errors:
            for error in errors:
                print(f"    ❌ {error}")
        if warnings:
            for warning in warnings:
                print(f"    🟡 {warning}")

        print()  # Empty line

        return {
            "task_count": task_count,
            "valid_patterns": valid_patterns,
            "errors": errors,
            "warnings": warnings,
            "status": status,
            "coordination_language": coordination_found,
        }

    def print_summary(self):
        """Print summary of all results."""
        print("=== Summary ===")

        total_agents = len(self.results)
        agents_with_tasks = sum(1 for r in self.results.values() if r["task_count"] > 0)
        agents_with_errors = sum(1 for r in self.results.values() if r["errors"])
        agents_with_warnings = sum(1 for r in self.results.values() if r["warnings"])

        total_tasks = sum(r["task_count"] for r in self.results.values())
        total_valid = sum(r["valid_patterns"] for r in self.results.values())

        print(f"Total agents: {total_agents}")
        print(f"Agents with Task() patterns: {agents_with_tasks}")
        print(f"Agents with errors: {agents_with_errors}")
        print(f"Agents with warnings: {agents_with_warnings}")
        print(f"Total Task() patterns: {total_tasks}")
        print(f"Valid Task() blocks: {total_valid}")

        # Agents by status
        status_counts = {}
        for result in self.results.values():
            status = result["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        print("\nStatus breakdown:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")

        # Top agents by Task() count
        print("\nTop agents by Task() count:")
        sorted_agents = sorted(
            self.results.items(), key=lambda x: x[1]["task_count"], reverse=True
        )

        for agent_name, result in sorted_agents[:10]:
            agent_name = agent_name.replace(".md", "")
            print(f"  {agent_name}: {result['task_count']} patterns")


def main():
    """Main checking function."""
    checker = TaskPatternChecker()
    results = checker.check_all_agents()

    # Return appropriate exit code
    has_errors = any(r["errors"] for r in results.values())
    return 1 if has_errors else 0


if __name__ == "__main__":
    exit(main())
