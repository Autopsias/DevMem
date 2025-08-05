"""
Architectural Health Monitoring and Alerting System

Provides continuous monitoring of Claude Code framework health,
architectural compliance, and performance metrics with intelligent alerting.
"""

import time
import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class AlertLevel(Enum):
    """Alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of architectural health metrics."""

    RESPONSE_TIME = "response_time"
    RESOURCE_USAGE = "resource_usage"
    SUCCESS_RATE = "success_rate"
    CONTEXT_PRESERVATION = "context_preservation"
    AGENT_COUNT = "agent_count"
    CONSTRAINT_VIOLATIONS = "constraint_violations"


@dataclass
class HealthMetric:
    """Represents a single health metric measurement."""

    metric_type: MetricType
    value: float
    timestamp: datetime
    context: Dict = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}


@dataclass
class HealthAlert:
    """Represents a health monitoring alert."""

    alert_id: str
    level: AlertLevel
    metric_type: MetricType
    message: str
    value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None


@dataclass
class HealthThresholds:
    """Health monitoring thresholds."""

    response_time_warning: float = 3.0
    response_time_critical: float = 10.0
    resource_usage_warning: float = 0.8
    resource_usage_critical: float = 0.95
    success_rate_warning: float = 0.9
    success_rate_critical: float = 0.8
    context_preservation_warning: float = 0.95
    context_preservation_critical: float = 0.9
    agent_count_warning: int = 8
    agent_count_critical: int = 10


class ArchitecturalHealthMonitor:
    """
    Monitors architectural health and generates alerts for Claude Code framework.
    """

    def __init__(self, thresholds: HealthThresholds = None):
        self.thresholds = thresholds or HealthThresholds()
        self.metrics_history: List[HealthMetric] = []
        self.active_alerts: List[HealthAlert] = []
        self.alert_history: List[HealthAlert] = []
        self.monitoring_start_time = datetime.now()

    def record_metric(
        self, metric_type: MetricType, value: float, context: Dict = None
    ):
        """Record a health metric measurement."""
        metric = HealthMetric(
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
            context=context or {},
        )

        self.metrics_history.append(metric)

        # Check for alert conditions
        self._check_alert_conditions(metric)

        # Clean up old metrics (keep last 1000)
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]

    def _check_alert_conditions(self, metric: HealthMetric):
        """Check if metric triggers any alert conditions."""
        alerts = []

        if metric.metric_type == MetricType.RESPONSE_TIME:
            if metric.value > self.thresholds.response_time_critical:
                alerts.append(
                    self._create_alert(
                        AlertLevel.CRITICAL,
                        metric,
                        self.thresholds.response_time_critical,
                        f"Response time {metric.value:.2f}s exceeds critical threshold",
                    )
                )
            elif metric.value > self.thresholds.response_time_warning:
                alerts.append(
                    self._create_alert(
                        AlertLevel.WARNING,
                        metric,
                        self.thresholds.response_time_warning,
                        f"Response time {metric.value:.2f}s exceeds warning threshold",
                    )
                )

        elif metric.metric_type == MetricType.RESOURCE_USAGE:
            if metric.value > self.thresholds.resource_usage_critical:
                alerts.append(
                    self._create_alert(
                        AlertLevel.CRITICAL,
                        metric,
                        self.thresholds.resource_usage_critical,
                        f"Resource usage {metric.value:.1%} exceeds critical threshold",
                    )
                )
            elif metric.value > self.thresholds.resource_usage_warning:
                alerts.append(
                    self._create_alert(
                        AlertLevel.WARNING,
                        metric,
                        self.thresholds.resource_usage_warning,
                        f"Resource usage {metric.value:.1%} exceeds warning threshold",
                    )
                )

        elif metric.metric_type == MetricType.SUCCESS_RATE:
            if metric.value < self.thresholds.success_rate_critical:
                alerts.append(
                    self._create_alert(
                        AlertLevel.CRITICAL,
                        metric,
                        self.thresholds.success_rate_critical,
                        f"Success rate {metric.value:.1%} below critical threshold",
                    )
                )
            elif metric.value < self.thresholds.success_rate_warning:
                alerts.append(
                    self._create_alert(
                        AlertLevel.WARNING,
                        metric,
                        self.thresholds.success_rate_warning,
                        f"Success rate {metric.value:.1%} below warning threshold",
                    )
                )

        elif metric.metric_type == MetricType.CONTEXT_PRESERVATION:
            if metric.value < self.thresholds.context_preservation_critical:
                alerts.append(
                    self._create_alert(
                        AlertLevel.CRITICAL,
                        metric,
                        self.thresholds.context_preservation_critical,
                        f"Context preservation {metric.value:.1%} below critical threshold",
                    )
                )
            elif metric.value < self.thresholds.context_preservation_warning:
                alerts.append(
                    self._create_alert(
                        AlertLevel.WARNING,
                        metric,
                        self.thresholds.context_preservation_warning,
                        f"Context preservation {metric.value:.1%} below warning threshold",
                    )
                )

        elif metric.metric_type == MetricType.AGENT_COUNT:
            if metric.value > self.thresholds.agent_count_critical:
                alerts.append(
                    self._create_alert(
                        AlertLevel.CRITICAL,
                        metric,
                        self.thresholds.agent_count_critical,
                        f"Agent count {int(metric.value)} exceeds critical limit - activating graceful degradation",
                    )
                )
            elif metric.value > self.thresholds.agent_count_warning:
                alerts.append(
                    self._create_alert(
                        AlertLevel.WARNING,
                        metric,
                        self.thresholds.agent_count_warning,
                        f"Agent count {int(metric.value)} approaching limit",
                    )
                )

        # Add new alerts
        for alert in alerts:
            self._add_alert(alert)

    def _create_alert(
        self, level: AlertLevel, metric: HealthMetric, threshold: float, message: str
    ) -> HealthAlert:
        """Create a new health alert."""
        alert_id = f"{metric.metric_type.value}_{int(time.time())}"

        return HealthAlert(
            alert_id=alert_id,
            level=level,
            metric_type=metric.metric_type,
            message=message,
            value=metric.value,
            threshold=threshold,
            timestamp=metric.timestamp,
        )

    def _add_alert(self, alert: HealthAlert):
        """Add alert to active alerts and history."""
        # Check if similar alert already exists
        existing_alert = self._find_existing_alert(alert)
        if existing_alert:
            return  # Don't duplicate similar alerts

        self.active_alerts.append(alert)
        self.alert_history.append(alert)

        # Clean up old alert history (keep last 500)
        if len(self.alert_history) > 500:
            self.alert_history = self.alert_history[-500:]

    def _find_existing_alert(self, new_alert: HealthAlert) -> Optional[HealthAlert]:
        """Find existing similar alert to avoid duplicates."""
        for alert in self.active_alerts:
            if (
                alert.metric_type == new_alert.metric_type
                and alert.level == new_alert.level
                and not alert.resolved
                and (new_alert.timestamp - alert.timestamp).seconds < 300
            ):  # 5 minutes
                return alert
        return None

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved."""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolution_time = datetime.now()
                break

    def get_health_status(self) -> Dict:
        """Get current health status summary."""
        recent_metrics = self._get_recent_metrics(minutes=5)

        status = {
            "overall_health": self._calculate_overall_health(),
            "active_alerts": len([a for a in self.active_alerts if not a.resolved]),
            "critical_alerts": len(
                [
                    a
                    for a in self.active_alerts
                    if not a.resolved and a.level == AlertLevel.CRITICAL
                ]
            ),
            "metrics_summary": {},
            "monitoring_duration": str(datetime.now() - self.monitoring_start_time),
            "last_updated": datetime.now().isoformat(),
        }

        # Add metric summaries
        for metric_type in MetricType:
            type_metrics = [m for m in recent_metrics if m.metric_type == metric_type]
            if type_metrics:
                values = [m.value for m in type_metrics]
                status["metrics_summary"][metric_type.value] = {
                    "current": values[-1] if values else None,
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                }

        return status

    def _get_recent_metrics(self, minutes: int = 5) -> List[HealthMetric]:
        """Get metrics from the last N minutes."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [m for m in self.metrics_history if m.timestamp >= cutoff_time]

    def _calculate_overall_health(self) -> str:
        """Calculate overall health status."""
        critical_alerts = [
            a
            for a in self.active_alerts
            if not a.resolved and a.level == AlertLevel.CRITICAL
        ]
        warning_alerts = [
            a
            for a in self.active_alerts
            if not a.resolved and a.level == AlertLevel.WARNING
        ]

        if critical_alerts:
            return "CRITICAL"
        elif warning_alerts:
            return "WARNING"
        else:
            return "HEALTHY"

    def generate_health_report(self) -> str:
        """Generate a comprehensive health report."""
        status = self.get_health_status()

        report = f"""
# Claude Code Framework Health Report

**Overall Health**: {status['overall_health']}
**Monitoring Duration**: {status['monitoring_duration']}
**Last Updated**: {status['last_updated']}

## Alert Summary
- **Active Alerts**: {status['active_alerts']}
- **Critical Alerts**: {status['critical_alerts']}

## Active Alerts
"""

        active_unresolved = [a for a in self.active_alerts if not a.resolved]
        if active_unresolved:
            for alert in sorted(
                active_unresolved, key=lambda x: x.timestamp, reverse=True
            ):
                report += f"- **{alert.level.value.upper()}**: {alert.message} (Threshold: {alert.threshold})\n"
        else:
            report += "No active alerts.\n"

        report += "\n## Metrics Summary\n"
        for metric_name, metrics in status["metrics_summary"].items():
            if metrics:
                report += f"- **{metric_name.replace('_', ' ').title()}**: Current: {metrics['current']:.2f}, Avg: {metrics['average']:.2f}\n"

        return report

    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file."""
        if filename is None:
            filename = f"health_metrics_{int(time.time())}.json"

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "monitoring_start_time": self.monitoring_start_time.isoformat(),
            "thresholds": {
                "response_time_warning": self.thresholds.response_time_warning,
                "response_time_critical": self.thresholds.response_time_critical,
                "resource_usage_warning": self.thresholds.resource_usage_warning,
                "resource_usage_critical": self.thresholds.resource_usage_critical,
                "success_rate_warning": self.thresholds.success_rate_warning,
                "success_rate_critical": self.thresholds.success_rate_critical,
            },
            "metrics": [
                {
                    "type": m.metric_type.value,
                    "value": m.value,
                    "timestamp": m.timestamp.isoformat(),
                    "context": m.context,
                }
                for m in self.metrics_history
            ],
            "alerts": [
                {
                    "id": a.alert_id,
                    "level": a.level.value,
                    "metric_type": a.metric_type.value,
                    "message": a.message,
                    "value": a.value,
                    "threshold": a.threshold,
                    "timestamp": a.timestamp.isoformat(),
                    "resolved": a.resolved,
                    "resolution_time": (
                        a.resolution_time.isoformat() if a.resolution_time else None
                    ),
                }
                for a in self.alert_history
            ],
        }

        with open(filename, "w") as f:
            json.dump(export_data, f, indent=2)

        return filename


# Integration functions for agent framework
def create_framework_monitor() -> ArchitecturalHealthMonitor:
    """Create a health monitor configured for the Claude Code framework."""
    # Customize thresholds for DevMem framework
    thresholds = HealthThresholds(
        response_time_warning=2.0,  # 2s warning for this framework
        response_time_critical=8.0,  # 8s critical for this framework
        resource_usage_warning=0.75,  # 75% warning
        resource_usage_critical=0.9,  # 90% critical
        success_rate_warning=0.92,  # 92% warning
        success_rate_critical=0.85,  # 85% critical
        agent_count_warning=7,  # 7 agents warning
        agent_count_critical=10,  # 10 agents critical
    )

    return ArchitecturalHealthMonitor(thresholds)


def monitor_agent_execution(
    monitor: ArchitecturalHealthMonitor,
    agent_count: int,
    execution_time: float,
    success: bool,
    context: Dict = None,
):
    """Record agent execution metrics."""
    monitor.record_metric(MetricType.AGENT_COUNT, agent_count, context)
    monitor.record_metric(MetricType.RESPONSE_TIME, execution_time, context)

    # Record success rate (1.0 for success, 0.0 for failure)
    success_rate = 1.0 if success else 0.0
    monitor.record_metric(MetricType.SUCCESS_RATE, success_rate, context)


def monitor_resource_usage(
    monitor: ArchitecturalHealthMonitor, usage_percentage: float, context: Dict = None
):
    """Record resource usage metrics."""
    monitor.record_metric(MetricType.RESOURCE_USAGE, usage_percentage, context)


def monitor_context_preservation(
    monitor: ArchitecturalHealthMonitor, preservation_score: float, context: Dict = None
):
    """Record context preservation quality metrics."""
    monitor.record_metric(MetricType.CONTEXT_PRESERVATION, preservation_score, context)


# Example usage and testing
if __name__ == "__main__":
    # Create monitor
    monitor = create_framework_monitor()

    # Simulate some metrics
    monitor_agent_execution(monitor, 3, 1.5, True, {"strategy": "direct_delegation"})
    monitor_agent_execution(
        monitor, 6, 4.2, True, {"strategy": "parallel_coordination"}
    )
    monitor_agent_execution(
        monitor, 11, 12.0, False, {"strategy": "graceful_degradation"}
    )

    monitor_resource_usage(monitor, 0.85)
    monitor_context_preservation(monitor, 0.88)

    # Generate health report
    print(monitor.generate_health_report())

    # Export metrics
    filename = monitor.export_metrics()
    print(f"Metrics exported to: {filename}")
