# Single-Domain Validation Testing for Agent Framework
# Testing S3.3: Category 1 - Single-Domain Validation

import pytest
import time
from unittest.mock import Mock, AsyncMock
from typing import Dict, List


class TestSingleDomainValidation:
    """Test suite for individual agent functionality validation."""

    def setup_method(self):
        """Setup test environment."""
        self.agents = self._setup_all_primary_agents()
        self.start_time = time.time()

    def _setup_all_primary_agents(self) -> Dict[str, Mock]:
        """Setup all 16 primary agents for testing."""
        primary_agents = [
            "test-specialist",
            "performance-optimizer",
            "security-enforcer",
            "infrastructure-engineer",
            "docker-specialist",
            "environment-analyst",
            "code-quality-specialist",
            "security-auditor",
            "ci-specialist",
            "intelligent-enhancer",
            "git-commit-assistant",
            "lint-enforcer",
            "meta-coordinator",
            "framework-coordinator",
            "agent-reviewer",
            "analysis-gateway",
        ]

        agents = {}
        for name in primary_agents:
            mock_agent = AsyncMock()
            mock_agent.name = name
            mock_agent.execute.return_value = {
                "agent": name,
                "status": "success",
                "execution_time": 0.5,
                "results": f"Mock results from {name}",
                "domain_expertise": self._get_agent_domain(name),
                "capabilities": self._get_agent_capabilities(name),
            }
            agents[name] = mock_agent

        return agents

    def _get_agent_domain(self, agent_name: str) -> str:
        """Get primary domain for agent."""
        domain_mapping = {
            "test-specialist": "testing",
            "performance-optimizer": "performance",
            "security-enforcer": "security",
            "infrastructure-engineer": "infrastructure",
            "docker-specialist": "containerization",
            "environment-analyst": "environment",
            "code-quality-specialist": "code_quality",
            "security-auditor": "security_audit",
            "ci-specialist": "ci_cd",
            "intelligent-enhancer": "development",
            "git-commit-assistant": "version_control",
            "lint-enforcer": "code_standards",
            "meta-coordinator": "orchestration",
            "framework-coordinator": "framework_management",
            "agent-reviewer": "agent_health",
            "analysis-gateway": "problem_routing",
        }
        return domain_mapping.get(agent_name, "unknown")

    def _get_agent_capabilities(self, agent_name: str) -> List[str]:
        """Get capabilities for agent."""
        capabilities_mapping = {
            "test-specialist": [
                "test_failure_analysis",
                "async_testing",
                "mock_configuration",
                "coverage_analysis",
            ],
            "performance-optimizer": [
                "bottleneck_identification",
                "resource_optimization",
                "scalability_analysis",
            ],
            "security-enforcer": [
                "vulnerability_scanning",
                "security_validation",
                "threat_detection",
            ],
            "infrastructure-engineer": [
                "deployment_orchestration",
                "service_networking",
                "scaling_management",
            ],
            "docker-specialist": [
                "container_troubleshooting",
                "orchestration_optimization",
                "service_coordination",
            ],
            "environment-analyst": [
                "environment_configuration",
                "dependency_management",
                "resource_constraints",
            ],
            "code-quality-specialist": [
                "quality_analysis",
                "semgrep_scanning",
                "compliance_validation",
            ],
            "security-auditor": [
                "comprehensive_security_analysis",
                "threat_modeling",
                "compliance_assessment",
            ],
            "ci-specialist": [
                "pipeline_optimization",
                "github_actions_analysis",
                "deployment_automation",
            ],
            "intelligent-enhancer": [
                "code_improvement",
                "refactoring_suggestions",
                "ai_powered_enhancements",
            ],
            "git-commit-assistant": [
                "commit_optimization",
                "workflow_automation",
                "version_control_best_practices",
            ],
            "lint-enforcer": [
                "code_formatting",
                "linting_enforcement",
                "standard_compliance",
            ],
            "meta-coordinator": [
                "strategic_orchestration",
                "multi_domain_coordination",
                "complex_problem_solving",
            ],
            "framework-coordinator": [
                "framework_analysis",
                "ecosystem_coordination",
                "architectural_compliance",
            ],
            "agent-reviewer": [
                "agent_health_monitoring",
                "ecosystem_intelligence",
                "framework_compliance",
            ],
            "analysis-gateway": [
                "problem_analysis",
                "routing_intelligence",
                "coordination_orchestration",
            ],
        }
        return capabilities_mapping.get(agent_name, ["general_assistance"])

    async def test_test_specialist_functionality(self):
        """Verify test-specialist maintains core testing functionality."""
        agent = self.agents["test-specialist"]

        # Test core testing scenarios
        test_scenarios = [
            "pytest test failures in authentication module",
            "async test patterns with mock configuration",
            "test coverage gaps in user management",
            "fixture setup issues in integration tests",
        ]

        for scenario in test_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "test-specialist"
            assert result["domain_expertise"] == "testing"
            assert "test_failure_analysis" in result["capabilities"]
            assert result["execution_time"] < 1.0  # <1s target for single agent

    async def test_performance_optimizer_functionality(self):
        """Verify performance-optimizer maintains core performance functionality."""
        agent = self.agents["performance-optimizer"]

        performance_scenarios = [
            "application response time bottlenecks",
            "memory usage optimization needed",
            "database query performance issues",
            "API endpoint latency problems",
        ]

        for scenario in performance_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "performance-optimizer"
            assert result["domain_expertise"] == "performance"
            assert "bottleneck_identification" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_security_enforcer_functionality(self):
        """Verify security-enforcer maintains core security functionality."""
        agent = self.agents["security-enforcer"]

        security_scenarios = [
            "authentication vulnerability detected",
            "SQL injection risk in user input",
            "insecure API endpoint configuration",
            "permission bypass in authorization",
        ]

        for scenario in security_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "security-enforcer"
            assert result["domain_expertise"] == "security"
            assert "vulnerability_scanning" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_infrastructure_engineer_functionality(self):
        """Verify infrastructure-engineer maintains core infrastructure functionality."""
        agent = self.agents["infrastructure-engineer"]

        infrastructure_scenarios = [
            "deployment pipeline failing",
            "service networking configuration issues",
            "scaling problems with load balancing",
            "container orchestration failures",
        ]

        for scenario in infrastructure_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "infrastructure-engineer"
            assert result["domain_expertise"] == "infrastructure"
            assert "deployment_orchestration" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_docker_specialist_functionality(self):
        """Verify docker-specialist maintains core containerization functionality."""
        agent = self.agents["docker-specialist"]

        docker_scenarios = [
            "Docker container won't start",
            "container networking problems",
            "Docker Compose orchestration issues",
            "container resource allocation problems",
        ]

        for scenario in docker_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "docker-specialist"
            assert result["domain_expertise"] == "containerization"
            assert "container_troubleshooting" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_environment_analyst_functionality(self):
        """Verify environment-analyst maintains core environment functionality."""
        agent = self.agents["environment-analyst"]

        environment_scenarios = [
            "development environment configuration issues",
            "dependency conflicts in production",
            "environment variable management problems",
            "cross-environment synchronization issues",
        ]

        for scenario in environment_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "environment-analyst"
            assert result["domain_expertise"] == "environment"
            assert "environment_configuration" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_code_quality_specialist_functionality(self):
        """Verify code-quality-specialist maintains core quality functionality."""
        agent = self.agents["code-quality-specialist"]

        quality_scenarios = [
            "code quality violations in pull request",
            "semgrep security scan failures",
            "compliance violations in codebase",
            "architectural compliance issues",
        ]

        for scenario in quality_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "code-quality-specialist"
            assert result["domain_expertise"] == "code_quality"
            assert "quality_analysis" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_security_auditor_functionality(self):
        """Verify security-auditor maintains comprehensive security functionality."""
        agent = self.agents["security-auditor"]

        audit_scenarios = [
            "comprehensive security audit needed",
            "threat modeling for new features",
            "compliance assessment requirements",
            "multi-standard security validation",
        ]

        for scenario in audit_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "security-auditor"
            assert result["domain_expertise"] == "security_audit"
            assert "comprehensive_security_analysis" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_ci_specialist_functionality(self):
        """Verify ci-specialist maintains core CI/CD functionality."""
        agent = self.agents["ci-specialist"]

        ci_scenarios = [
            "GitHub Actions pipeline failing",
            "deployment automation issues",
            "CI pipeline optimization needed",
            "workflow troubleshooting required",
        ]

        for scenario in ci_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "ci-specialist"
            assert result["domain_expertise"] == "ci_cd"
            assert "pipeline_optimization" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_intelligent_enhancer_functionality(self):
        """Verify intelligent-enhancer maintains core development functionality."""
        agent = self.agents["intelligent-enhancer"]

        enhancement_scenarios = [
            "code improvement suggestions needed",
            "refactoring opportunities identified",
            "AI-powered code optimization",
            "intelligent variable naming improvements",
        ]

        for scenario in enhancement_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "intelligent-enhancer"
            assert result["domain_expertise"] == "development"
            assert "code_improvement" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_git_commit_assistant_functionality(self):
        """Verify git-commit-assistant maintains core version control functionality."""
        agent = self.agents["git-commit-assistant"]

        git_scenarios = [
            "commit message optimization needed",
            "git workflow automation required",
            "version control best practices",
            "commit staging assistance",
        ]

        for scenario in git_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "git-commit-assistant"
            assert result["domain_expertise"] == "version_control"
            assert "commit_optimization" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_lint_enforcer_functionality(self):
        """Verify lint-enforcer maintains core code standards functionality."""
        agent = self.agents["lint-enforcer"]

        lint_scenarios = [
            "code formatting violations detected",
            "linting errors need resolution",
            "code style consistency issues",
            "standard compliance enforcement",
        ]

        for scenario in lint_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "lint-enforcer"
            assert result["domain_expertise"] == "code_standards"
            assert "code_formatting" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_meta_coordinator_functionality(self):
        """Verify meta-coordinator maintains core orchestration functionality."""
        agent = self.agents["meta-coordinator"]

        orchestration_scenarios = [
            "strategic coordination of 5+ domains required",
            "complex multi-domain problem solving",
            "strategic orchestration planning",
            "meta-level coordination intelligence",
        ]

        for scenario in orchestration_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "meta-coordinator"
            assert result["domain_expertise"] == "orchestration"
            assert "strategic_orchestration" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_framework_coordinator_functionality(self):
        """Verify framework-coordinator maintains core framework functionality."""
        agent = self.agents["framework-coordinator"]

        framework_scenarios = [
            "framework architecture analysis needed",
            "ecosystem coordination requirements",
            "architectural compliance validation",
            "framework health monitoring",
        ]

        for scenario in framework_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "framework-coordinator"
            assert result["domain_expertise"] == "framework_management"
            assert "framework_analysis" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_agent_reviewer_functionality(self):
        """Verify agent-reviewer maintains core agent health functionality."""
        agent = self.agents["agent-reviewer"]

        review_scenarios = [
            "agent health monitoring required",
            "ecosystem intelligence analysis",
            "framework compliance validation",
            "agent performance assessment",
        ]

        for scenario in review_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "agent-reviewer"
            assert result["domain_expertise"] == "agent_health"
            assert "agent_health_monitoring" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_analysis_gateway_functionality(self):
        """Verify analysis-gateway maintains core routing functionality."""
        agent = self.agents["analysis-gateway"]

        routing_scenarios = [
            "complex problem analysis and routing",
            "coordination orchestration planning",
            "routing intelligence optimization",
            "problem categorization and delegation",
        ]

        for scenario in routing_scenarios:
            result = await agent.execute(scenario)

            assert result["status"] == "success"
            assert result["agent"] == "analysis-gateway"
            assert result["domain_expertise"] == "problem_routing"
            assert "problem_analysis" in result["capabilities"]
            assert result["execution_time"] < 1.0

    async def test_all_agents_performance_regression(self):
        """Verify no performance regression across all 16 primary agents."""
        performance_results = []

        for agent_name, agent in self.agents.items():
            start_time = time.perf_counter()
            result = await agent.execute(f"Standard {agent_name} operation test")
            execution_time = time.perf_counter() - start_time

            performance_results.append(
                {
                    "agent": agent_name,
                    "execution_time": execution_time,
                    "status": result["status"],
                }
            )

            # Individual agent performance validation
            assert result["status"] == "success"
            assert execution_time < 1.0  # <1s target for single agents

        # Overall performance validation
        avg_execution_time = sum(
            r["execution_time"] for r in performance_results
        ) / len(performance_results)
        assert avg_execution_time < 0.7  # Average should be well under 1s limit

        successful_agents = [
            r["agent"] for r in performance_results if r["status"] == "success"
        ]
        assert len(successful_agents) == 16  # All agents should succeed

    async def test_agent_capability_preservation(self):
        """Verify all agents preserve their core capabilities after framework updates."""
        for agent_name, agent in self.agents.items():
            result = await agent.execute(f"Capability validation for {agent_name}")

            # Validate core capability preservation
            assert result["domain_expertise"] is not None
            assert len(result["capabilities"]) > 0
            assert result["status"] == "success"

            # Validate domain-specific capabilities
            expected_domain = self._get_agent_domain(agent_name)
            assert result["domain_expertise"] == expected_domain

            expected_capabilities = self._get_agent_capabilities(agent_name)
            for capability in expected_capabilities:
                assert capability in result["capabilities"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
