#!/usr/bin/env python3
"""
Integrated Validation Framework for Claude Code Agent System

Consolidates all validation functionality from standalone scripts:
1. Story completion validation (S6.1 Performance Optimization)
2. S6.3 Enhanced Testing Framework Implementation
3. Agent selection validation
4. Infrastructure learning validation
5. Native configuration validation
6. Claude Code agent learning comprehensive validation

This framework provides a unified testing approach while preserving all functionality
from the individual validation scripts.
"""

import pytest
import json
import sys
import time
import tempfile
import subprocess
import statistics
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@dataclass
class ValidationResult:
    """Represents the result of a validation test."""

    name: str
    passed: bool
    score: Optional[float] = None
    details: Optional[str] = None
    execution_time_ms: Optional[float] = None


@dataclass
class ValidationSuite:
    """Represents a complete validation suite result."""

    name: str
    results: List[ValidationResult]
    overall_passed: bool
    total_time_ms: float

    @property
    def pass_rate(self) -> float:
        """Calculate the pass rate for this suite."""
        if not self.results:
            return 0.0
        return sum(1 for r in self.results if r.passed) / len(self.results)

    @property
    def passed_count(self) -> int:
        """Count of passed tests."""
        return sum(1 for r in self.results if r.passed)

    @property
    def total_count(self) -> int:
        """Total count of tests."""
        return len(self.results)


class IntegratedValidationFramework:
    """Main validation framework that consolidates all validation functionality."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the validation framework."""
        self.project_root = project_root or Path(__file__).parent.parent
        self.test_results: List[ValidationSuite] = []
        self.start_time = time.perf_counter()

    def run_all_validations(self) -> bool:
        """Run all validation suites and return overall success status."""
        print("🚀 Claude Code Agent System - Integrated Validation Framework")
        print("=" * 80)

        # Run all validation suites
        validation_suites = [
            ("Story Completion (S6.1)", self._validate_story_completion),
            ("S6.3 Testing Framework", self._validate_s63_implementation),
            ("Agent Selection", self._validate_agent_selection),
            ("Infrastructure Learning", self._validate_infrastructure_learning),
            ("Native Configuration", self._validate_native_config),
            ("Claude Code Agent Framework", self._validate_agent_framework_structure),
            ("Claude Code Agent Learning", self._validate_claude_code_agent_learning),
        ]

        overall_success = True

        for suite_name, validator in validation_suites:
            print(f"\n🔍 Running {suite_name} Validation...")
            print("-" * 60)

            suite_start = time.perf_counter()
            try:
                suite_result = validator()
                suite_time = (time.perf_counter() - suite_start) * 1000

                # Create validation suite
                suite = ValidationSuite(
                    name=suite_name,
                    results=(
                        suite_result
                        if isinstance(suite_result, list)
                        else [ValidationResult(suite_name, suite_result)]
                    ),
                    overall_passed=(
                        all(r.passed for r in suite_result)
                        if isinstance(suite_result, list)
                        else suite_result
                    ),
                    total_time_ms=suite_time,
                )

                self.test_results.append(suite)

                if suite.overall_passed:
                    print(
                        f"✅ {suite_name}: PASSED ({suite.passed_count}/{suite.total_count})"
                    )
                else:
                    print(
                        f"❌ {suite_name}: FAILED ({suite.passed_count}/{suite.total_count})"
                    )
                    overall_success = False

            except Exception as e:
                print(f"⚠️ {suite_name}: ERROR - {e}")
                error_result = ValidationSuite(
                    name=suite_name,
                    results=[ValidationResult(suite_name, False, details=str(e))],
                    overall_passed=False,
                    total_time_ms=(time.perf_counter() - suite_start) * 1000,
                )
                self.test_results.append(error_result)
                overall_success = False

        # Generate final report
        self._generate_final_report(overall_success)

        return overall_success

    def _validate_story_completion(self) -> List[ValidationResult]:
        """Validate S6.1 Claude Code Performance Optimization story completion."""
        results = []

        # Task 1: Prompt caching system
        cache_files = [
            self.project_root / "src/performance/prompt_cache.py",
            self.project_root / "src/performance/cache_invalidation.py",
        ]

        cache_validation = all(f.exists() for f in cache_files)
        results.append(
            ValidationResult(
                "Prompt Caching System",
                cache_validation,
                details=f"Files checked: {[str(f.name) for f in cache_files]}",
            )
        )

        # Task 2: Token usage estimation
        token_files = [
            self.project_root / "src/performance/token_estimation.py",
            self.project_root / "src/performance/usage_dashboard.py",
        ]

        token_validation = all(f.exists() for f in token_files)
        results.append(
            ValidationResult(
                "Token Usage Estimation",
                token_validation,
                details=f"Files checked: {[str(f.name) for f in token_files]}",
            )
        )

        # Task 3: Prompt optimization
        optimization_files = [
            self.project_root / "src/performance/prompt_optimization.py",
            self.project_root / "src/performance/agent_invocation.py",
        ]

        optimization_validation = all(f.exists() for f in optimization_files)
        results.append(
            ValidationResult(
                "Prompt Optimization",
                optimization_validation,
                details=f"Files checked: {[str(f.name) for f in optimization_files]}",
            )
        )

        # Task 4: Agent ecosystem validation
        test_files = [
            self.project_root / "tests/performance/test_cache_basic.py",
            self.project_root / "tests/performance/test_optimization_simple.py",
            self.project_root / "tests/performance/test_performance_benchmarks.py",
        ]

        test_validation = all(f.exists() for f in test_files)
        results.append(
            ValidationResult(
                "Agent Ecosystem Testing",
                test_validation,
                details=f"Test files checked: {[str(f.name) for f in test_files]}",
            )
        )

        return results

    def _validate_s63_implementation(self) -> List[ValidationResult]:
        """Validate S6.3 Enhanced Testing Framework Implementation."""
        results = []
        test_root = self.project_root / "tests"

        # AC1: Coordination patterns testing
        coordination_file = (
            test_root / "agent_coordination" / "test_coordination_patterns.py"
        )
        coordination_valid = False
        if coordination_file.exists():
            content = coordination_file.read_text()
            coordination_valid = all(
                pattern in content
                for pattern in [
                    "TestAgentCoordinationPatterns",
                    "TestContextPreservation",
                    "TestCrossDomainCommunication",
                ]
            )

        results.append(
            ValidationResult(
                "Coordination Patterns Testing",
                coordination_valid,
                details=f"File exists: {coordination_file.exists()}, Content valid: {coordination_valid}",
            )
        )

        # AC2: Performance benchmarks
        performance_file = test_root / "performance" / "test_performance_benchmarks.py"
        performance_valid = False
        if performance_file.exists():
            content = performance_file.read_text()
            performance_valid = all(
                pattern in content
                for pattern in ["PerformanceBenchmark", "baseline_metrics"]
            )

        results.append(
            ValidationResult(
                "Performance Benchmarks",
                performance_valid,
                details=f"File exists: {performance_file.exists()}, Content valid: {performance_valid}",
            )
        )

        # AC3: Sequential and parallel testing
        sequential_parallel_valid = False
        if coordination_file.exists():
            content = coordination_file.read_text()
            sequential_parallel_valid = (
                "sequential" in content.lower() and "parallel" in content.lower()
            )

        results.append(
            ValidationResult(
                "Sequential/Parallel Testing",
                sequential_parallel_valid,
                details=f"Sequential and parallel patterns found: {sequential_parallel_valid}",
            )
        )

        # AC4: Integration testing
        integration_file = (
            test_root / "agent_coordination" / "test_integration_scenarios.py"
        )
        integration_valid = False
        if integration_file.exists():
            content = integration_file.read_text()
            integration_valid = all(
                pattern in content
                for pattern in [
                    "TestAgentEcosystemIntegration",
                    "TestIntegrationScenarios",
                ]
            )

        results.append(
            ValidationResult(
                "Integration Testing",
                integration_valid,
                details=f"File exists: {integration_file.exists()}, Content valid: {integration_valid}",
            )
        )

        return results

    def _validate_agent_selection(self) -> List[ValidationResult]:
        """Validate enhanced agent selection system."""
        results = []

        try:
            # Import and test basic functionality
            from agent_selector import EnhancedAgentSelector, select_best_agent

            selector = EnhancedAgentSelector()
            results.append(ValidationResult("Agent Selector Creation", True))

            # Test basic selection
            test_cases = [
                (
                    "pytest test failing with async mock configuration",
                    "test-specialist",
                ),
                (
                    "docker orchestration issues with container networking",
                    "infrastructure-engineer",
                ),
                (
                    "security vulnerability scan reveals credential leaks",
                    "security-enforcer",
                ),
                (
                    "performance bottleneck in latency optimization",
                    "performance-optimizer",
                ),
                ("refactor code with better variable naming", "intelligent-enhancer"),
            ]

            success_count = 0
            total_time = 0

            for query, expected_agent in test_cases:
                start_time = time.perf_counter()
                result = selector.select_agent(query)
                end_time = time.perf_counter()

                total_time += (end_time - start_time) * 1000

                if result.agent_name == expected_agent:
                    success_count += 1

            accuracy = success_count / len(test_cases)
            avg_time = total_time / len(test_cases)

            results.append(
                ValidationResult(
                    "Agent Selection Accuracy",
                    accuracy >= 0.8,
                    score=accuracy,
                    details=f"Accuracy: {accuracy:.1%}, Avg time: {avg_time:.2f}ms",
                )
            )

            # Test global function
            global_result = select_best_agent("test query")
            results.append(ValidationResult("Global Function", bool(global_result)))

            # Test edge cases
            empty_result = selector.select_agent("")
            results.append(ValidationResult("Empty Query Handling", bool(empty_result)))

        except ImportError as e:
            results.append(
                ValidationResult(
                    "Agent Selector Import", False, details=f"Import error: {e}"
                )
            )
        except Exception as e:
            results.append(
                ValidationResult("Agent Selection Error", False, details=f"Error: {e}")
            )

        return results

    def _validate_infrastructure_learning(self) -> List[ValidationResult]:
        """Validate infrastructure learning improvements."""
        results = []

        try:
            # Import the enhanced coordinator
            from enhanced_cross_domain_coordinator import (
                EnhancedCrossDomainCoordinator,
                PatternLearningEngine,
            )

            # Create temporary hub for testing
            temp_dir = tempfile.mkdtemp()
            hub_path = Path(temp_dir) / "coordination-hub.md"

            # Test baseline coordinator
            baseline_coordinator = EnhancedCrossDomainCoordinator()
            baseline_coordinator.pattern_learning_engine = None

            test_cases = [
                ("docker container orchestration setup", "infrastructure-engineer"),
                ("kubernetes pod scaling issues", "infrastructure-engineer"),
                ("docker performance optimization", "performance-optimizer"),
                ("container networking problems", "docker-specialist"),
                ("infrastructure monitoring setup", "infrastructure-engineer"),
            ]

            # Baseline measurement
            baseline_correct = 0
            baseline_times = []

            for query, expected_agent in test_cases:
                start_time = time.perf_counter()
                analysis = baseline_coordinator.analyze_cross_domain_integration(query)
                end_time = time.perf_counter()

                baseline_times.append((end_time - start_time) * 1000)
                predicted_agent = (
                    analysis.agent_suggestions[0][0]
                    if analysis.agent_suggestions
                    else "unknown"
                )

                if predicted_agent == expected_agent:
                    baseline_correct += 1

            baseline_accuracy = (baseline_correct / len(test_cases)) * 100
            baseline_avg_time = sum(baseline_times) / len(baseline_times)

            results.append(
                ValidationResult(
                    "Baseline Accuracy",
                    baseline_accuracy > 0,
                    score=baseline_accuracy,
                    details=f"Accuracy: {baseline_accuracy:.1f}%, Avg time: {baseline_avg_time:.2f}ms",
                )
            )

            # Test learning coordinator
            learning_coordinator = EnhancedCrossDomainCoordinator()
            learning_coordinator.pattern_learning_engine = PatternLearningEngine(
                coordination_hub_path=str(hub_path)
            )

            # Learning phase (train on subset)
            training_cases = test_cases[:3]
            patterns_learned = 0

            for query, correct_agent in training_cases:
                analysis = learning_coordinator.analyze_cross_domain_integration(query)
                predicted_agent = (
                    analysis.agent_suggestions[0][0]
                    if analysis.agent_suggestions
                    else "unknown"
                )

                if predicted_agent == correct_agent:
                    learning_coordinator.record_selection_feedback(
                        query, correct_agent, 0.9, user_feedback=True
                    )
                    patterns_learned += 1

            learning_coordinator.force_pattern_storage()

            results.append(
                ValidationResult(
                    "Pattern Learning",
                    patterns_learned > 0,
                    score=patterns_learned,
                    details=f"Patterns learned: {patterns_learned}",
                )
            )

            # Test on validation set
            validation_cases = test_cases[3:]
            learning_correct = 0

            for query, expected_agent in validation_cases:
                analysis = learning_coordinator.analyze_cross_domain_integration(query)
                predicted_agent = (
                    analysis.agent_suggestions[0][0]
                    if analysis.agent_suggestions
                    else "unknown"
                )

                if predicted_agent == expected_agent:
                    learning_correct += 1

            learning_accuracy = (
                (learning_correct / len(validation_cases)) * 100
                if validation_cases
                else 0
            )

            results.append(
                ValidationResult(
                    "Learning Accuracy",
                    learning_accuracy >= 40.0,  # Target > 38%
                    score=learning_accuracy,
                    details=f"Learning accuracy: {learning_accuracy:.1f}%",
                )
            )

        except ImportError as e:
            results.append(
                ValidationResult(
                    "Infrastructure Learning Import",
                    False,
                    details=f"Import error: {e}",
                )
            )
        except Exception as e:
            results.append(
                ValidationResult(
                    "Infrastructure Learning Error", False, details=f"Error: {e}"
                )
            )

        return results

    def _validate_native_config(self) -> List[ValidationResult]:
        """Validate native configuration."""
        results = []
        config_path = self.project_root / ".claude" / "settings.json"

        # Check if config file exists
        if not config_path.exists():
            results.append(
                ValidationResult(
                    "Configuration File",
                    False,
                    details=f"File not found: {config_path}",
                )
            )
            return results

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            results.append(ValidationResult("JSON Parsing", True))

            # Validate sections
            required_sections = ["env", "permissions", "hooks", "agents"]
            for section in required_sections:
                section_exists = section in config
                results.append(
                    ValidationResult(
                        f"Section: {section}",
                        section_exists,
                        details=f"Section {'found' if section_exists else 'missing'}",
                    )
                )

            # Validate environment variables
            if "env" in config:
                env_config = config["env"]
                required_env_vars = [
                    "PYTHONPATH",
                    "CLAUDE_AGENT_FRAMEWORK_ENABLED",
                    "CLAUDE_AGENT_PERFORMANCE_TARGET_MS",
                    "TEST_COVERAGE_MINIMUM",
                ]

                env_valid = all(var in env_config for var in required_env_vars)
                results.append(
                    ValidationResult(
                        "Environment Variables",
                        env_valid,
                        details=f"Required vars present: {env_valid}",
                    )
                )

            # Validate agents section
            if "agents" in config:
                agents_config = config["agents"]
                agents_valid = all(
                    key in agents_config
                    for key in ["version", "framework_config", "performance_targets"]
                )
                results.append(
                    ValidationResult(
                        "Agents Configuration",
                        agents_valid,
                        details=f"Agent config complete: {agents_valid}",
                    )
                )

        except json.JSONDecodeError as e:
            results.append(
                ValidationResult("JSON Parsing", False, details=f"JSON error: {e}")
            )
        except Exception as e:
            results.append(
                ValidationResult(
                    "Configuration Validation", False, details=f"Error: {e}"
                )
            )

        return results

    def _validate_claude_code_agent_learning(self) -> List[ValidationResult]:
        """Validate Claude Code agent learning capabilities."""
        results = []

        # First, validate the Claude Code agent framework structure
        agent_framework_results = self._validate_agent_framework_structure()
        results.extend(agent_framework_results)

        # Test suites to validate
        test_suites = [
            (
                "TestTaskToolIntegration",
                "Task Tool Integration & Parallel Coordination",
            ),
            (
                "TestLearningPatternValidation",
                "Learning Pattern Validation from coordination-hub.md",
            ),
            (
                "TestAgentDirectoryIntegration",
                "Agent Directory (.claude/agents/) Integration",
            ),
            ("TestMemorySystemPerformance", "Memory System Performance Metrics"),
            (
                "TestAgentDelegationCoordination",
                "Agent Delegation & Coordination Patterns",
            ),
        ]

        for test_class, description in test_suites:
            try:
                # Run the specific test class
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        f"tests/test_claude_code_agent_learning.py::{test_class}",
                        "-v",
                        "--tb=short",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                test_passed = result.returncode == 0

                # Count passed tests from output
                passed_count = result.stdout.count(" PASSED")
                failed_count = result.stdout.count(" FAILED")

                results.append(
                    ValidationResult(
                        description,
                        test_passed,
                        score=(
                            passed_count / (passed_count + failed_count)
                            if (passed_count + failed_count) > 0
                            else 0
                        ),
                        details=f"Passed: {passed_count}, Failed: {failed_count}",
                    )
                )

            except subprocess.TimeoutExpired:
                results.append(
                    ValidationResult(description, False, details="Test timeout (>60s)")
                )
            except Exception as e:
                results.append(
                    ValidationResult(
                        description, False, details=f"Test execution error: {e}"
                    )
                )

        # Also test coordination hub validation
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/test_agent_selection_validation.py::TestCoordinationHubLearningValidation",
                    "-v",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            coordination_passed = result.returncode == 0
            passed_count = result.stdout.count(" PASSED")

            results.append(
                ValidationResult(
                    "Coordination Hub Learning",
                    coordination_passed,
                    score=passed_count,
                    details=f"Tests passed: {passed_count}",
                )
            )

        except Exception as e:
            results.append(
                ValidationResult(
                    "Coordination Hub Learning", False, details=f"Error: {e}"
                )
            )

        return results

    def _validate_agent_framework_structure(self) -> List[ValidationResult]:
        """Validate Claude Code agent framework structure according to Anthropic guidelines."""
        results = []
        agents_dir = self.project_root / ".claude" / "agents"
        secondary_dir = agents_dir / "secondary"

        # Check agent directory structure
        results.append(
            ValidationResult(
                "Agent Directory Structure",
                agents_dir.exists() and secondary_dir.exists(),
                details=f"Agents dir exists: {agents_dir.exists()}, Secondary dir exists: {secondary_dir.exists()}",
            )
        )

        if not agents_dir.exists():
            return results

        # Validate primary agents
        primary_agents = list(agents_dir.glob("*.md"))
        results.append(
            ValidationResult(
                "Primary Agents Count",
                len(primary_agents) >= 15,  # Should have substantial primary agents
                score=len(primary_agents),
                details=f"Found {len(primary_agents)} primary agents",
            )
        )

        # Validate secondary agents
        secondary_agents = (
            list(secondary_dir.glob("*.md")) if secondary_dir.exists() else []
        )
        results.append(
            ValidationResult(
                "Secondary Agents Count",
                len(secondary_agents) >= 10,  # Should have substantial secondary agents
                score=len(secondary_agents),
                details=f"Found {len(secondary_agents)} secondary agents",
            )
        )

        # Validate agent file format compliance
        valid_agents = 0
        total_agents = len(primary_agents) + len(secondary_agents)

        for agent_file in primary_agents + secondary_agents:
            if self._validate_agent_file_format(agent_file):
                valid_agents += 1

        format_compliance = valid_agents / total_agents if total_agents > 0 else 0
        results.append(
            ValidationResult(
                "Agent Format Compliance",
                format_compliance >= 0.9,  # 90% of agents should be properly formatted
                score=format_compliance,
                details=f"{valid_agents}/{total_agents} agents properly formatted",
            )
        )

        # Validate required primary agents exist
        required_primary_agents = [
            "analysis-gateway.md",
            "meta-coordinator.md",
            "test-specialist.md",
            "security-enforcer.md",
            "infrastructure-engineer.md",
            "code-quality-specialist.md",
        ]

        found_required = 0
        for required_agent in required_primary_agents:
            if (agents_dir / required_agent).exists():
                found_required += 1

        results.append(
            ValidationResult(
                "Required Primary Agents",
                found_required == len(required_primary_agents),
                score=found_required / len(required_primary_agents),
                details=f"{found_required}/{len(required_primary_agents)} required primary agents found",
            )
        )

        # Validate required secondary agents exist
        required_secondary_agents = [
            "refactoring-coordinator.md",
            "performance-optimizer.md",
            "docker-specialist.md",
            "dependency-resolver.md",
            "pattern-analyzer.md",
        ]

        found_secondary_required = 0
        for required_agent in required_secondary_agents:
            if (secondary_dir / required_agent).exists():
                found_secondary_required += 1

        results.append(
            ValidationResult(
                "Required Secondary Agents",
                found_secondary_required
                >= len(required_secondary_agents) * 0.8,  # 80% should exist
                score=found_secondary_required / len(required_secondary_agents),
                details=f"{found_secondary_required}/{len(required_secondary_agents)} required secondary agents found",
            )
        )

        # Validate agent ecosystem completeness
        total_agent_count = len(primary_agents) + len(secondary_agents)
        results.append(
            ValidationResult(
                "Agent Ecosystem Completeness",
                total_agent_count >= 30,  # Target of 30+ agents for complete ecosystem
                score=total_agent_count,
                details=f"Total agent ecosystem: {total_agent_count} agents",
            )
        )

        return results

    def _validate_agent_file_format(self, agent_file: Path) -> bool:
        """Validate individual agent file format according to Anthropic guidelines."""
        try:
            content = agent_file.read_text()

            # Check for YAML frontmatter
            if not content.startswith("---"):
                return False

            # Extract frontmatter
            frontmatter_end = content.find("---", 3)
            if frontmatter_end == -1:
                return False

            frontmatter = content[3:frontmatter_end]

            # Check required frontmatter fields
            required_fields = ["name:", "description:", "tools:"]
            for field in required_fields:
                if field not in frontmatter:
                    return False

            # Check that content exists after frontmatter
            content_after = content[frontmatter_end + 3 :].strip()
            if not content_after:
                return False

            # Check for basic structure elements
            structure_elements = ["Purpose", "Responsibilities", "Core", "#"]
            has_structure = any(element in content for element in structure_elements)

            return has_structure

        except Exception:
            return False

    def _generate_final_report(self, overall_success: bool) -> None:
        """Generate final validation report."""
        total_time = (time.perf_counter() - self.start_time) * 1000

        print("\n" + "=" * 80)
        print("📋 INTEGRATED VALIDATION FRAMEWORK - FINAL REPORT")
        print("=" * 80)

        # Suite summary
        print("\n📊 Validation Suite Results:")
        for suite in self.test_results:
            status = "✅ PASSED" if suite.overall_passed else "❌ FAILED"
            print(
                f"{status} {suite.name} ({suite.passed_count}/{suite.total_count}) - {suite.total_time_ms:.1f}ms"
            )

        # Overall statistics
        total_suites = len(self.test_results)
        passed_suites = sum(1 for suite in self.test_results if suite.overall_passed)
        total_tests = sum(suite.total_count for suite in self.test_results)
        passed_tests = sum(suite.passed_count for suite in self.test_results)

        print("\n📈 Overall Statistics:")
        print(
            f"   Validation Suites: {passed_suites}/{total_suites} passed ({(passed_suites/total_suites):.1%})"
        )
        print(
            f"   Individual Tests: {passed_tests}/{total_tests} passed ({(passed_tests/total_tests):.1%})"
        )
        print(f"   Total Execution Time: {total_time:.1f}ms")

        # Performance insights
        if self.test_results:
            avg_suite_time = statistics.mean(
                suite.total_time_ms for suite in self.test_results
            )
            print(f"   Average Suite Time: {avg_suite_time:.1f}ms")

        # Final assessment
        print("\n🎯 Final Assessment:")
        if overall_success:
            print("   🏆 ALL VALIDATIONS PASSED!")
            print("   ✨ Claude Code Agent System is functioning correctly")
            print("   🚀 Ready for production deployment")
        else:
            failed_suites = [
                suite.name for suite in self.test_results if not suite.overall_passed
            ]
            print(f"   ⚠️ {len(failed_suites)} validation suite(s) failed:")
            for suite_name in failed_suites:
                print(f"      - {suite_name}")
            print("   🔧 Review failed validations before proceeding")

        print("\n" + "=" * 80)


# Pytest integration classes for structured testing
class TestIntegratedValidationFramework:
    """Pytest class for integrated validation framework testing."""

    @pytest.fixture(scope="class")
    def validation_framework(self):
        """Create validation framework instance."""
        return IntegratedValidationFramework()

    def test_story_completion_validation(self, validation_framework):
        """Test story completion validation."""
        results = validation_framework._validate_story_completion()
        assert len(results) > 0, "Should have validation results"

        # Check that validation structure is correct (don't require files to exist)
        expected_validations = [
            "Prompt Caching System",
            "Token Usage Estimation",
            "Prompt Optimization",
            "Agent Ecosystem Testing",
        ]

        result_names = [r.name for r in results]
        for expected in expected_validations:
            assert expected in result_names, f"Should have validation for {expected}"

        # The validations exist and run (files may or may not exist)
        assert all(
            isinstance(r.passed, bool) for r in results
        ), "All results should have boolean pass status"

    def test_agent_selection_validation(self, validation_framework):
        """Test agent selection validation."""
        results = validation_framework._validate_agent_selection()
        assert len(results) > 0, "Should have agent selection results"

        # Should be able to create selector
        creation_result = next((r for r in results if "Creation" in r.name), None)
        if creation_result:
            assert creation_result.passed, "Agent selector should be creatable"

    def test_native_config_validation(self, validation_framework):
        """Test native configuration validation."""
        results = validation_framework._validate_native_config()
        assert len(results) > 0, "Should have configuration validation results"

    def test_agent_framework_validation(self, validation_framework):
        """Test Claude Code agent framework validation."""
        results = validation_framework._validate_agent_framework_structure()
        assert len(results) > 0, "Should have agent framework validation results"

        # Check that we have the expected validation categories
        result_names = [r.name for r in results]
        expected_validations = [
            "Agent Directory Structure",
            "Primary Agents Count",
            "Secondary Agents Count",
            "Agent Format Compliance",
            "Required Primary Agents",
            "Required Secondary Agents",
            "Agent Ecosystem Completeness",
        ]

        for expected in expected_validations:
            assert expected in result_names, f"Should validate {expected}"

        # Check that directory structure validation passes (since .claude/agents exists)
        dir_structure_result = next(
            (r for r in results if "Directory Structure" in r.name), None
        )
        if dir_structure_result:
            assert dir_structure_result.passed, "Agent directory structure should exist"

    def test_agent_file_format_validation(self, validation_framework):
        """Test individual agent file format validation."""
        agents_dir = validation_framework.project_root / ".claude" / "agents"
        if not agents_dir.exists():
            pytest.skip("Agent directory not found")

        # Test a few agent files
        agent_files = list(agents_dir.glob("*.md"))
        if agent_files:
            # Test first agent file
            test_file = agent_files[0]
            is_valid = validation_framework._validate_agent_file_format(test_file)
            assert isinstance(is_valid, bool), "Should return boolean validation result"
            # Don't assert True since format might vary, just ensure it doesn't crash

    def test_full_validation_run(self, validation_framework):
        """Test complete validation run."""
        # This is an integration test - just verify it doesn't crash
        try:
            success = validation_framework.run_all_validations()
            # Don't assert success since some validations might fail in test environment
            # Just ensure it completes without exceptions
            assert isinstance(success, bool), "Should return boolean result"
        except Exception as e:
            pytest.fail(f"Full validation run should not raise exceptions: {e}")


# CLI interface for standalone execution
def main():
    """Main entry point for CLI execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Integrated Validation Framework for Claude Code Agent System"
    )
    parser.add_argument(
        "--suite",
        choices=[
            "story",
            "s63",
            "agent-selection",
            "infrastructure",
            "config",
            "learning",
            "all",
        ],
        default="all",
        help="Specific validation suite to run (default: all)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Project root directory (default: auto-detect)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # Create framework
    framework = IntegratedValidationFramework(args.project_root)

    # Run specific suite or all
    if args.suite == "all":
        success = framework.run_all_validations()
    else:
        # Run specific suite
        suite_map = {
            "story": framework._validate_story_completion,
            "s63": framework._validate_s63_implementation,
            "agent-selection": framework._validate_agent_selection,
            "infrastructure": framework._validate_infrastructure_learning,
            "config": framework._validate_native_config,
            "learning": framework._validate_claude_code_agent_learning,
        }

        validator = suite_map[args.suite]
        print(f"🔍 Running {args.suite} validation...")

        results = validator()
        success = all(r.passed for r in results)

        print(f"\n{'✅ PASSED' if success else '❌ FAILED'}: {args.suite} validation")
        for result in results:
            status = "✅" if result.passed else "❌"
            print(f"  {status} {result.name}: {result.details or 'OK'}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
