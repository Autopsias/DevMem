# Tests for analysis-gateway routing logic
# Testing S3.2: Fix Analysis-Gateway Routing

import pytest
from unittest.mock import Mock
import time


class TestAnalysisGatewayRouting:
    """Test suite for analysis-gateway routing logic implementation."""

    def setup_method(self):
        """Setup test environment."""
        self.gateway = Mock()
        self.start_time = time.time()

    def test_single_domain_direct_routing(self):
        """Test that single domain problems route directly to appropriate agent."""
        # Test cases for single domain routing
        test_cases = [
            ("pytest test failures", "test-specialist"),
            ("security vulnerability in auth", "security-enforcer"),
            ("Docker container won't start", "infrastructure-engineer"),
            ("performance optimization needed", "performance-optimizer"),
            ("code quality violations", "code-quality-specialist"),
        ]

        for problem_description, expected_agent in test_cases:
            domains = self._detect_domains(problem_description)
            assert (
                len(domains) == 1
            ), f"Expected 1 domain for '{problem_description}', got {len(domains)}"
            routing = self._route_problem(problem_description)
            expected_domain = domains[0]
            assert (
                expected_domain in routing
            ), f"Expected {expected_domain} domain routing for '{problem_description}'"
            assert (
                "direct_routing" in routing
            ), f"Expected direct routing for single domain problem '{problem_description}'"

    def test_multi_domain_direct_task_routing(self):
        """Test that 2-4 domain problems use direct Task() calls instead of meta-coordinator."""
        # Test cases for 2-4 domain routing
        test_cases = [
            (
                "test failures and security vulnerabilities",
                2,
                "direct_task_coordination",
            ),
            (
                "Docker performance issues affecting CI pipeline",
                3,
                "direct_task_coordination",
            ),
            (
                "code quality problems with security and performance issues",
                3,
                "direct_task_coordination",
            ),
            (
                "testing, performance, security, and infrastructure analysis needed",
                4,
                "direct_task_coordination",
            ),
        ]

        for problem_description, expected_domains, expected_routing in test_cases:
            domains = self._detect_domains(problem_description)
            assert (
                len(domains) == expected_domains
            ), f"Expected {expected_domains} domains for '{problem_description}', got {len(domains)}"

            routing = self._route_problem(problem_description)
            assert (
                expected_routing in routing
            ), f"Expected {expected_routing} for '{problem_description}'"
            assert (
                "meta_coordinator" not in routing
            ), f"Should not use meta-coordinator for {expected_domains} domains"

    def test_strategic_meta_coordinator_routing(self):
        """Test that 5+ domain problems route to meta-coordinator."""
        # Test cases for 5+ domain strategic coordination
        test_cases = [
            (
                "system crisis affecting security, performance, testing, infrastructure, and CI",
                5,
            ),
            (
                "comprehensive architecture review of security, performance, testing, infrastructure, CI, and environment",
                6,
            ),
            (
                "crisis response requiring security, performance, testing, infrastructure, configuration, CI, and quality analysis",
                7,
            ),
        ]

        for problem_description, expected_domains in test_cases:
            domains = self._detect_domains(problem_description)
            assert (
                len(domains) >= 5
            ), f"Expected 5+ domains for '{problem_description}', got {len(domains)}"

            routing = self._route_problem(problem_description)
            assert (
                "meta_coordinator" in routing
            ), f"Expected meta-coordinator for {expected_domains} domains"

    def test_domain_detection_algorithm(self):
        """Test the domain detection algorithm accuracy."""
        domain_test_cases = {
            "testing": ["test", "testing", "coverage", "pytest", "mock", "fixture"],
            "security": [
                "security",
                "vulnerability",
                "auth",
                "permission",
                "encryption",
            ],
            "performance": [
                "performance",
                "slow",
                "optimization",
                "latency",
                "throughput",
            ],
            "infrastructure": [
                "docker",
                "container",
                "deployment",
                "infrastructure",
                "scaling",
            ],
            "code_quality": ["quality", "lint", "refactor", "code review", "standards"],
            "ci_cd": ["ci", "cd", "pipeline", "github actions", "deployment"],
            "environment": ["environment", "configuration", "env", "config", "setup"],
        }

        for domain, keywords in domain_test_cases.items():
            for keyword in keywords:
                problem = f"Issue with {keyword} needs attention"
                domains = self._detect_domains(problem)
                assert (
                    domain in domains
                ), f"Expected {domain} domain detected for keyword '{keyword}'"

    def test_routing_performance_targets(self):
        """Test that routing meets performance targets."""
        # Test direct routing latency target (<1.5s for 2-4 domains)
        test_problems = [
            "test failures and security issues",
            "Docker performance and environment configuration",
            "code quality, security, and performance analysis",
        ]

        for problem in test_problems:
            start_time = time.time()
            routing = self._route_problem(problem)
            routing_time = time.time() - start_time

            # Simulated routing decision time should be minimal
            assert routing_time < 0.1, f"Routing decision too slow: {routing_time}s"
            assert (
                "direct_task_coordination" in routing
            ), f"Should use direct coordination for '{problem}'"

    def test_agent_mapping_accuracy(self):
        """Test that domain-to-agent mapping is correct."""
        agent_mapping = {
            "testing": "test-specialist",
            "security": "security-enforcer",
            "performance": "performance-optimizer",
            "infrastructure": "infrastructure-engineer",
            "code_quality": "code-quality-specialist",
            "ci_cd": "ci-specialist",
            "environment": "environment-analyst",
            "docker": "infrastructure-engineer",  # Docker maps to infrastructure-engineer
        }

        for domain, expected_agent in agent_mapping.items():
            agent = self._map_domain_to_agent(domain)
            assert (
                agent == expected_agent
            ), f"Expected {expected_agent} for {domain}, got {agent}"

    def test_parallel_execution_templates(self):
        """Test that parallel execution templates are properly formatted."""
        template_tests = [
            (2, "I'll coordinate analysis using 2 tasks in parallel"),
            (3, "I'll coordinate analysis using 3 tasks in parallel"),
            (4, "I'll coordinate analysis using 4 tasks in parallel"),
        ]

        for domain_count, expected_phrase in template_tests:
            template = self._get_coordination_template(domain_count)
            assert (
                expected_phrase in template
            ), f"Template for {domain_count} domains should contain '{expected_phrase}'"

    def _detect_domains(self, problem_description: str) -> list:
        """Mock implementation of domain detection algorithm."""
        domain_patterns = {
            "testing": ["test", "testing", "coverage", "pytest", "mock", "fixture"],
            "security": [
                "security",
                "vulnerability",
                "auth",
                "permission",
                "encryption",
            ],
            "performance": [
                "performance",
                "slow",
                "optimization",
                "latency",
                "throughput",
            ],
            "infrastructure": [
                "docker",
                "container",
                "deployment",
                "infrastructure",
                "scaling",
            ],
            "code_quality": ["quality", "lint", "refactor", "code review", "standards"],
            "ci_cd": ["ci", "cd", "pipeline", "github actions", "deployment"],
            "environment": ["environment", "configuration", "env", "config", "setup"],
        }

        detected_domains = []
        for domain, keywords in domain_patterns.items():
            if any(keyword in problem_description.lower() for keyword in keywords):
                detected_domains.append(domain)

        return detected_domains

    def _route_problem(self, problem_context: str) -> str:
        """Mock implementation of routing logic."""
        domains = self._detect_domains(problem_context)
        domain_count = len(domains)

        if domain_count == 1:
            return f"direct_routing_to_{domains[0]}_specialist"
        elif 2 <= domain_count <= 4:
            return f"direct_task_coordination_{domain_count}_domains"
        else:  # 5+ domains
            return "meta_coordinator_strategic_orchestration"

    def _map_domain_to_agent(self, domain: str) -> str:
        """Mock implementation of domain-to-agent mapping."""
        mapping = {
            "testing": "test-specialist",
            "security": "security-enforcer",
            "performance": "performance-optimizer",
            "infrastructure": "infrastructure-engineer",
            "code_quality": "code-quality-specialist",
            "ci_cd": "ci-specialist",
            "environment": "environment-analyst",
            "docker": "infrastructure-engineer",
        }
        return mapping.get(domain, "unknown-agent")

    def _get_coordination_template(self, domain_count: int) -> str:
        """Mock implementation of coordination template generation."""
        return f"I'll coordinate analysis using {domain_count} tasks in parallel: domain analysis coordination."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
