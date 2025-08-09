"""
Pytest configuration and shared fixtures for agent coordination testing.

Provides common fixtures and configuration for:
- Agent coordination pattern testing
- Performance benchmarking
- Integration testing scenarios
- CI pipeline integration
"""

import pytest
import time

try:
    import psutil
except ImportError:
    # Mock psutil for testing when not available
    class MockPsutil:
        class Process:
            def memory_info(self):
                class MemInfo:
                    rss = 100 * 1024 * 1024  # 100MB mock

                return MemInfo()

        @staticmethod
        def cpu_percent():
            return 25.0  # Mock 25% CPU usage

    psutil = MockPsutil()
import json
from pathlib import Path
from typing import Dict, Any, List
import logging


# Configure logging for test runs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@pytest.fixture(scope="session")
def test_config():
    """Session-scoped test configuration."""
    return {
        "project_root": Path("/Users/ricardocarvalho/DeveloperFolder/DevMem"),
        "agents_dir": Path(
            "/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/agents"
        ),
        "memory_dir": Path(
            "/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/memory"
        ),
        "test_results_dir": Path(
            "/Users/ricardocarvalho/DeveloperFolder/DevMem/tests/results"
        ),
        "performance_thresholds": {
            "max_execution_time_ms": 5000,
            "max_memory_usage_mb": 200,
            "max_cpu_usage_percent": 80,
        },
    }


@pytest.fixture(scope="session")
def ensure_test_directories(test_config):
    """Ensure test result directories exist."""
    test_config["test_results_dir"].mkdir(exist_ok=True)
    (test_config["test_results_dir"] / "performance").mkdir(exist_ok=True)
    (test_config["test_results_dir"] / "coordination").mkdir(exist_ok=True)
    (test_config["test_results_dir"] / "integration").mkdir(exist_ok=True)
    return test_config


@pytest.fixture
def performance_monitor():
    """Performance monitoring fixture."""

    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.start_memory = None
            self.results = {}

        def start(self, test_name: str):
            """Start monitoring performance."""
            self.start_time = time.time()
            self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            self.current_test = test_name

        def stop(self) -> Dict[str, Any]:
            """Stop monitoring and return results."""
            if self.start_time is None:
                return {}

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

            results = {
                "execution_time_ms": (end_time - self.start_time) * 1000,
                "memory_delta_mb": end_memory - self.start_memory,
                "cpu_percent": psutil.cpu_percent(),
            }

            self.results[self.current_test] = results
            return results

    return PerformanceMonitor()


@pytest.fixture
def agent_validator():
    """Agent validation fixture."""

    class AgentValidator:
        def __init__(self, agents_dir: Path):
            self.agents_dir = agents_dir

        def validate_agent_exists(self, agent_name: str) -> bool:
            """Validate that an agent file exists."""
            primary_path = self.agents_dir / f"{agent_name}.md"
            secondary_path = self.agents_dir / "secondary" / f"{agent_name}.md"
            return primary_path.exists() or secondary_path.exists()

        def validate_agent_content(self, agent_name: str) -> Dict[str, Any]:
            """Validate agent content and extract metadata."""
            primary_path = self.agents_dir / f"{agent_name}.md"
            secondary_path = self.agents_dir / "secondary" / f"{agent_name}.md"

            agent_path = primary_path if primary_path.exists() else secondary_path
            if not agent_path.exists():
                return {"exists": False}

            content = agent_path.read_text()
            return {
                "exists": True,
                "path": agent_path,
                "content_length": len(content),
                "has_ultrathink": "UltraThink Analysis" in content,
                "has_epic4": "Epic 4:" in content,
                "has_coordination": "coordination" in content.lower(),
                "has_tools": any(
                    tool in content for tool in ["Read", "Edit", "Bash", "Task"]
                ),
                "is_primary": agent_path.parent.name != "secondary",
            }

        def get_all_agents(self) -> Dict[str, Dict[str, Any]]:
            """Get all agents with their validation results."""
            agents = {}

            # Primary agents
            for agent_file in self.agents_dir.glob("*.md"):
                agent_name = agent_file.stem
                agents[agent_name] = self.validate_agent_content(agent_name)

            # Secondary agents
            secondary_dir = self.agents_dir / "secondary"
            if secondary_dir.exists():
                for agent_file in secondary_dir.glob("*.md"):
                    agent_name = agent_file.stem
                    agents[agent_name] = self.validate_agent_content(agent_name)

            return agents

    return AgentValidator


@pytest.fixture
def agent_validator_instance(test_config, agent_validator):
    """Agent validator instance with test configuration."""
    return agent_validator(test_config["agents_dir"])


@pytest.fixture
def coordination_tester():
    """Coordination testing fixture."""

    class CoordinationTester:
        def __init__(self):
            self.coordination_results = {}

        def test_sequential_coordination(self, agents: List[str]) -> Dict[str, Any]:
            """Test sequential coordination pattern."""
            start_time = time.time()
            results = {
                "agents": agents,
                "coordination_type": "sequential",
                "results": [],
            }

            context = {}
            for i, agent_name in enumerate(agents):
                agent_result = {
                    "agent": agent_name,
                    "position": i + 1,
                    "context_received": len(context),
                    "processing_time": 0.01,  # Simulated processing time
                }

                # Simulate context accumulation
                context[f"step_{i}"] = {"agent": agent_name, "result": f"output_{i}"}
                agent_result["context_contributed"] = 1

                results["results"].append(agent_result)
                time.sleep(0.01)  # Simulate processing delay

            results["total_time"] = time.time() - start_time
            results["context_preserved"] = len(context) == len(agents)

            return results

        def test_parallel_coordination(self, agents: List[str]) -> Dict[str, Any]:
            """Test parallel coordination pattern."""
            import concurrent.futures

            start_time = time.time()
            results = {"agents": agents, "coordination_type": "parallel", "results": []}

            def process_agent(agent_name):
                """Simulate agent processing."""
                time.sleep(0.02)  # 20ms processing simulation
                return {
                    "agent": agent_name,
                    "processing_time": 0.02,
                    "output": f"result_{agent_name}",
                }

            # Execute agents in parallel
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(agents)
            ) as executor:
                futures = [executor.submit(process_agent, agent) for agent in agents]
                for future in concurrent.futures.as_completed(futures):
                    results["results"].append(future.result())

            results["total_time"] = time.time() - start_time
            results["parallel_efficiency"] = results["total_time"] < (
                0.02 * len(agents)
            )

            return results

        def validate_coordination_results(
            self, results: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Validate coordination test results."""
            validation = {"valid": True, "issues": []}

            if not results.get("results"):
                validation["valid"] = False
                validation["issues"].append("No coordination results")

            if results.get("total_time", 0) > 5.0:  # 5 second threshold
                validation["valid"] = False
                validation["issues"].append("Coordination took too long")

            if results.get("coordination_type") == "sequential":
                if not results.get("context_preserved", False):
                    validation["valid"] = False
                    validation["issues"].append(
                        "Context not preserved in sequential coordination"
                    )

            if results.get("coordination_type") == "parallel":
                if not results.get("parallel_efficiency", False):
                    validation["valid"] = False
                    validation["issues"].append("Parallel coordination not efficient")

            return validation

    return CoordinationTester()


@pytest.fixture
def test_reporter(ensure_test_directories):
    """Test result reporting fixture."""

    class TestReporter:
        def __init__(self, results_dir: Path):
            self.results_dir = results_dir
            self.test_session_results = {}

        def record_test_result(self, test_name: str, result: Dict[str, Any]):
            """Record a test result."""
            self.test_session_results[test_name] = {
                "timestamp": time.time(),
                "result": result,
            }

        def save_session_results(self, session_type: str = "coordination"):
            """Save session results to file."""
            results_file = self.results_dir / f"{session_type}_results.json"
            with open(results_file, "w") as f:
                json.dump(self.test_session_results, f, indent=2)

        def generate_performance_report(
            self, performance_results: Dict[str, Any]
        ) -> str:
            """Generate actionable performance insights report for agent optimization."""
            report = ["Performance Test Results", "=" * 25, ""]

            for test_name, metrics in performance_results.items():
                exec_time = metrics.get("execution_time_ms", 0)
                memory_delta = metrics.get("memory_delta_mb", 0)
                cpu_usage = metrics.get("cpu_percent", 0)

                report.extend(
                    [
                        f"Test: {test_name}",
                        f"  Execution Time: {exec_time:.2f} ms",
                        f"  Memory Delta: {memory_delta:.2f} MB",
                        f"  CPU Usage: {cpu_usage:.1f}%",
                    ]
                )

                # Add actionable insights
                if exec_time > 1000:
                    report.append(
                        f"  ⚠️  Action: Optimize {test_name} - execution time exceeds 1s"
                    )
                if memory_delta > 100:
                    report.append(
                        f"  ⚠️  Action: Review {test_name} memory usage - high memory consumption"
                    )
                if cpu_usage > 80:
                    report.append(
                        f"  ⚠️  Action: Investigate {test_name} CPU usage - high CPU load"
                    )

                report.append("")

            return "\n".join(report)

        def check_ci_environment(self) -> bool:
            """Check if running in CI environment."""
            import os

            ci_indicators = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL"]
            return any(os.getenv(indicator) for indicator in ci_indicators)

    return TestReporter(ensure_test_directories["test_results_dir"])


# Pytest hooks for CI integration
def pytest_configure(config):
    """Configure pytest for CI integration."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "coordination: mark test as coordination pattern test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance benchmark test"
    )
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection for CI optimization."""
    import os

    # If in CI environment, skip slow tests unless explicitly requested
    if os.getenv("CI") and not os.getenv("RUN_SLOW_TESTS"):
        skip_slow = pytest.mark.skip(reason="Skipping slow tests in CI")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_sessionstart(session):
    """Called after the Session object has been created."""
    print("Starting Agent Coordination Testing Session")
    print(f"Test directory: {session.config.rootdir}")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished."""
    if exitstatus == 0:
        print("✅ All agent coordination tests passed!")
    else:
        print(f"❌ Some tests failed (exit status: {exitstatus})")


# Custom pytest fixtures for specific test scenarios
@pytest.fixture(
    params=[
        "sequential_basic",
        "sequential_with_context",
        "parallel_basic",
        "parallel_with_synthesis",
        "hybrid_coordination",
    ]
)
def coordination_scenario(request):
    """Parameterized coordination scenario fixture."""
    scenarios = {
        "sequential_basic": {
            "type": "sequential",
            "agents": ["analysis-gateway", "test-specialist"],
            "expected_time": 1.0,
        },
        "sequential_with_context": {
            "type": "sequential",
            "agents": ["digdeep", "synthesis-coordinator"],
            "expected_time": 1.5,
        },
        "parallel_basic": {
            "type": "parallel",
            "agents": ["infrastructure-engineer", "security-enforcer"],
            "expected_time": 0.5,
        },
        "parallel_with_synthesis": {
            "type": "parallel",
            "agents": [
                "test-specialist",
                "infrastructure-engineer",
                "synthesis-coordinator",
            ],
            "expected_time": 0.8,
        },
        "hybrid_coordination": {
            "type": "hybrid",
            "agents": ["meta-coordinator", "analysis-gateway", "synthesis-coordinator"],
            "expected_time": 2.0,
        },
    }

    return scenarios[request.param]
