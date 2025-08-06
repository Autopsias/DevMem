"""Configuration monitoring and adaptive optimization system."""

import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from collections import deque, defaultdict
import logging

from .adaptive import AdaptiveConfigurationManager, MetricType
from .validation import ConfigurationValidator

logger = logging.getLogger(__name__)

@dataclass
class ConfigurationHealthMetric:
    """Health metric for configuration monitoring."""
    timestamp: float
    metric_name: str
    value: float
    status: str  # "healthy", "warning", "critical"
    details: Optional[Dict[str, Any]] = None

class ConfigurationMonitor:
    """Monitors configuration health and performance impact."""
    
    def __init__(self, check_interval: float = 60.0):
        """Initialize configuration monitor."""
        self.check_interval = check_interval
        self._health_metrics: deque = deque(maxlen=1000)
        self._monitoring_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()
        self._validator = ConfigurationValidator()
        self._health_callbacks: List[Callable[[ConfigurationHealthMetric], None]] = []
        
        # Health thresholds
        self._health_thresholds = {
            "avg_response_time": {"warning": 30.0, "critical": 60.0},
            "success_rate": {"warning": 0.8, "critical": 0.6},
            "config_validation_errors": {"warning": 1, "critical": 5},
            "adaptation_rate": {"warning": 10, "critical": 20},  # adjustments per hour
            "memory_usage_mb": {"warning": 100, "critical": 500}
        }
    
    def start_monitoring(self) -> None:
        """Start configuration monitoring."""
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            logger.warning("Configuration monitoring already running")
            return
        
        self._stop_monitoring.clear()
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="ConfigurationMonitor"
        )
        self._monitoring_thread.start()
        logger.info("Started configuration monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop configuration monitoring."""
        if not self._monitoring_thread:
            return
        
        self._stop_monitoring.set()
        self._monitoring_thread.join(timeout=5.0)
        
        if self._monitoring_thread.is_alive():
            logger.warning("Configuration monitoring thread did not stop cleanly")
        else:
            logger.info("Stopped configuration monitoring")
        
        self._monitoring_thread = None
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        logger.debug("Configuration monitoring loop started")
        
        while not self._stop_monitoring.wait(self.check_interval):
            try:
                self._perform_health_check()
            except Exception as e:
                logger.error(f"Error during configuration health check: {e}")
    
    def _perform_health_check(self) -> None:
        """Perform comprehensive health check."""
        current_time = time.time()
        
        # Check various health metrics
        health_checks = [
            self._check_configuration_validity,
            self._check_performance_health,
            self._check_adaptation_health,
            self._check_system_resource_health
        ]
        
        for health_check in health_checks:
            try:
                health_check(current_time)
            except Exception as e:
                logger.error(f"Error in health check {health_check.__name__}: {e}")
    
    def _check_configuration_validity(self, timestamp: float) -> None:
        """Check current configuration validity."""
        # This would integrate with the actual configuration manager
        # For now, simulate configuration checking
        
        # Simulate some validation issues
        validation_error_count = 0  # Would come from actual validation
        
        status = "healthy"
        if validation_error_count >= self._health_thresholds["config_validation_errors"]["critical"]:
            status = "critical"
        elif validation_error_count >= self._health_thresholds["config_validation_errors"]["warning"]:
            status = "warning"
        
        metric = ConfigurationHealthMetric(
            timestamp=timestamp,
            metric_name="config_validation_errors",
            value=validation_error_count,
            status=status,
            details={"error_count": validation_error_count}
        )
        
        self._record_health_metric(metric)
    
    def _check_performance_health(self, timestamp: float) -> None:
        """Check performance-related health metrics."""
        # Simulate performance data - in real implementation, this would come from
        # the adaptive configuration manager and actual agent performance metrics
        
        # Check average response time
        simulated_avg_response_time = 15.0  # Would come from actual metrics
        
        status = "healthy"
        if simulated_avg_response_time >= self._health_thresholds["avg_response_time"]["critical"]:
            status = "critical"
        elif simulated_avg_response_time >= self._health_thresholds["avg_response_time"]["warning"]:
            status = "warning"
        
        response_time_metric = ConfigurationHealthMetric(
            timestamp=timestamp,
            metric_name="avg_response_time",
            value=simulated_avg_response_time,
            status=status,
            details={"measurement_period": "last_hour"}
        )
        
        self._record_health_metric(response_time_metric)
        
        # Check success rate
        simulated_success_rate = 0.92  # Would come from actual metrics
        
        status = "healthy"
        if simulated_success_rate <= self._health_thresholds["success_rate"]["critical"]:
            status = "critical"
        elif simulated_success_rate <= self._health_thresholds["success_rate"]["warning"]:
            status = "warning"
        
        success_rate_metric = ConfigurationHealthMetric(
            timestamp=timestamp,
            metric_name="success_rate",
            value=simulated_success_rate,
            status=status,
            details={"measurement_period": "last_hour"}
        )
        
        self._record_health_metric(success_rate_metric)
    
    def _check_adaptation_health(self, timestamp: float) -> None:
        """Check adaptive configuration health."""
        # Count adaptations in the last hour
        one_hour_ago = timestamp - 3600
        recent_adaptations = sum(
            1 for metric in self._health_metrics
            if metric.timestamp > one_hour_ago and metric.metric_name == "adaptation_applied"
        )
        
        status = "healthy"
        if recent_adaptations >= self._health_thresholds["adaptation_rate"]["critical"]:
            status = "critical"
        elif recent_adaptations >= self._health_thresholds["adaptation_rate"]["warning"]:
            status = "warning"
        
        metric = ConfigurationHealthMetric(
            timestamp=timestamp,
            metric_name="adaptation_rate",
            value=recent_adaptations,
            status=status,
            details={"period": "last_hour", "adaptations_count": recent_adaptations}
        )
        
        self._record_health_metric(metric)
    
    def _check_system_resource_health(self, timestamp: float) -> None:
        """Check system resource usage related to configuration."""
        # Simulate memory usage - in real implementation, this would measure actual usage
        simulated_memory_usage = 45.0  # MB
        
        status = "healthy"
        if simulated_memory_usage >= self._health_thresholds["memory_usage_mb"]["critical"]:
            status = "critical"
        elif simulated_memory_usage >= self._health_thresholds["memory_usage_mb"]["warning"]:
            status = "warning"
        
        metric = ConfigurationHealthMetric(
            timestamp=timestamp,
            metric_name="memory_usage_mb",
            value=simulated_memory_usage,
            status=status,
            details={"process": "configuration_system"}
        )
        
        self._record_health_metric(metric)
    
    def _record_health_metric(self, metric: ConfigurationHealthMetric) -> None:
        """Record health metric and notify callbacks."""
        self._health_metrics.append(metric)
        
        # Log critical and warning metrics
        if metric.status in ["warning", "critical"]:
            log_level = logging.WARNING if metric.status == "warning" else logging.ERROR
            logger.log(log_level, f"Configuration health {metric.status}: {metric.metric_name}={metric.value}")
        
        # Notify callbacks
        for callback in self._health_callbacks:
            try:
                callback(metric)
            except Exception as e:
                logger.error(f"Error in health callback: {e}")
    
    def register_health_callback(self, callback: Callable[[ConfigurationHealthMetric], None]) -> None:
        """Register callback for health metric notifications."""
        self._health_callbacks.append(callback)
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary."""
        current_time = time.time()
        one_hour_ago = current_time - 3600
        
        recent_metrics = [m for m in self._health_metrics if m.timestamp > one_hour_ago]
        
        # Group by metric name and status
        metrics_by_name = defaultdict(list)
        status_counts = defaultdict(int)
        
        for metric in recent_metrics:
            metrics_by_name[metric.metric_name].append(metric)
            status_counts[metric.status] += 1
        
        # Calculate latest values for each metric
        latest_metrics = {}
        for metric_name, metric_list in metrics_by_name.items():
            if metric_list:
                latest_metric = max(metric_list, key=lambda m: m.timestamp)
                latest_metrics[metric_name] = {
                    "value": latest_metric.value,
                    "status": latest_metric.status,
                    "timestamp": latest_metric.timestamp,
                    "details": latest_metric.details
                }
        
        # Overall health status
        overall_status = "healthy"
        if status_counts["critical"] > 0:
            overall_status = "critical"
        elif status_counts["warning"] > 0:
            overall_status = "warning"
        
        return {
            "overall_status": overall_status,
            "timestamp": current_time,
            "status_counts": dict(status_counts),
            "latest_metrics": latest_metrics,
            "monitoring_period": "last_hour",
            "total_metrics_recorded": len(self._health_metrics)
        }
    
    def get_health_history(self, hours: int = 24) -> List[ConfigurationHealthMetric]:
        """Get health metrics history for specified period."""
        cutoff_time = time.time() - (hours * 3600)
        
        return [
            metric for metric in self._health_metrics
            if metric.timestamp > cutoff_time
        ]
    
    def set_health_threshold(self, metric_name: str, warning: float, critical: float) -> None:
        """Set custom health thresholds for a metric."""
        self._health_thresholds[metric_name] = {
            "warning": warning,
            "critical": critical
        }
        logger.info(f"Updated health thresholds for {metric_name}: warning={warning}, critical={critical}")

class AdaptiveOptimizationEngine:
    """Engine that combines monitoring and adaptive configuration for optimization."""
    
    def __init__(self):
        """Initialize adaptive optimization engine."""
        self.monitor = ConfigurationMonitor()
        self.adaptive_manager = AdaptiveConfigurationManager()
        self._optimization_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
        # Register cross-component callbacks
        self.monitor.register_health_callback(self._on_health_metric)
        self.adaptive_manager.register_adjustment_callback(self._on_configuration_adjustment)
    
    def start_optimization(self) -> None:
        """Start the optimization engine."""
        self.monitor.start_monitoring()
        logger.info("Adaptive optimization engine started")
    
    def stop_optimization(self) -> None:
        """Stop the optimization engine."""
        self.monitor.stop_monitoring()
        logger.info("Adaptive optimization engine stopped")
    
    def _on_health_metric(self, metric: ConfigurationHealthMetric) -> None:
        """Handle health metric for optimization decisions."""
        # Convert health metrics to performance metrics for adaptive system
        if metric.metric_name == "avg_response_time":
            # Record as performance metric for all agents (aggregated)
            self.adaptive_manager.record_metric(
                agent_name="system_wide",
                metric_type=MetricType.RESPONSE_TIME,
                value=metric.value
            )
        elif metric.metric_name == "success_rate":
            self.adaptive_manager.record_metric(
                agent_name="system_wide", 
                metric_type=MetricType.SUCCESS_RATE,
                value=metric.value
            )
    
    def _on_configuration_adjustment(self, adjustment: Dict[str, Any]) -> None:
        """Handle configuration adjustment for monitoring."""
        # Record adaptation event as health metric
        current_time = time.time()
        
        adaptation_metric = ConfigurationHealthMetric(
            timestamp=current_time,
            metric_name="adaptation_applied",
            value=1.0,  # Count of adaptations
            status="healthy",
            details={
                "rule_name": adjustment.get("rule_name"),
                "affected_agents": adjustment.get("affected_agents", []),
                "adjustment_count": len(adjustment.get("adjustments", {}))
            }
        )
        
        self.monitor._record_health_metric(adaptation_metric)
        
        # Notify optimization callbacks
        for callback in self._optimization_callbacks:
            try:
                callback(adjustment)
            except Exception as e:
                logger.error(f"Error in optimization callback: {e}")
    
    def trigger_optimization_cycle(self) -> Dict[str, Any]:
        """Manually trigger an optimization cycle."""
        logger.info("Triggering manual optimization cycle")
        
        # Get current health status
        health_summary = self.monitor.get_health_summary()
        
        # Run adaptive evaluation
        adjustments = self.adaptive_manager.evaluate_and_adjust()
        
        # Get adaptation statistics
        adaptation_stats = self.adaptive_manager.get_adaptation_statistics()
        
        optimization_result = {
            "timestamp": time.time(),
            "health_status": health_summary,
            "adaptations_applied": adjustments,
            "adaptation_statistics": adaptation_stats,
            "optimization_trigger": "manual"
        }
        
        logger.info(f"Optimization cycle completed: {len(adjustments)} adjustments applied")
        return optimization_result
    
    def register_optimization_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register callback for optimization events."""
        self._optimization_callbacks.append(callback)
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get comprehensive optimization status."""
        return {
            "monitoring_active": self.monitor._monitoring_thread is not None and self.monitor._monitoring_thread.is_alive(),
            "health_summary": self.monitor.get_health_summary(),
            "adaptation_statistics": self.adaptive_manager.get_adaptation_statistics(),
            "optimization_callbacks_count": len(self._optimization_callbacks)
        }