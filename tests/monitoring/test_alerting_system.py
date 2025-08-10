import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List
import numpy as np

from src.monitoring.metrics_collector import MetricsCollector
from src.monitoring.alerting_system import AlertingSystem, EnhancedAlert

class TestAlertingSystem:
    @pytest.fixture
    def metrics_collector(self) -> MetricsCollector:
        return MetricsCollector()
    
    @pytest.fixture
    def alerting_system(self, metrics_collector: MetricsCollector) -> AlertingSystem:
        return AlertingSystem(metrics_collector)
    
    def test_basic_alerting(self, alerting_system: AlertingSystem, metrics_collector: MetricsCollector):
        # Generate metrics that should trigger alerts
        for i in range(10):
            metrics_collector.collect_metric("pattern_execution_time", 0.15 + i * 0.01)  # Increasing trend
            metrics_collector.collect_metric("memory_usage_mb", 2000 + i * 100)        # Correlated increase
            
        # Check alerts
        alerts = alerting_system.check_alerts()
        
        # Verify critical alerts generated
        critical_alerts = [a for a in alerts if a.severity == "critical"]
        assert len(critical_alerts) > 0
        
        # Verify alert details
        execution_alerts = [
            a for a in critical_alerts
            if a.metric_type == "pattern_execution_time"
        ]
        assert execution_alerts
        assert execution_alerts[0].value > execution_alerts[0].threshold
        
        # Verify enhanced alert features
        assert execution_alerts[0].correlation_insights, "No correlation insights generated"
        assert execution_alerts[0].trend_insights, "No trend insights generated"
        assert execution_alerts[0].recommended_actions
        
    def test_correlation_analysis(
        self,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        # Generate correlated metrics
        for i in range(100):
            base_value = i * 0.01
            metrics_collector.collect_metric(
                "pattern_execution_time",
                base_value
            )
            metrics_collector.collect_metric(
                "memory_usage_mb",
                base_value * 1000
            )
            
        alerts = alerting_system.check_alerts()
        
        # Find alerts with correlations
        alerts_with_correlations = [
            a for a in alerts
            if any("correlation" in insight for insight in a.correlation_insights)
        ]
        
        assert alerts_with_correlations
        for alert in alerts_with_correlations:
            assert alert.context.correlation_scores
            
    def test_trend_detection(
        self,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        # Generate increasing trend
        base_value = 1500  # Start at warning threshold
        for i in range(10):
            metrics_collector.collect_metric(
                "memory_usage_mb",
                base_value + i * 50  # Significant increase per data point
            )
            
        alerts = alerting_system.check_alerts()
        
        # Find alerts with trend insights
        trend_alerts = [
            a for a in alerts
            if any("trend" in insight.lower() for insight in a.trend_insights)
        ]
        
        assert trend_alerts
        for alert in trend_alerts:
            assert alert.context.trend_score > 0  # Should detect increasing trend
            
    def test_alert_suppression(
        self,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        # Generate alerting condition
        metrics_collector.collect_metric("pattern_execution_time", 0.15)
        
        # Get initial alerts
        initial_alerts = alerting_system.check_alerts()
        assert initial_alerts
        
        # Suppress alerts
        alerting_system.suppress_alerts("pattern_execution_time", 60)
        
        # Generate more alerting conditions
        metrics_collector.collect_metric("pattern_execution_time", 0.2)
        
        # Verify alerts are suppressed
        suppressed_alerts = alerting_system.check_alerts()
        assert not any(
            a.metric_type == "pattern_execution_time"
            for a in suppressed_alerts
        )
        
    def test_alert_handlers(
        self,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        received_alerts = []
        
        def test_handler(alert: EnhancedAlert) -> None:
            received_alerts.append(alert)
            
        alerting_system.add_alert_handler(test_handler)
        
        # Generate alerting condition
        metrics_collector.collect_metric("pattern_execution_time", 0.15)
        
        # Check alerts
        alerts = alerting_system.check_alerts()
        
        # Verify handler was called
        assert len(received_alerts) == len(alerts)
        assert all(isinstance(a, EnhancedAlert) for a in received_alerts)
        
    def test_alert_history(
        self,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        # Generate alerts over time
        for i in range(3):
            metrics_collector.collect_metric("pattern_execution_time", 0.15)
            alerting_system.check_alerts()
            
        # Get alert history
        history = alerting_system.get_alert_history(
            metric_type="pattern_execution_time",
            severity="critical",
            duration_seconds=3600
        )
        
        assert len(history) > 0
        assert all(
            isinstance(alert, EnhancedAlert)
            for alert in history
        )
        assert all(
            alert.metric_type == "pattern_execution_time"
            and alert.severity == "critical"
            for alert in history
        )
        
    def test_alert_stats(
        self,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        # Generate mixed alerts
        metrics_collector.collect_metric("pattern_execution_time", 0.15)  # Critical
        metrics_collector.collect_metric("memory_usage_mb", 1600)        # Warning
        alerting_system.check_alerts()
        
        # Get stats
        stats = alerting_system.get_alert_stats()
        
        assert "total_alerts" in stats
        assert "by_severity" in stats
        assert "by_metric" in stats
        assert stats["by_severity"]["critical"] > 0
        assert stats["by_severity"]["warning"] > 0