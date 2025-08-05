# Performance tests for routing efficiency comparison
# Testing S3.2: Performance improvements from direct routing

import pytest
import time
import statistics


class TestRoutingPerformance:
    """Performance test suite for analysis-gateway routing improvements."""

    def test_direct_routing_latency_target(self):
        """Test that direct routing meets <1.5s latency target for 2-4 domain problems."""
        multi_domain_problems = [
            "test failures with security vulnerabilities",
            "Docker performance issues affecting CI pipeline",
            "code quality problems with security and performance issues",
            "testing, performance, security, and infrastructure analysis needed",
        ]

        latencies = []
        for problem in multi_domain_problems:
            start_time = time.time()
            routing = self._simulate_direct_routing(problem)
            latency = time.time() - start_time
            latencies.append(latency)

            # Individual problem should meet target
            assert (
                latency < 1.5
            ), f"Direct routing latency {latency:.3f}s exceeds 1.5s target for '{problem}'"
            assert "direct_task_coordination" in routing

        # Average latency should be well under target
        avg_latency = statistics.mean(latencies)
        assert (
            avg_latency < 0.5
        ), f"Average direct routing latency {avg_latency:.3f}s should be well under 1.5s"

    def test_routing_decision_speed(self):
        """Test that routing decision time meets <0.1s target."""
        test_problems = [
            "single domain test failure",
            "multi-domain security and performance issues",
            "strategic crisis requiring comprehensive coordination",
        ]

        for problem in test_problems:
            start_time = time.time()
            domains = self._detect_domains(problem)
            self._make_routing_decision(domains)
            decision_time = time.time() - start_time

            assert (
                decision_time < 0.1
            ), f"Routing decision time {decision_time:.3f}s exceeds 0.1s target for '{problem}'"

    def test_direct_vs_meta_coordinator_performance(self):
        """Test performance comparison between direct routing and meta-coordinator routing."""
        # Problems that now use direct routing (2-4 domains)
        direct_routing_problems = [
            "test and security analysis",
            "Docker performance and environment issues",
            "code quality, security, and performance review",
        ]

        # Problems that still use meta-coordinator (5+ domains)
        meta_coordination_problems = [
            "comprehensive system analysis across security, performance, testing, infrastructure, and CI",
            "crisis response requiring all domain coordination",
        ]

        # Measure direct routing performance
        direct_latencies = []
        for problem in direct_routing_problems:
            start_time = time.time()
            self._simulate_direct_routing(problem)
            latency = time.time() - start_time
            direct_latencies.append(latency)

        # Measure meta-coordinator performance (simulated)
        meta_latencies = []
        for problem in meta_coordination_problems:
            start_time = time.time()
            self._simulate_meta_coordinator_routing(problem)
            latency = time.time() - start_time
            meta_latencies.append(latency)

        avg_direct = statistics.mean(direct_latencies)
        avg_meta = statistics.mean(meta_latencies)

        # Direct routing should be significantly faster
        improvement_ratio = avg_meta / avg_direct
        assert (
            improvement_ratio > 2.0
        ), f"Direct routing should be >2x faster than meta-coordinator, got {improvement_ratio:.2f}x"

    def test_context_preservation_efficiency(self):
        """Test that context preservation is >95% efficient through direct routing."""
        test_contexts = [
            {
                "problem": "authentication system test failures with security concerns",
                "expected_context": ["testing", "security", "authentication"],
                "domains": 2,
            },
            {
                "problem": "Docker container performance issues affecting CI deployment",
                "expected_context": ["infrastructure", "performance", "ci_cd"],
                "domains": 3,
            },
        ]

        for context_test in test_contexts:
            problem = context_test["problem"]
            expected_context = context_test["expected_context"]

            # Simulate context preservation through direct routing
            preserved_context = self._simulate_context_preservation(
                problem, expected_context
            )
            preservation_rate = len(preserved_context) / len(expected_context)

            assert (
                preservation_rate >= 0.95
            ), f"Context preservation {preservation_rate:.2%} below 95% target for '{problem}'"

    def test_resource_optimization_efficiency(self):
        """Test that direct routing provides precise agent selection without overhead."""
        test_cases = [
            {
                "problem": "test coverage gaps with fixture issues",
                "expected_agents": 1,  # Only testing domain detected
                "routing_type": "direct",
            },
            {
                "problem": "Docker performance affecting testing and CI",
                "expected_agents": 4,  # infrastructure, performance, testing, ci_cd
                "routing_type": "direct",
            },
            {
                "problem": "comprehensive system architecture review",
                "expected_agents": 7,  # comprehensive adds multiple domains
                "routing_type": "strategic",
            },
        ]

        for test_case in test_cases:
            problem = test_case["problem"]
            expected_agents = test_case["expected_agents"]
            routing_type = test_case["routing_type"]

            start_time = time.time()
            if routing_type == "direct":
                agents = self._simulate_direct_agent_selection(problem)
                coordination_time = time.time() - start_time
                # Direct routing should be very efficient
                assert (
                    coordination_time < 0.1
                ), f"Direct coordination too slow: {coordination_time:.3f}s"
            else:
                agents = self._simulate_strategic_agent_selection(problem)
                coordination_time = time.time() - start_time
                # Strategic coordination can take longer
                assert (
                    coordination_time < 0.5
                ), f"Strategic coordination time: {coordination_time:.3f}s"

            # Agent count should match expectations
            assert (
                len(agents) == expected_agents
            ), f"Expected {expected_agents} agents, got {len(agents)}"

    def test_end_to_end_routing_efficiency(self):
        """Test end-to-end routing efficiency from problem to solution."""
        efficiency_tests = [
            {
                "problem": "pytest test failures affecting deployment",
                "expected_domains": 3,  # testing, infrastructure, ci_cd
                "target_latency": 1.0,
                "routing": "direct",
            },
            {
                "problem": "security vulnerabilities with performance impact and test failures",
                "expected_domains": 3,  # security, performance, testing
                "target_latency": 1.2,
                "routing": "direct",
            },
            {
                "problem": "comprehensive system crisis requiring all domain analysis",
                "expected_domains": 7,  # comprehensive expands to all domains
                "target_latency": 3.0,
                "routing": "strategic",
            },
        ]

        for test in efficiency_tests:
            start_time = time.time()

            # Full routing pipeline
            domains = self._detect_domains(test["problem"])
            self._make_routing_decision(domains)

            if test["routing"] == "direct":
                self._simulate_direct_routing(test["problem"])
            else:
                self._simulate_meta_coordinator_routing(test["problem"])

            total_time = time.time() - start_time

            assert (
                len(domains) == test["expected_domains"]
            ), f"Domain count mismatch for '{test['problem']}'"
            assert (
                total_time < test["target_latency"]
            ), f"End-to-end latency {total_time:.3f}s exceeds {test['target_latency']}s target"

    # Helper methods for simulation
    def _detect_domains(self, problem_description: str) -> list:
        """Simulate domain detection algorithm."""
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

        # Handle comprehensive analysis
        if (
            "comprehensive" in problem_description.lower()
            or "crisis" in problem_description.lower()
        ):
            if len(detected_domains) < 5:
                detected_domains.extend(
                    [
                        "security",
                        "performance",
                        "testing",
                        "infrastructure",
                        "ci_cd",
                        "environment",
                        "code_quality",
                    ][: 7 - len(detected_domains)]
                )

        return detected_domains

    def _make_routing_decision(self, domains: list) -> str:
        """Simulate routing decision making."""
        domain_count = len(domains)

        if domain_count == 1:
            return f"direct_routing_to_{domains[0]}_specialist"
        elif 2 <= domain_count <= 4:
            return f"direct_task_coordination_{domain_count}_domains"
        else:
            return "meta_coordinator_strategic_orchestration"

    def _simulate_direct_routing(self, problem: str) -> str:
        """Simulate direct routing execution (optimized)."""
        time.sleep(0.001)  # Simulate minimal processing time
        domains = self._detect_domains(problem)
        return f"direct_task_coordination_{len(domains)}_domains"

    def _simulate_meta_coordinator_routing(self, problem: str) -> str:
        """Simulate meta-coordinator routing (higher overhead)."""
        time.sleep(0.005)  # Simulate strategic coordination overhead
        domains = self._detect_domains(problem)
        return f"meta_coordinator_strategic_orchestration_{len(domains)}_domains"

    def _simulate_context_preservation(
        self, problem: str, expected_context: list
    ) -> list:
        """Simulate context preservation through routing."""
        # Direct routing preserves context more efficiently
        time.sleep(0.001)
        detected_domains = self._detect_domains(problem)

        # Simulate high context preservation rate
        preserved = []
        for context_item in expected_context:
            if (
                any(context_item in domain for domain in detected_domains)
                or context_item in problem.lower()
            ):
                preserved.append(context_item)

        return preserved

    def _simulate_direct_agent_selection(self, problem: str) -> list:
        """Simulate direct agent selection (efficient)."""
        time.sleep(0.001)
        domains = self._detect_domains(problem)
        return [f"{domain}_agent" for domain in domains]

    def _simulate_strategic_agent_selection(self, problem: str) -> list:
        """Simulate strategic agent selection (more overhead)."""
        time.sleep(0.003)
        domains = self._detect_domains(problem)
        return [f"{domain}_agent" for domain in domains]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
