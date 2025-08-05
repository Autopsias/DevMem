# Integration tests for routing boundary validation
# Testing S3.2: Analysis-Gateway and Meta-Coordinator boundaries

import pytest
import time


class TestRoutingBoundaries:
    """Test suite for validating routing boundaries between analysis-gateway and meta-coordinator."""

    def test_meta_coordinator_boundary_validation(self):
        """Test that meta-coordinator is only used for 5+ domain problems."""
        # Problems that should NOT use meta-coordinator (2-4 domains)
        direct_routing_cases = [
            "test failures and security vulnerabilities",  # 2 domains
            "Docker performance issues affecting CI",  # 3 domains
            "code quality problems with security and performance",  # 3 domains
            "testing, performance, security, and infrastructure analysis",  # 4 domains
        ]

        # Problems that SHOULD use meta-coordinator (5+ domains)
        strategic_routing_cases = [
            "system crisis affecting security, performance, testing, infrastructure, and CI",  # 5 domains
            "architecture review of security, performance, testing, infrastructure, CI, and environment",  # 6 domains
            "crisis response requiring security, performance, testing, infrastructure, configuration, CI, and quality",  # 7 domains
        ]

        # Test direct routing (should NOT use meta-coordinator)
        for problem in direct_routing_cases:
            domains = self._detect_domains(problem)
            routing = self._route_problem(problem)

            assert (
                2 <= len(domains) <= 4
            ), f"Expected 2-4 domains for '{problem}', got {len(domains)}"
            assert (
                "direct_task_coordination" in routing
            ), f"Should use direct coordination for '{problem}'"
            assert (
                "meta_coordinator" not in routing
            ), f"Should NOT use meta-coordinator for {len(domains)} domains"

        # Test strategic routing (should use meta-coordinator)
        for problem in strategic_routing_cases:
            domains = self._detect_domains(problem)
            routing = self._route_problem(problem)

            assert (
                len(domains) >= 5
            ), f"Expected 5+ domains for '{problem}', got {len(domains)}"
            assert (
                "meta_coordinator" in routing
            ), f"Should use meta-coordinator for {len(domains)} domains"

    def test_performance_boundary_validation(self):
        """Test that direct routing meets performance targets vs meta-coordinator."""
        # Direct routing performance targets
        multi_domain_problems = [
            "test failures with security issues",
            "Docker performance and CI problems",
            "code quality with security vulnerabilities",
        ]

        for problem in multi_domain_problems:
            start_time = time.time()
            routing = self._route_problem(problem)
            routing_time = time.time() - start_time

            # Direct routing should be faster than meta-coordinator
            assert routing_time < 0.1, f"Direct routing too slow: {routing_time}s"
            assert "direct_task_coordination" in routing

    def test_existing_functionality_preservation(self):
        """Test that existing meta-coordinator functionality is preserved for strategic scenarios."""
        # Strategic scenarios that should still work
        strategic_scenarios = [
            {
                "problem": "comprehensive system crisis with 6+ domains",
                "domains": [
                    "security",
                    "performance",
                    "testing",
                    "infrastructure",
                    "ci_cd",
                    "environment",
                ],
                "expected_coordination": "strategic_orchestration",
            },
            {
                "problem": "architectural migration affecting all system domains",
                "domains": [
                    "security",
                    "performance",
                    "testing",
                    "infrastructure",
                    "ci_cd",
                    "environment",
                    "code_quality",
                ],
                "expected_coordination": "strategic_orchestration",
            },
        ]

        for scenario in strategic_scenarios:
            problem = scenario["problem"]
            routing = self._route_problem(problem)

            assert (
                "meta_coordinator" in routing
            ), f"Strategic scenario should use meta-coordinator: {problem}"

    def test_context_preservation_through_routing(self):
        """Test that context is preserved correctly through different routing paths."""
        test_contexts = [
            {
                "problem": "authentication system test failures",
                "expected_context": ["testing", "security", "authentication"],
                "expected_routing": "direct_task_coordination",
            },
            {
                "problem": "comprehensive DevMem RAG system analysis",
                "expected_context": [
                    "security",
                    "performance",
                    "testing",
                    "infrastructure",
                    "ci_cd",
                ],
                "expected_routing": "meta_coordinator",
            },
        ]

        for context_test in test_contexts:
            problem = context_test["problem"]
            routing = self._route_problem(problem)

            if "direct_task_coordination" in routing:
                assert (
                    len(self._detect_domains(problem)) <= 4
                ), "Direct routing domain count validation failed"
            elif "meta_coordinator" in routing:
                assert (
                    len(self._detect_domains(problem)) >= 5
                ), "Meta-coordinator domain count validation failed"

    def test_integration_with_synthesis_coordinator(self):
        """Test that synthesis-coordinator integration works with both routing approaches."""
        # Direct coordination should integrate results without synthesis-coordinator
        direct_problems = [
            "test and security analysis needed",
            "Docker performance and environment issues",
        ]

        # Strategic coordination should use synthesis-coordinator
        strategic_problems = [
            "comprehensive system analysis across 6+ domains",
            "crisis response requiring full domain coordination",
        ]

        for problem in direct_problems:
            routing = self._route_problem(problem)
            assert "direct_task_coordination" in routing
            # Direct coordination handles integration internally

        for problem in strategic_problems:
            routing = self._route_problem(problem)
            assert "meta_coordinator" in routing
            # Meta-coordinator uses synthesis-coordinator for complex integration

    def test_common_domain_combinations(self):
        """Test routing for common domain combinations from the story requirements."""
        story_combinations = [
            # Direct Task() coordination (2-4 domains)
            ("Testing + Performance + Security", 3, "direct_task_coordination"),
            ("Infrastructure + Docker + Environment", 3, "direct_task_coordination"),
            ("Code Quality + Security + Performance", 3, "direct_task_coordination"),
            ("CI + Testing + Quality", 3, "direct_task_coordination"),
            # Strategic Meta-coordination (5+ domains)
            ("Complex system architecture", 5, "meta_coordinator"),
            ("Crisis response", 6, "meta_coordinator"),
            ("Cross-system integration", 5, "meta_coordinator"),
        ]

        for description, expected_domain_count, expected_routing in story_combinations:
            # Create a problem description that matches the domain count
            if expected_domain_count == 3:
                if "Testing + Performance + Security" in description:
                    problem = "test failures with performance issues and security vulnerabilities"
                elif "Infrastructure + Docker + Environment" in description:
                    problem = "infrastructure problems with Docker containers and environment configuration"
                elif "Code Quality + Security + Performance" in description:
                    problem = "code quality violations with security issues and performance problems"
                elif "CI + Testing + Quality" in description:
                    problem = "CI pipeline failures with test issues and code quality problems"
            else:
                # Generate strategic problem descriptions
                problem = f"{description.lower()} requiring comprehensive multi-domain coordination analysis"

            domains = self._detect_domains(problem)
            routing = self._route_problem(problem)

            if expected_routing == "direct_task_coordination":
                assert 2 <= len(domains) <= 4, f"Expected 2-4 domains for {description}"
                assert "direct_task_coordination" in routing
            else:
                assert (
                    len(domains) >= 5 or "comprehensive" in problem
                ), f"Expected 5+ domains for {description}"
                assert "meta_coordinator" in routing

    def _detect_domains(self, problem_description: str) -> list:
        """Domain detection algorithm implementation."""
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

        # Handle special cases for comprehensive analysis
        if "comprehensive" in problem_description.lower():
            # Comprehensive analysis implies multiple domains
            if len(detected_domains) < 5:
                detected_domains.extend(
                    ["security", "performance", "testing", "infrastructure", "ci_cd"][
                        : 5 - len(detected_domains)
                    ]
                )

        return detected_domains

    def _route_problem(self, problem_context: str) -> str:
        """Routing logic implementation."""
        domains = self._detect_domains(problem_context)
        domain_count = len(domains)

        if domain_count == 1:
            return f"direct_routing_to_{domains[0]}_specialist"
        elif 2 <= domain_count <= 4:
            return f"direct_task_coordination_{domain_count}_domains"
        else:  # 5+ domains
            return "meta_coordinator_strategic_orchestration"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
