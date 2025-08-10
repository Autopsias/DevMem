from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import json
import numpy as np
from collections import deque
from .metrics_collector import MetricPoint, Alert, AlertThreshold, MetricsCollector

@dataclass
class AlertRule:
    metric_type: str
    warning_threshold: float
    critical_threshold: float
    comparison: str  # "above" or "below"
    duration_seconds: int
    cooldown_seconds: int  # Minimum time between repeated alerts
    correlation_metrics: List[str]  # Related metrics to check for correlation
    analysis_window: int  # Number of data points to analyze for trends

@dataclass
class AlertContext:
    metric_values: List[float]
    related_values: Dict[str, List[float]]
    correlation_scores: Dict[str, float]
    trend_score: float
    anomaly_score: float

@dataclass
class EnhancedAlert(Alert):
    context: AlertContext
    correlation_insights: List[str]
    trend_insights: List[str]
    recommended_actions: List[str]

class AlertingSystem:
    def __init__(self, metrics_collector: MetricsCollector):
        self.collector = metrics_collector
        self.alert_rules: Dict[str, AlertRule] = {}
        self.alert_history: Dict[str, List[EnhancedAlert]] = {}
        self.last_alert_time: Dict[str, datetime] = {}
        self.alert_handlers: List[Callable[[EnhancedAlert], None]] = []
        self.alert_suppression: Dict[str, datetime] = {}
        
        # Initialize default rules
        self._initialize_default_rules()
        
    def _initialize_default_rules(self) -> None:
        self.alert_rules = {
            "pattern_execution_time": AlertRule(
                metric_type="pattern_execution_time",
                warning_threshold=0.045,
                critical_threshold=0.1,
                comparison="above",
                duration_seconds=60,
                cooldown_seconds=300,
                correlation_metrics=["memory_usage_mb", "pattern_success_rate"],
                analysis_window=10
            ),
            "pattern_success_rate": AlertRule(
                metric_type="pattern_success_rate",
                warning_threshold=0.95,
                critical_threshold=0.90,
                comparison="below",
                duration_seconds=300,
                cooldown_seconds=600,
                correlation_metrics=["pattern_execution_time"],
                analysis_window=10
            ),
            "memory_usage_mb": AlertRule(
                metric_type="memory_usage_mb",
                warning_threshold=1500,
                critical_threshold=1800,
                comparison="above",
                duration_seconds=120,
                cooldown_seconds=300,
                correlation_metrics=["pattern_execution_time"],
                analysis_window=10
            )
        }
        
    def add_alert_handler(self, handler: Callable[[EnhancedAlert], None]) -> None:
        self.alert_handlers.append(handler)
        
    def check_alerts(self) -> List[EnhancedAlert]:
        new_alerts = []
        
        for metric_type, rule in self.alert_rules.items():
            if self._should_check_alert(metric_type):
                alert = self._analyze_metric(rule)
                if alert:
                    self._handle_alert(alert)
                    new_alerts.append(alert)
                    
        return new_alerts
        
    def _should_check_alert(self, metric_type: str) -> bool:
        # Check cooldown period
        if metric_type in self.last_alert_time:
            last_time = self.last_alert_time[metric_type]
            cooldown = self.alert_rules[metric_type].cooldown_seconds
            if (datetime.now() - last_time).total_seconds() < cooldown:
                return False
                
        # Check if metric is being suppressed
        if metric_type in self.alert_suppression:
            if datetime.now() < self.alert_suppression[metric_type]:
                return False
                
        return True
        
    def _analyze_metric(self, rule: AlertRule) -> Optional[EnhancedAlert]:
        recent_metrics = self.collector.get_recent_metrics(
            rule.metric_type,
            rule.duration_seconds
        )
        
        if not recent_metrics:
            return None
            
        # Get metric values and calculate baseline statistics
        values = [m.value for m in recent_metrics]
        avg_value = np.mean(values)
        
        # Check thresholds
        severity = None
        threshold = 0.0
        
        if self._threshold_exceeded(avg_value, rule.critical_threshold, rule.comparison):
            severity = "critical"
            threshold = rule.critical_threshold
        elif self._threshold_exceeded(avg_value, rule.warning_threshold, rule.comparison):
            severity = "warning"
            threshold = rule.warning_threshold
            
        if not severity:
            return None
            
        # Build alert context with correlation analysis
        context = self._build_alert_context(rule, values[-rule.analysis_window:])
        
        # Generate insights based on context
        correlation_insights = self._generate_correlation_insights(context)
        trend_insights = self._generate_trend_insights(context)
        recommended_actions = self._generate_recommendations(
            rule,
            context,
            severity
        )
        
        # Create enhanced alert
        alert = EnhancedAlert(
            metric_type=rule.metric_type,
            severity=severity,
            value=avg_value,
            threshold=threshold,
            timestamp=datetime.now(),
            message=self._generate_alert_message(
                rule,
                avg_value,
                threshold,
                severity,
                context
            ),
            context=context,
            correlation_insights=correlation_insights,
            trend_insights=trend_insights,
            recommended_actions=recommended_actions
        )
        
        # Update alert history
        if rule.metric_type not in self.alert_history:
            self.alert_history[rule.metric_type] = []
        self.alert_history[rule.metric_type].append(alert)
        
        return alert
        
    def _build_alert_context(
        self,
        rule: AlertRule,
        values: List[float]
    ) -> AlertContext:
        # Get correlated metrics
        related_values = {}
        correlation_scores = {}
        
        for metric in rule.correlation_metrics:
            recent = self.collector.get_recent_metrics(
                metric,
                rule.duration_seconds
            )
            if recent:
                metric_values = [m.value for m in recent[-rule.analysis_window:]]
                if len(metric_values) == len(values):  # Ensure equal length
                    related_values[metric] = metric_values
                    correlation = self._calculate_correlation(values, metric_values)
                    if not np.isnan(correlation):
                        correlation_scores[metric] = correlation
                    
        # Calculate trend score (-1 to 1, indicating trend direction and strength)
        trend_score = self._calculate_trend_score(values)
            
        # Calculate anomaly score based on standard deviations from mean
        anomaly_score = self._calculate_anomaly_score(values)
            
        return AlertContext(
            metric_values=values,
            related_values=related_values,
            correlation_scores=correlation_scores,
            trend_score=trend_score,
            anomaly_score=anomaly_score
        )
        
    def _calculate_correlation(self, values1: List[float], values2: List[float]) -> float:
        if len(values1) < 2 or len(values2) < 2:
            return 0.0
            
        # Remove any constant sequences
        if len(set(values1)) == 1 or len(set(values2)) == 1:
            return 0.0
            
        return np.corrcoef(values1, values2)[0, 1]
        
    def _calculate_trend_score(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
            
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        # Normalize slope to [-1, 1] range
        max_slope = max(abs(max(values) - min(values)) / len(values), 1e-10)
        return np.clip(slope / max_slope, -1, 1)
        
    def _calculate_anomaly_score(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
            
        std = np.std(values)
        if std == 0:
            return 0.0
            
        recent = values[-1]
        mean = np.mean(values[:-1]) if len(values) > 1 else values[0]
        
        return abs(recent - mean) / std
        
    def _generate_correlation_insights(self, context: AlertContext) -> List[str]:
        insights = []
        
        for metric, score in context.correlation_scores.items():
            if abs(score) > 0.7:
                direction = "positive" if score > 0 else "negative"
                insights.append(
                    f"Strong {direction} correlation with {metric} "
                    f"(correlation={score:.2f})"
                )
            elif abs(score) > 0.4:
                direction = "positive" if score > 0 else "negative"
                insights.append(
                    f"Moderate {direction} correlation with {metric} "
                    f"(correlation={score:.2f})"
                )
                
        return insights
        
    def _generate_trend_insights(self, context: AlertContext) -> List[str]:
        insights = []
        
        # Analyze trend direction and strength
        if abs(context.trend_score) > 0.7:
            direction = "increasing" if context.trend_score > 0 else "decreasing"
            insights.append(f"Strong {direction} trend detected")
        elif abs(context.trend_score) > 0.3:
            direction = "increasing" if context.trend_score > 0 else "decreasing"
            insights.append(f"Moderate {direction} trend detected")
            
        # Analyze anomaly score
        if context.anomaly_score > 3:
            insights.append(
                f"Severe anomaly detected ({context.anomaly_score:.1f} standard "
                "deviations from baseline)"
            )
        elif context.anomaly_score > 2:
            insights.append(
                f"Significant anomaly detected ({context.anomaly_score:.1f} standard "
                "deviations from baseline)"
            )
            
        return insights
        
    def _generate_recommendations(
        self,
        rule: AlertRule,
        context: AlertContext,
        severity: str
    ) -> List[str]:
        recommendations = []
        
        # Basic recommendations based on metric type
        if rule.metric_type == "pattern_execution_time":
            if context.trend_score > 0.3:
                recommendations.append(
                    "Consider optimizing pattern execution or increasing resources"
                )
            if any(abs(score) > 0.7 for score in context.correlation_scores.values()):
                recommendations.append(
                    "Investigate correlated metrics for potential root causes"
                )
                
        elif rule.metric_type == "memory_usage_mb":
            if severity == "critical":
                recommendations.append("Immediate action required to prevent OOM")
                recommendations.append("Consider scaling up resources")
            else:
                recommendations.append("Monitor memory usage trend")
                recommendations.append("Review memory-intensive operations")
                
        elif rule.metric_type == "pattern_success_rate":
            if severity == "critical":
                recommendations.append("Investigate pattern execution failures")
                recommendations.append("Check error logs for failure patterns")
            else:
                recommendations.append("Monitor pattern execution trends")
                recommendations.append("Review recent pattern changes")
                
        # Add general recommendations based on severity
        if severity == "critical":
            recommendations.append("Escalate to on-call team")
            recommendations.append("Consider immediate mitigation actions")
        else:
            recommendations.append("Monitor situation for escalation")
            
        return recommendations
        
    def _generate_alert_message(
        self,
        rule: AlertRule,
        value: float,
        threshold: float,
        severity: str,
        context: AlertContext
    ) -> str:
        message = (
            f"{severity.upper()}: {rule.metric_type} = {value:.3f} "
            f"({threshold:.3f} threshold)\n"
        )
        
        # Add trend information
        if abs(context.trend_score) > 0.3:
            direction = "increasing" if context.trend_score > 0 else "decreasing"
            message += f"Metric is {direction} "
            message += f"(trend_score={context.trend_score:.2f})\n"
            
        # Add correlation information
        strong_correlations = [
            (metric, score)
            for metric, score in context.correlation_scores.items()
            if abs(score) > 0.7
        ]
        if strong_correlations:
            message += "Strong correlations with:\n"
            for metric, score in strong_correlations:
                message += f"- {metric} (correlation={score:.2f})\n"
                
        return message.strip()
        
    def _threshold_exceeded(
        self,
        value: float,
        threshold: float,
        comparison: str
    ) -> bool:
        if comparison == "above":
            return value > threshold
        return value < threshold
        
    def _handle_alert(self, alert: EnhancedAlert) -> None:
        # Update last alert time
        self.last_alert_time[alert.metric_type] = alert.timestamp
        
        # Notify handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Error in alert handler: {e}")
                
    def suppress_alerts(
        self,
        metric_type: str,
        duration_seconds: int
    ) -> None:
        """Suppress alerts for a metric type for the specified duration"""
        self.alert_suppression[metric_type] = (
            datetime.now() + timedelta(seconds=duration_seconds)
        )
        
    def get_alert_history(
        self,
        metric_type: Optional[str] = None,
        severity: Optional[str] = None,
        duration_seconds: int = 3600
    ) -> List[EnhancedAlert]:
        """Get alert history with optional filtering"""
        cutoff = datetime.now() - timedelta(seconds=duration_seconds)
        
        alerts = []
        for m_type, history in self.alert_history.items():
            if metric_type and m_type != metric_type:
                continue
                
            alerts.extend([
                alert for alert in history
                if alert.timestamp > cutoff
                and (not severity or alert.severity == severity)
            ])
            
        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)
        
    def get_alert_stats(
        self,
        duration_seconds: int = 3600
    ) -> Dict[str, Any]:
        """Get alert statistics for analysis"""
        alerts = self.get_alert_history(duration_seconds=duration_seconds)
        
        return {
            "total_alerts": len(alerts),
            "by_severity": {
                "critical": len([a for a in alerts if a.severity == "critical"]),
                "warning": len([a for a in alerts if a.severity == "warning"])
            },
            "by_metric": {
                metric: len([a for a in alerts if a.metric_type == metric])
                for metric in self.alert_rules
            },
            "suppressed_metrics": list(self.alert_suppression.keys())
        }