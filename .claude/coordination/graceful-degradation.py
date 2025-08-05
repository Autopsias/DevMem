"""
Graceful Degradation Implementation for Claude Code Parallel Execution

Provides intelligent resource constraint handling and coordination strategy
degradation when Claude Code architectural limits are exceeded.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple
import time


class CoordinationStrategy(Enum):
    """Available coordination strategies based on resource constraints."""

    DIRECT_DELEGATION = "direct_delegation"
    PARALLEL_COORDINATION = "parallel_coordination"
    STRATEGIC_ORCHESTRATION = "strategic_orchestration"
    GRACEFUL_DEGRADATION = "graceful_degradation"


class AgentPriority(Enum):
    """Agent priority levels for graceful degradation."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AgentRequest:
    """Represents a request for agent execution."""

    agent_type: str
    description: str
    prompt: str
    priority: AgentPriority
    domain: str
    estimated_duration: float = 2.0
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class ResourceConstraints:
    """Current resource constraints and limits."""

    max_simultaneous_agents: int = 10
    max_single_batch_agents: int = 6
    max_response_time: float = 10.0
    max_resource_usage: float = 0.95
    current_agent_count: int = 0
    current_resource_usage: float = 0.0


@dataclass
class BatchExecutionPlan:
    """Plan for batched agent execution."""

    batches: List[List[AgentRequest]]
    execution_strategy: CoordinationStrategy
    estimated_total_time: float
    degradation_applied: bool = False


class GracefulDegradationManager:
    """Manages graceful degradation of parallel execution when constraints are violated."""

    def __init__(self, constraints: ResourceConstraints = None):
        self.constraints = constraints or ResourceConstraints()
        self.performance_history: List[Dict] = []

    def assess_execution_feasibility(
        self, agent_requests: List[AgentRequest]
    ) -> Tuple[CoordinationStrategy, bool]:
        """
        Assess whether the requested agent execution is feasible within constraints.

        Returns:
            Tuple of (recommended_strategy, constraint_violation_detected)
        """
        agent_count = len(agent_requests)
        estimated_time = self._estimate_execution_time(agent_requests)

        # Check hard constraints
        constraint_violated = (
            agent_count > self.constraints.max_simultaneous_agents
            or estimated_time > self.constraints.max_response_time
            or self.constraints.current_resource_usage
            > self.constraints.max_resource_usage
        )

        # Determine strategy based on agent count and constraints
        if constraint_violated:
            return CoordinationStrategy.GRACEFUL_DEGRADATION, True
        elif agent_count <= 3:
            return CoordinationStrategy.DIRECT_DELEGATION, False
        elif agent_count <= 6:
            return CoordinationStrategy.PARALLEL_COORDINATION, False
        elif agent_count <= 10:
            return CoordinationStrategy.STRATEGIC_ORCHESTRATION, False
        else:
            return CoordinationStrategy.GRACEFUL_DEGRADATION, True

    def create_degradation_plan(
        self, agent_requests: List[AgentRequest]
    ) -> BatchExecutionPlan:
        """
        Create a batch execution plan with graceful degradation.

        Implements intelligent batching based on:
        1. Agent priorities
        2. Domain clustering
        3. Dependency ordering
        4. Resource constraints
        """
        # Sort by priority and dependencies
        prioritized_agents = self._prioritize_agents(agent_requests)

        # Create batches respecting constraints
        batches = self._create_intelligent_batches(prioritized_agents)

        # Calculate execution strategy
        strategy = self._determine_batch_strategy(batches)

        # Estimate total execution time
        estimated_time = self._estimate_batch_execution_time(batches)

        return BatchExecutionPlan(
            batches=batches,
            execution_strategy=strategy,
            estimated_total_time=estimated_time,
            degradation_applied=True,
        )

    def _prioritize_agents(
        self, agent_requests: List[AgentRequest]
    ) -> List[AgentRequest]:
        """Prioritize agents based on priority level and dependencies."""
        # Sort by priority (critical first) and then by dependencies
        priority_order = {
            AgentPriority.CRITICAL: 0,
            AgentPriority.HIGH: 1,
            AgentPriority.MEDIUM: 2,
            AgentPriority.LOW: 3,
        }

        return sorted(
            agent_requests,
            key=lambda x: (
                priority_order[x.priority],
                len(x.dependencies),  # Agents with dependencies go later
                x.estimated_duration,  # Shorter tasks first within same priority
            ),
        )

    def _create_intelligent_batches(
        self, prioritized_agents: List[AgentRequest]
    ) -> List[List[AgentRequest]]:
        """Create intelligent batches based on domain clustering and constraints."""
        batches = []
        current_batch = []
        current_batch_domains = set()

        for agent in prioritized_agents:
            # Check if adding this agent would exceed batch limits
            batch_would_exceed_limit = (
                len(current_batch) >= self.constraints.max_single_batch_agents
            )

            # Check if agent has dependency conflicts with current batch
            dependency_conflict = any(
                dep in [a.agent_type for a in current_batch]
                for dep in agent.dependencies
            )

            # Start new batch if limits exceeded or conflicts exist
            if batch_would_exceed_limit or dependency_conflict:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [agent]
                current_batch_domains = {agent.domain}
            else:
                # Add to current batch, prefer domain clustering
                current_batch.append(agent)
                current_batch_domains.add(agent.domain)

        # Add final batch
        if current_batch:
            batches.append(current_batch)

        return batches

    def _determine_batch_strategy(
        self, batches: List[List[AgentRequest]]
    ) -> CoordinationStrategy:
        """Determine the coordination strategy for batch execution."""
        total_agents = sum(len(batch) for batch in batches)
        batch_count = len(batches)

        if batch_count == 1 and total_agents <= 6:
            return CoordinationStrategy.PARALLEL_COORDINATION
        elif total_agents <= 10:
            return CoordinationStrategy.STRATEGIC_ORCHESTRATION
        else:
            return CoordinationStrategy.GRACEFUL_DEGRADATION

    def _estimate_execution_time(self, agent_requests: List[AgentRequest]) -> float:
        """Estimate execution time for agent requests."""
        if not agent_requests:
            return 0.0

        # For parallel execution, time is max of all agents
        max_duration = max(agent.estimated_duration for agent in agent_requests)

        # Add coordination overhead
        coordination_overhead = len(agent_requests) * 0.1  # 100ms per agent

        return max_duration + coordination_overhead

    def _estimate_batch_execution_time(
        self, batches: List[List[AgentRequest]]
    ) -> float:
        """Estimate total execution time for batched execution."""
        total_time = 0.0

        for batch in batches:
            batch_time = self._estimate_execution_time(batch)
            total_time += batch_time

        # Add batch transition overhead
        batch_overhead = (len(batches) - 1) * 0.5  # 500ms between batches

        return total_time + batch_overhead

    def generate_execution_language(self, plan: BatchExecutionPlan) -> str:
        """
        Generate natural language for Claude Code execution that respects constraints.

        Creates language patterns that trigger appropriate coordination while
        respecting architectural boundaries.
        """
        if plan.execution_strategy == CoordinationStrategy.DIRECT_DELEGATION:
            return self._generate_direct_delegation_language(plan.batches[0])
        elif plan.execution_strategy == CoordinationStrategy.PARALLEL_COORDINATION:
            return self._generate_parallel_coordination_language(plan.batches[0])
        elif plan.execution_strategy == CoordinationStrategy.STRATEGIC_ORCHESTRATION:
            return self._generate_strategic_orchestration_language(plan.batches)
        else:  # GRACEFUL_DEGRADATION
            return self._generate_degraded_execution_language(plan.batches)

    def _generate_direct_delegation_language(self, agents: List[AgentRequest]) -> str:
        """Generate language for direct delegation (1-3 agents)."""
        domains = list(set(agent.domain for agent in agents))
        domain_desc = " and ".join(domains)

        return f"Addressing {domain_desc} requirements through specialized analysis and direct implementation."

    def _generate_parallel_coordination_language(
        self, agents: List[AgentRequest]
    ) -> str:
        """Generate language for parallel coordination (4-6 agents)."""
        domains = list(set(agent.domain for agent in agents))
        agent_count = len(agents)

        return f"Coordinating comprehensive analysis using {agent_count} tasks in parallel across {', '.join(domains)} domains."

    def _generate_strategic_orchestration_language(
        self, batches: List[List[AgentRequest]]
    ) -> str:
        """Generate language for strategic orchestration (7-10 agents)."""
        total_agents = sum(len(batch) for batch in batches)
        domains = list(set(agent.domain for batch in batches for agent in batch))

        return f"Orchestrating strategic analysis across {len(domains)} domains using coordinated multi-batch execution with {total_agents} specialized agents."

    def _generate_degraded_execution_language(
        self, batches: List[List[AgentRequest]]
    ) -> str:
        """Generate language for graceful degradation (>10 agents)."""
        total_agents = sum(len(batch) for batch in batches)
        batch_count = len(batches)

        return f"Managing complex multi-domain analysis through {batch_count} sequential coordination phases covering {total_agents} specialized agents with intelligent resource management."

    def record_execution_performance(
        self, plan: BatchExecutionPlan, actual_time: float, success: bool
    ):
        """Record execution performance for learning."""
        self.performance_history.append(
            {
                "timestamp": time.time(),
                "strategy": plan.execution_strategy.value,
                "estimated_time": plan.estimated_total_time,
                "actual_time": actual_time,
                "success": success,
                "degradation_applied": plan.degradation_applied,
                "batch_count": len(plan.batches),
                "total_agents": sum(len(batch) for batch in plan.batches),
            }
        )

        # Keep only recent history (last 100 executions)
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]


# Example usage patterns for integration
def create_example_degradation_scenarios():
    """Example scenarios for testing graceful degradation."""

    # Scenario 1: Normal multi-domain coordination (within limits)
    normal_requests = [
        AgentRequest(
            "test-specialist",
            "Test analysis",
            "Analyze test failures",
            AgentPriority.HIGH,
            "testing",
        ),
        AgentRequest(
            "security-auditor",
            "Security scan",
            "Check vulnerabilities",
            AgentPriority.CRITICAL,
            "security",
        ),
        AgentRequest(
            "performance-optimizer",
            "Performance check",
            "Optimize performance",
            AgentPriority.MEDIUM,
            "performance",
        ),
    ]

    # Scenario 2: Resource constraint violation (needs degradation)
    excessive_requests = [
        AgentRequest(
            f"agent-{i}",
            f"Task {i}",
            f"Execute task {i}",
            AgentPriority.HIGH if i < 5 else AgentPriority.MEDIUM,
            f"domain-{i%3}",
        )
        for i in range(15)  # 15 agents > 10 limit
    ]

    manager = GracefulDegradationManager()

    # Test normal coordination
    strategy, violation = manager.assess_execution_feasibility(normal_requests)
    print(f"Normal scenario: {strategy.value}, violation: {violation}")

    # Test degradation
    strategy, violation = manager.assess_execution_feasibility(excessive_requests)
    print(f"Excessive scenario: {strategy.value}, violation: {violation}")

    if violation:
        plan = manager.create_degradation_plan(excessive_requests)
        print(
            f"Degradation plan: {len(plan.batches)} batches, {plan.estimated_total_time:.2f}s estimated"
        )
        language = manager.generate_execution_language(plan)
        print(f"Execution language: {language}")


if __name__ == "__main__":
    create_example_degradation_scenarios()
