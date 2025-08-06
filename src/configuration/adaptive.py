"""Dynamic configuration adjustment based on usage patterns."""

import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque
import statistics
import logging

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of metrics tracked for adaptive configuration."""
    RESPONSE_TIME = "response_time"
    SUCCESS_RATE = "success_rate"
    TOKEN_USAGE = "token_usage"
    PARALLEL_UTILIZATION = "parallel_utilization"
    CACHE_HIT_RATE = "cache_hit_rate"
    ESCALATION_RATE = "escalation_rate"

@dataclass
class PerformanceMetric:
    """Performance metric data point."""
    timestamp: float
    agent_name: str
    metric_type: MetricType
    value: float
    context: Optional[Dict[str, Any]] = None

@dataclass
class AdaptiveRule:
    """Rule for adaptive configuration adjustment."""
    name: str
    condition: Callable[[List[PerformanceMetric]], bool]
    adjustment: Dict[str, Any]
    min_samples: int = 10
    confidence_threshold: float = 0.8
    cooldown_period: float = 300.0  # 5 minutes
    last_applied: float = 0.0
    
class AdaptiveConfigurationManager:
    """Manages dynamic configuration adjustments based on usage patterns."""
    
    def __init__(self, max_history_size: int = 1000):
        """Initialize adaptive configuration manager."""
        self.max_history_size = max_history_size
        self._metrics_history: deque = deque(maxlen=max_history_size)
        self._agent_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._adaptive_rules: List[AdaptiveRule] = []
        self._adjustments_log: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        
        # Initialize default adaptive rules
        self._initialize_default_rules()
        
        # Configuration change callbacks
        self._adjustment_callbacks: List[Callable[[Dict[str, Any]], None]] = []
    
    def _initialize_default_rules(self) -> None:
        """Initialize default adaptive rules."""
        # Rule 1: Increase timeout for slow agents
        self._adaptive_rules.append(AdaptiveRule(
            name="increase_timeout_slow_agents",
            condition=self._condition_slow_response_time,
            adjustment={"performance.response_timeout": 1.5},  # Multiply by 1.5
            min_samples=15,
            confidence_threshold=0.7
        ))
        
        # Rule 2: Reduce parallel limit for high failure rate
        self._adaptive_rules.append(AdaptiveRule(
            name="reduce_parallel_high_failure",
            condition=self._condition_high_failure_rate,
            adjustment={"performance.parallel_execution_limit": 0.5},  # Divide by 2
            min_samples=20,
            confidence_threshold=0.8
        ))
        
        # Rule 3: Enable caching for frequently used agents
        self._adaptive_rules.append(AdaptiveRule(
            name="enable_caching_frequent_use",
            condition=self._condition_frequent_usage,
            adjustment={"performance.cache_enabled": True},
            min_samples=10,
            confidence_threshold=0.6
        ))
        
        # Rule 4: Adjust context tokens based on usage
        self._adaptive_rules.append(AdaptiveRule(
            name="adjust_context_tokens",
            condition=self._condition_context_usage_pattern,
            adjustment={"performance.max_context_tokens": "dynamic"},  # Special value
            min_samples=25,
            confidence_threshold=0.75
        ))
        
        # Rule 5: Reduce escalation threshold for stable agents
        self._adaptive_rules.append(AdaptiveRule(
            name="reduce_escalation_stable_agents",
            condition=self._condition_stable_performance,
            adjustment={"coordination.escalation_threshold": 0.8},  # Multiply by 0.8
            min_samples=30,
            confidence_threshold=0.85
        ))
    
    def record_metric(self, agent_name: str, metric_type: MetricType, value: float, 
                     context: Optional[Dict[str, Any]] = None) -> None:
        """Record a performance metric."""
        metric = PerformanceMetric(
            timestamp=time.time(),
            agent_name=agent_name,
            metric_type=metric_type,
            value=value,
            context=context
        )
        
        with self._lock:
            self._metrics_history.append(metric)
            self._agent_metrics[agent_name].append(metric)
        
        logger.debug(f"Recorded metric {metric_type.value}={value} for agent {agent_name}")
    
    def evaluate_and_adjust(self) -> List[Dict[str, Any]]:
        """Evaluate all adaptive rules and apply adjustments."""
        adjustments = []
        current_time = time.time()
        
        with self._lock:
            for rule in self._adaptive_rules:
                # Check cooldown period
                if current_time - rule.last_applied < rule.cooldown_period:
                    continue
                
                # Get relevant metrics for this rule
                relevant_metrics = list(self._metrics_history)
                
                if len(relevant_metrics) < rule.min_samples:
                    continue
                
                # Evaluate condition
                try:
                    if rule.condition(relevant_metrics):
                        # Apply adjustment
                        adjustment_result = self._apply_adjustment(rule)
                        if adjustment_result:
                            adjustments.append(adjustment_result)
                            rule.last_applied = current_time
                            
                            logger.info(f"Applied adaptive rule '{rule.name}': {adjustment_result}")
                
                except Exception as e:
                    logger.error(f"Error evaluating adaptive rule '{rule.name}': {e}")
        
        return adjustments
    
    def _apply_adjustment(self, rule: AdaptiveRule) -> Optional[Dict[str, Any]]:
        """Apply configuration adjustment from rule."""
        # Determine which agents are affected
        affected_agents = self._get_affected_agents(rule)
        
        if not affected_agents:
            return None
        
        adjustment_result = {
            "rule_name": rule.name,
            "timestamp": time.time(),
            "affected_agents": affected_agents,
            "adjustments": {}
        }
        
        for agent_name in affected_agents:
            agent_adjustments = {}
            
            for config_path, adjustment_value in rule.adjustment.items():
                if adjustment_value == "dynamic":
                    # Handle dynamic adjustments
                    dynamic_value = self._calculate_dynamic_adjustment(agent_name, config_path)
                    if dynamic_value is not None:
                        agent_adjustments[config_path] = dynamic_value
                else:
                    # Handle static adjustments (multipliers, etc.)
                    current_value = self._get_current_config_value(agent_name, config_path)
                    if current_value is not None:
                        if isinstance(adjustment_value, (int, float)) and adjustment_value != 1.0:
                            if isinstance(current_value, (int, float)):
                                new_value = current_value * adjustment_value
                                agent_adjustments[config_path] = new_value
                        else:
                            agent_adjustments[config_path] = adjustment_value
            
            if agent_adjustments:
                adjustment_result["adjustments"][agent_name] = agent_adjustments
        
        # Log the adjustment
        self._adjustments_log.append(adjustment_result)
        
        # Notify callbacks
        for callback in self._adjustment_callbacks:
            try:
                callback(adjustment_result)
            except Exception as e:
                logger.error(f"Error in adjustment callback: {e}")
        
        return adjustment_result
    
    def _get_affected_agents(self, rule: AdaptiveRule) -> List[str]:
        """Determine which agents should be affected by the rule."""
        # For now, return agents that have sufficient metrics
        agents_with_metrics = set()
        
        for metric in self._metrics_history:
            if len(self._agent_metrics[metric.agent_name]) >= rule.min_samples:
                agents_with_metrics.add(metric.agent_name)
        
        return list(agents_with_metrics)
    
    def _get_current_config_value(self, agent_name: str, config_path: str) -> Any:
        """Get current configuration value for agent."""
        # This would integrate with the configuration manager
        # For now, return placeholder values
        
        defaults = {
            "performance.response_timeout": 30.0,
            "performance.parallel_execution_limit": 3,
            "performance.max_context_tokens": 8000,
            "performance.cache_enabled": True,
            "coordination.escalation_threshold": 3
        }
        
        return defaults.get(config_path, None)
    
    def _calculate_dynamic_adjustment(self, agent_name: str, config_path: str) -> Optional[Any]:
        """Calculate dynamic adjustment value based on usage patterns."""
        agent_metrics = self._agent_metrics.get(agent_name, [])
        
        if config_path == "performance.max_context_tokens":
            # Adjust based on actual token usage patterns
            token_usage_metrics = [
                m.value for m in agent_metrics 
                if m.metric_type == MetricType.TOKEN_USAGE
            ]
            
            if token_usage_metrics and len(token_usage_metrics) >= 5:
                p95_usage = sorted(token_usage_metrics)[int(len(token_usage_metrics) * 0.95)]
                
                # Set limit to 120% of 95th percentile usage
                recommended_limit = int(p95_usage * 1.2)
                return max(recommended_limit, 1000)  # Minimum 1000 tokens
        
        return None
    
    # Condition functions for adaptive rules
    
    def _condition_slow_response_time(self, metrics: List[PerformanceMetric]) -> bool:
        """Check if response times are consistently slow."""
        response_time_metrics = [
            m for m in metrics[-50:]  # Last 50 metrics
            if m.metric_type == MetricType.RESPONSE_TIME
        ]
        
        if len(response_time_metrics) < 15:
            return False
        
        recent_times = [m.value for m in response_time_metrics[-15:]]
        avg_recent = statistics.mean(recent_times)
        
        # Consider slow if average response time > 25 seconds
        return avg_recent > 25.0
    
    def _condition_high_failure_rate(self, metrics: List[PerformanceMetric]) -> bool:
        """Check if success rate is consistently low."""
        success_rate_metrics = [
            m for m in metrics[-100:]
            if m.metric_type == MetricType.SUCCESS_RATE
        ]
        
        if len(success_rate_metrics) < 20:
            return False
        
        recent_success_rates = [m.value for m in success_rate_metrics[-20:]]
        avg_success_rate = statistics.mean(recent_success_rates)
        
        # Consider high failure if success rate < 70%
        return avg_success_rate < 0.7
    
    def _condition_frequent_usage(self, metrics: List[PerformanceMetric]) -> bool:
        """Check if agent is used frequently."""
        # Count metrics in last hour
        current_time = time.time()
        one_hour_ago = current_time - 3600
        
        recent_usage = sum(
            1 for m in metrics 
            if m.timestamp > one_hour_ago
        )
        
        # Consider frequent if more than 20 operations per hour
        return recent_usage > 20
    
    def _condition_context_usage_pattern(self, metrics: List[PerformanceMetric]) -> bool:
        """Check if context token usage has clear patterns."""
        token_usage_metrics = [
            m for m in metrics[-100:]
            if m.metric_type == MetricType.TOKEN_USAGE
        ]
        
        if len(token_usage_metrics) < 25:
            return False
        
        # Check if there's significant variance in usage
        token_values = [m.value for m in token_usage_metrics]
        if not token_values:
            return False
        
        std_dev = statistics.stdev(token_values)
        mean_usage = statistics.mean(token_values)
        
        # Adjust if coefficient of variation is low (consistent usage pattern)
        coefficient_of_variation = std_dev / mean_usage if mean_usage > 0 else 1
        return coefficient_of_variation < 0.3
    
    def _condition_stable_performance(self, metrics: List[PerformanceMetric]) -> bool:
        """Check if agent performance is stable."""
        success_rate_metrics = [
            m for m in metrics[-100:]
            if m.metric_type == MetricType.SUCCESS_RATE
        ]
        
        if len(success_rate_metrics) < 30:
            return False
        
        recent_success_rates = [m.value for m in success_rate_metrics[-30:]]
        avg_success = statistics.mean(recent_success_rates)
        
        # Consider stable if average success rate > 90%
        return avg_success > 0.9
    
    def add_adaptive_rule(self, rule: AdaptiveRule) -> None:
        """Add custom adaptive rule."""
        with self._lock:
            self._adaptive_rules.append(rule)
        logger.info(f"Added adaptive rule: {rule.name}")
    
    def remove_adaptive_rule(self, rule_name: str) -> bool:
        """Remove adaptive rule by name."""
        with self._lock:
            original_count = len(self._adaptive_rules)
            self._adaptive_rules = [r for r in self._adaptive_rules if r.name != rule_name]
            removed = len(self._adaptive_rules) < original_count
        
        if removed:
            logger.info(f"Removed adaptive rule: {rule_name}")
        
        return removed
    
    def register_adjustment_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register callback to be notified of configuration adjustments."""
        self._adjustment_callbacks.append(callback)
    
    def get_adaptation_statistics(self) -> Dict[str, Any]:
        """Get statistics about adaptive behavior."""
        with self._lock:
            total_metrics = len(self._metrics_history)
            agent_metric_counts = {
                agent: len(metrics) for agent, metrics in self._agent_metrics.items()
            }
            
            rule_stats = []
            for rule in self._adaptive_rules:
                rule_stats.append({
                    "name": rule.name,
                    "last_applied": rule.last_applied,
                    "applications_count": sum(
                        1 for adj in self._adjustments_log
                        if adj["rule_name"] == rule.name
                    )
                })
        
        return {
            "total_metrics_recorded": total_metrics,
            "agent_metric_counts": agent_metric_counts,
            "active_rules_count": len(self._adaptive_rules),
            "rule_statistics": rule_stats,
            "total_adjustments": len(self._adjustments_log),
            "last_evaluation": time.time()
        }
    
    def get_adjustments_history(self) -> List[Dict[str, Any]]:
        """Get history of all configuration adjustments."""
        return self._adjustments_log.copy()