import pytest
from datetime import datetime, timedelta
import time
from typing import Dict, Any

from src.monitoring.metrics_collector import MetricsCollector, Alert, MetricPoint
from src.monitoring.dashboard import Dashboard

class TestMonitoring:
    class MetricSubscriber:
        def __init__(self):
            self.received_metrics = []
            
        def handle_metric(self, metric: MetricPoint) -> None:
            self.received_metrics.append(metric)
            
    @pytest.fixture
    def subscriber(self) -> MetricSubscriber:
        return TestMonitoring.MetricSubscriber()
    @pytest.fixture
    def metrics_collector(self) -> MetricsCollector:
        return MetricsCollector()
    
    @pytest.fixture
    def dashboard(self, metrics_collector: MetricsCollector) -> Dashboard:
        return Dashboard(metrics_collector)

    def test_metrics_collection(self, metrics_collector: MetricsCollector):
        # Collect test metrics
        metrics_collector.collect_metric("pattern_execution_time", 0.025)
        metrics_collector.collect_metric("pattern_execution_time", 0.035)
        metrics_collector.collect_metric("memory_usage_mb", 1000)
        
        # Verify metrics stored correctly
        metrics = metrics_collector.get_recent_metrics("pattern_execution_time")
        assert len(metrics) == 2
        assert metrics[0].value == 0.025
        assert metrics[1].value == 0.035
        
        memory_metrics = metrics_collector.get_recent_metrics("memory_usage_mb")
        assert len(memory_metrics) == 1
        assert memory_metrics[0].value == 1000

    def test_alert_generation(self, metrics_collector: MetricsCollector):
        # Generate metrics that should trigger alerts
        for _ in range(10):
            metrics_collector.collect_metric("pattern_execution_time", 0.15)  # Above critical
            metrics_collector.collect_metric("pattern_success_rate", 0.85)   # Below critical
        
        # Check alerts generated
        critical_alerts = metrics_collector.get_active_alerts("critical")
        assert len(critical_alerts) >= 2
        
        # Verify alert details
        execution_alerts = [a for a in critical_alerts if a.metric_type == "pattern_execution_time"]
        assert execution_alerts
        assert execution_alerts[0].value > execution_alerts[0].threshold

    def test_trend_analysis(self, metrics_collector: MetricsCollector):
        # Generate increasing trend
        for i in range(10):
            metrics_collector.collect_metric("test_metric", i * 0.1)
        
        trend = metrics_collector.calculate_trend("test_metric")
        assert trend > 0  # Should detect increasing trend
        
        # Generate decreasing trend
        for i in range(10):
            metrics_collector.collect_metric("test_metric_2", (10 - i) * 0.1)
            
        trend = metrics_collector.calculate_trend("test_metric_2")
        assert trend < 0  # Should detect decreasing trend

    def test_dashboard_generation(self, dashboard: Dashboard):
        # Generate test data
        collector = dashboard.collector
        
        # Add normal metrics
        collector.collect_metric("pattern_execution_time", 0.025)
        collector.collect_metric("memory_usage_mb", 1000)
        
        # Add some alerts
        collector.collect_metric("pattern_execution_time", 0.15)  # Should trigger critical
        
        # Get dashboard data
        data = dashboard.get_dashboard_data()
        
        # Verify dashboard structure
        assert "summary" in data
        assert "metrics" in data
        assert "alerts" in data
        assert "health" in data
        
        # Check summary
        assert data["summary"]["status"] in ["healthy", "warning", "critical"]
        
        # Check metrics view
        assert "pattern_execution_time" in data["metrics"]
        assert "memory_usage_mb" in data["metrics"]
        
        # Check alerts
        assert "critical" in data["alerts"]
        assert "warning" in data["alerts"]
        
        # Verify console rendering
        console_output = dashboard.render_console()
        assert "System Status" in console_output
        assert "Recent Metrics" in console_output
        assert "Active Alerts" in console_output

    def test_health_status(self, dashboard: Dashboard):
        collector = dashboard.collector
        
        # System healthy
        collector.collect_metric("pattern_execution_time", 0.025)
        collector.collect_metric("memory_usage_mb", 1000)
        data = dashboard.get_dashboard_data()
        assert data["health"]["overall"] == "healthy"
        
        # System warning
        collector.collect_metric("pattern_execution_time", 0.05)
        collector.collect_metric("memory_usage_mb", 1600)
        data = dashboard.get_dashboard_data()
        assert data["health"]["overall"] == "warning"
        
        # System critical
        collector.collect_metric("pattern_execution_time", 0.15)
        collector.collect_metric("memory_usage_mb", 2000)
        data = dashboard.get_dashboard_data()
        assert data["health"]["overall"] == "critical"
    
    def test_realtime_metrics(self, metrics_collector: MetricsCollector, subscriber: MetricSubscriber):
        # Subscribe to metrics
        metrics_collector.subscribe("test_metric", subscriber.handle_metric)
        
        # Generate test metrics
        metrics_collector.collect_metric("test_metric", 1.0)
        metrics_collector.collect_metric("test_metric", 2.0)
        metrics_collector.collect_metric("test_metric", 3.0)
        
        # Flush metrics to ensure processing
        metrics_collector.flush_metrics()
        
        # Verify subscriber received metrics
        assert len(subscriber.received_metrics) == 3
        assert [m.value for m in subscriber.received_metrics] == [1.0, 2.0, 3.0]
        
        # Test unsubscribe
        metrics_collector.unsubscribe("test_metric", subscriber.handle_metric)
        metrics_collector.collect_metric("test_metric", 4.0)
        metrics_collector.flush_metrics()
        
        # Verify no new metrics received after unsubscribe
        assert len(subscriber.received_metrics) == 3