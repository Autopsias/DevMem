"""
Streamlined Agent Invocation System

Implements optimized agent invocation patterns for Claude Code coordination
to reduce overhead and improve execution efficiency.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

from .prompt_cache import get_cache_manager, CacheStrategy
from .token_estimation import get_token_estimator, PromptType, ModelType
from .prompt_optimization import get_prompt_optimizer, OptimizationLevel


class InvocationType(Enum):
    """Types of agent invocation patterns."""
    DIRECT = "direct"                    # Direct single agent invocation
    SEQUENTIAL = "sequential"            # Sequential coordination flow
    PARALLEL = "parallel"               # Parallel agent execution
    HIERARCHICAL = "hierarchical"       # Hierarchical coordination
    CONDITIONAL = "conditional"         # Conditional agent selection


@dataclass
class InvocationSpec:
    """Specification for agent invocation."""
    agent_type: str
    task_description: str
    context: Dict[str, Any]
    invocation_type: InvocationType
    priority: int = 1
    timeout_seconds: Optional[int] = None
    dependencies: Optional[List[str]] = None


@dataclass
class InvocationResult:
    """Result of agent invocation."""
    agent_type: str
    success: bool
    execution_time_ms: float
    token_usage: Dict[str, int]
    cached: bool
    error_message: Optional[str] = None
    result_data: Optional[Dict[str, Any]] = None


class StreamlinedInvoker:
    """
    Streamlined agent invocation system with performance optimizations.
    
    Features:
    - Cached prompt templates for common invocations
    - Optimized coordination patterns
    - Reduced overhead through streamlined protocols
    - Performance metrics and monitoring
    """
    
    def __init__(self):
        """Initialize streamlined invoker."""
        self.cache_manager = get_cache_manager()
        self.token_estimator = get_token_estimator()
        self.prompt_optimizer = get_prompt_optimizer()
        
        # Performance tracking
        self.invocation_history: List[InvocationResult] = []
        
        # Streamlined prompt templates
        self.optimized_templates = {
            InvocationType.DIRECT: "Task({agent_type}) {task_description}",
            InvocationType.SEQUENTIAL: "Sequential({agents}) → {task_description}",
            InvocationType.PARALLEL: "Parallel({agents}) || {task_description}",
            InvocationType.HIERARCHICAL: "Hierarchical({primary_agent} → {secondary_agents}) ↕ {task_description}",
            InvocationType.CONDITIONAL: "If({condition}) → Task({agent_type}) {task_description}"
        }
        
        # Agent coordination patterns for common scenarios
        self.coordination_patterns = {
            "testing_analysis": {
                "primary": "test-specialist",
                "secondary": ["async-pattern-fixer", "mock-configuration-expert"],
                "template": "Analyze testing issues: {issue_description}. Focus on {focus_areas}."
            },
            "security_review": {
                "primary": "security-enforcer", 
                "secondary": ["security-auditor", "configuration-validator"],
                "template": "Security review: {scope}. Check {security_aspects}."
            },
            "performance_optimization": {
                "primary": "performance-optimizer",
                "secondary": ["resource-optimizer", "async-pattern-fixer"],
                "template": "Optimize performance: {target_system}. Address {bottlenecks}."
            },
            "infrastructure_deployment": {
                "primary": "infrastructure-engineer",
                "secondary": ["docker-specialist", "environment-synchronizer"],
                "template": "Deploy infrastructure: {deployment_target}. Configure {requirements}."
            }
        }
        
        # Common context patterns for caching
        self.context_patterns = {
            "project_context": ["project_name", "framework", "environment"],
            "testing_context": ["test_type", "coverage_target", "framework"],
            "security_context": ["security_scope", "compliance_standards", "risk_level"],
            "performance_context": ["performance_target", "current_metrics", "constraints"]
        }
    
    def invoke_agent(self, spec: InvocationSpec) -> InvocationResult:
        """
        Invoke agent with streamlined optimization.
        
        Args:
            spec: Agent invocation specification
            
        Returns:
            Invocation result with performance metrics
        """
        start_time = time.time()
        
        try:
            # Generate optimized prompt
            prompt = self._generate_optimized_prompt(spec)
            
            # Check cache first
            cached_result = self._check_cache(prompt, spec)
            if cached_result:
                execution_time = (time.time() - start_time) * 1000
                result = InvocationResult(
                    agent_type=spec.agent_type,
                    success=True,
                    execution_time_ms=execution_time,
                    token_usage={"input": 0, "output": 0},  # No tokens used for cached result
                    cached=True,
                    result_data=cached_result
                )
                
                self.invocation_history.append(result)
                return result
            
            # Execute invocation (simulated)
            result_data = self._execute_invocation(prompt, spec)
            
            # Calculate token usage
            token_usage = self._calculate_token_usage(prompt, result_data)
            
            # Cache result for future use
            self._cache_result(prompt, spec, result_data)
            
            execution_time = (time.time() - start_time) * 1000
            
            result = InvocationResult(
                agent_type=spec.agent_type,
                success=True,
                execution_time_ms=execution_time,
                token_usage=token_usage,
                cached=False,
                result_data=result_data
            )
            
            self.invocation_history.append(result)
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            
            result = InvocationResult(
                agent_type=spec.agent_type,
                success=False,
                execution_time_ms=execution_time,
                token_usage={"input": 0, "output": 0},
                cached=False,
                error_message=str(e)
            )
            
            self.invocation_history.append(result)
            return result
    
    def invoke_coordination_pattern(self, pattern_name: str, context: Dict[str, Any]) -> List[InvocationResult]:
        """
        Invoke pre-defined coordination pattern with optimizations.
        
        Args:
            pattern_name: Name of coordination pattern
            context: Context data for the pattern
            
        Returns:
            List of invocation results
        """
        if pattern_name not in self.coordination_patterns:
            raise ValueError(f"Unknown coordination pattern: {pattern_name}")
        
        pattern = self.coordination_patterns[pattern_name]
        results = []
        
        # Invoke primary agent
        primary_spec = InvocationSpec(
            agent_type=pattern["primary"],
            task_description=pattern["template"].format(**context),
            context=context,
            invocation_type=InvocationType.DIRECT
        )
        
        primary_result = self.invoke_agent(primary_spec)
        results.append(primary_result)
        
        # Invoke secondary agents in parallel if primary succeeds
        if primary_result.success and pattern["secondary"]:
            secondary_results = self._invoke_secondary_agents(
                pattern["secondary"], context, primary_result
            )
            results.extend(secondary_results)
        
        return results
    
    def batch_invoke(self, specs: List[InvocationSpec]) -> List[InvocationResult]:
        """
        Batch invoke multiple agents with optimization.
        
        Args:
            specs: List of invocation specifications
            
        Returns:
            List of invocation results
        """
        results = []
        
        # Group by invocation type for optimization
        grouped_specs = self._group_specs_by_type(specs)
        
        # Process groups efficiently
        for invocation_type, type_specs in grouped_specs.items():
            if invocation_type == InvocationType.PARALLEL:
                # Simulate parallel execution
                type_results = self._execute_parallel_batch(type_specs)
            else:
                # Sequential execution
                type_results = [self.invoke_agent(spec) for spec in type_specs]
            
            results.extend(type_results)
        
        return results
    
    def _generate_optimized_prompt(self, spec: InvocationSpec) -> str:
        """Generate optimized prompt for agent invocation."""
        # Use streamlined template
        if spec.invocation_type in self.optimized_templates:
            base_template = self.optimized_templates[spec.invocation_type]
            
            template_vars = {
                "agent_type": spec.agent_type,
                "task_description": spec.task_description,
                "agents": spec.agent_type  # For single agent, same as agent_type
            }
            
            # Add context variables
            template_vars.update(spec.context)
            
            prompt = base_template.format(**template_vars)
        else:
            # Fallback to standard format
            prompt = f"Task({spec.agent_type}) {spec.task_description}"
        
        # Optimize the prompt
        optimized_prompt = self.prompt_optimizer.optimize_prompt(
            prompt, OptimizationLevel.STANDARD
        )
        
        return optimized_prompt
    
    def _check_cache(self, prompt: str, spec: InvocationSpec) -> Optional[Dict[str, Any]]:
        """Check if result is cached."""
        # Generate cache key context
        cache_context = {
            "agent_type": spec.agent_type,
            "invocation_type": spec.invocation_type.value,
            **spec.context
        }
        
        cached = self.cache_manager.get_cached_prompt(
            prompt, cache_context, CacheStrategy.AGENT_COORDINATION,
            {spec.agent_type}
        )
        
        if cached:
            try:
                return json.loads(cached)
            except json.JSONDecodeError:
                return {"output": cached}
        
        return None
    
    def _execute_invocation(self, prompt: str, spec: InvocationSpec) -> Dict[str, Any]:
        """Execute agent invocation (simulated)."""
        # Simulate execution time based on agent type and task complexity
        base_time = 0.1  # 100ms base
        
        complexity_multipliers = {
            "meta-coordinator": 1.5,
            "synthesis-coordinator": 1.3,
            "test-specialist": 1.2,
            "security-enforcer": 1.4,
            "infrastructure-engineer": 1.3
        }
        
        multiplier = complexity_multipliers.get(spec.agent_type, 1.0)
        execution_time = base_time * multiplier
        
        time.sleep(execution_time)
        
        # Simulate result based on task
        return {
            "agent": spec.agent_type,
            "task": spec.task_description,
            "status": "completed",
            "execution_time_ms": execution_time * 1000,
            "recommendations": [
                f"Optimized {spec.agent_type} coordination",
                f"Applied streamlined invocation for {spec.invocation_type.value}"
            ]
        }
    
    def _cache_result(self, prompt: str, spec: InvocationSpec, result: Dict[str, Any]) -> None:
        """Cache invocation result."""
        cache_context = {
            "agent_type": spec.agent_type,
            "invocation_type": spec.invocation_type.value,
            **spec.context
        }
        
        # Serialize result
        result_json = json.dumps(result, default=str)
        
        self.cache_manager.cache_prompt(
            prompt, cache_context, CacheStrategy.AGENT_COORDINATION,
            result_json, {spec.agent_type}, ttl_hours=1  # Short TTL for dynamic results
        )
    
    def _calculate_token_usage(self, prompt: str, result: Dict[str, Any]) -> Dict[str, int]:
        """Calculate token usage for invocation."""
        input_tokens = self.token_estimator.count_tokens(prompt)
        
        # Estimate output tokens based on result
        output_text = json.dumps(result, default=str)
        output_tokens = self.token_estimator.count_tokens(output_text)
        
        return {
            "input": input_tokens,
            "output": output_tokens,
            "total": input_tokens + output_tokens
        }
    
    def _invoke_secondary_agents(self, 
                                secondary_agents: List[str],
                                context: Dict[str, Any],
                                primary_result: InvocationResult) -> List[InvocationResult]:
        """Invoke secondary agents based on primary result."""
        results = []
        
        # Enhance context with primary result
        enhanced_context = context.copy()
        if primary_result.result_data:
            enhanced_context.update({
                "primary_agent_output": primary_result.result_data,
                "primary_execution_time": primary_result.execution_time_ms
            })
        
        # Invoke secondary agents
        for agent_type in secondary_agents:
            spec = InvocationSpec(
                agent_type=agent_type,
                task_description=f"Support primary analysis with {agent_type} expertise",
                context=enhanced_context,
                invocation_type=InvocationType.DIRECT
            )
            
            result = self.invoke_agent(spec)
            results.append(result)
        
        return results
    
    def _group_specs_by_type(self, specs: List[InvocationSpec]) -> Dict[InvocationType, List[InvocationSpec]]:
        """Group invocation specs by type for optimization."""
        grouped = {}
        
        for spec in specs:
            if spec.invocation_type not in grouped:
                grouped[spec.invocation_type] = []
            grouped[spec.invocation_type].append(spec)
        
        return grouped
    
    def _execute_parallel_batch(self, specs: List[InvocationSpec]) -> List[InvocationResult]:
        """Execute parallel batch with simulated concurrency."""
        # Simulate parallel execution by processing all at once
        # In real implementation, this would use actual threading/async
        
        results = []
        start_time = time.time()
        
        for spec in specs:
            result = self.invoke_agent(spec)
            results.append(result)
        
        # Adjust timing to simulate parallel execution
        max_time = max(result.execution_time_ms for result in results)
        parallel_overhead = 50  # 50ms coordination overhead
        
        adjusted_time = max_time + parallel_overhead
        
        for result in results:
            result.execution_time_ms = adjusted_time
        
        return results
    
    def get_performance_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics for recent invocations."""
        if not self.invocation_history:
            return {"error": "No invocation history available"}
        
        # Filter recent history
        cutoff_time = time.time() - (hours * 3600)
        recent_results = [
            result for result in self.invocation_history
            if (time.time() - (result.execution_time_ms / 1000)) <= cutoff_time
        ]
        
        if not recent_results:
            return {"error": "No recent invocations"}
        
        # Calculate metrics
        total_invocations = len(recent_results)
        successful_invocations = sum(1 for r in recent_results if r.success)
        cached_invocations = sum(1 for r in recent_results if r.cached)
        
        avg_execution_time = sum(r.execution_time_ms for r in recent_results) / total_invocations
        
        total_tokens = sum(
            r.token_usage.get("total", 0) for r in recent_results
        )
        
        # Group by agent type
        by_agent = {}
        for result in recent_results:
            agent = result.agent_type
            if agent not in by_agent:
                by_agent[agent] = {"count": 0, "avg_time": 0, "success_rate": 0}
            
            by_agent[agent]["count"] += 1
            by_agent[agent]["avg_time"] = (
                by_agent[agent]["avg_time"] + result.execution_time_ms
            ) / by_agent[agent]["count"]
            
            if result.success:
                by_agent[agent]["success_rate"] += 1
        
        # Calculate success rates
        for agent_data in by_agent.values():
            agent_data["success_rate"] = (agent_data["success_rate"] / agent_data["count"]) * 100
        
        return {
            "period_hours": hours,
            "summary": {
                "total_invocations": total_invocations,
                "success_rate": (successful_invocations / total_invocations) * 100,
                "cache_hit_rate": (cached_invocations / total_invocations) * 100,
                "average_execution_time_ms": round(avg_execution_time, 2),
                "total_tokens_used": total_tokens
            },
            "by_agent_type": by_agent,
            "optimization_impact": {
                "cached_invocations": cached_invocations,
                "estimated_time_saved_ms": cached_invocations * avg_execution_time * 0.8,  # 80% time savings from cache
                "estimated_token_savings": cached_invocations * (total_tokens / total_invocations)
            }
        }
    
    def export_invocation_report(self, output_file: Optional[Path] = None) -> Path:
        """Export invocation performance report."""
        metrics = self.get_performance_metrics(hours=168)  # 1 week
        
        if output_file is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = Path.home() / ".claude" / "reports" / f"invocation_report_{timestamp}.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2, default=str)
        
        return output_file


# Global invoker instance
_invoker: Optional[StreamlinedInvoker] = None


def get_streamlined_invoker() -> StreamlinedInvoker:
    """Get or create global streamlined invoker."""
    global _invoker
    if _invoker is None:
        _invoker = StreamlinedInvoker()
    return _invoker


def invoke_agent_optimized(agent_type: str, 
                         task_description: str,
                         context: Optional[Dict[str, Any]] = None,
                         invocation_type: InvocationType = InvocationType.DIRECT) -> InvocationResult:
    """
    Convenience function for optimized agent invocation.
    
    Args:
        agent_type: Type of agent to invoke
        task_description: Description of task
        context: Additional context
        invocation_type: Type of invocation
        
    Returns:
        Invocation result
    """
    invoker = get_streamlined_invoker()
    
    spec = InvocationSpec(
        agent_type=agent_type,
        task_description=task_description,
        context=context or {},
        invocation_type=invocation_type
    )
    
    return invoker.invoke_agent(spec)


def invoke_coordination_pattern(pattern_name: str, context: Dict[str, Any]) -> List[InvocationResult]:
    """
    Convenience function for coordination pattern invocation.
    
    Args:
        pattern_name: Name of coordination pattern
        context: Context for the pattern
        
    Returns:
        List of invocation results
    """
    invoker = get_streamlined_invoker()
    return invoker.invoke_coordination_pattern(pattern_name, context)