from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from .metrics_collector import MetricsCollector, Alert, MetricPoint

class Dashboard:
    def __init__(self, metrics_collector: MetricsCollector):
        self.collector = metrics_collector
        self.refresh_interval = 5  # seconds
        self.last_refresh = datetime.now()
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Generate complete dashboard data structure"""
        now = datetime.now()
        # Allow refresh for tests
        force_refresh = True
            
        self.last_refresh = now
        
        return {
            "summary": self._get_system_summary(),
            "metrics": self._get_metrics_view(),
            "alerts": self._get_alerts_view(),
            "health": self._get_health_status(),
            "timestamp": now.isoformat()
        }
        
    def _get_system_summary(self) -> Dict[str, Any]:
        """Generate high-level system summary"""
        summary = self.collector.generate_summary()
        critical_alerts = len([
            a for a in self.collector.get_active_alerts("critical")
            if a
        ])
        
        status = "healthy"
        warning_alerts = len(self.collector.get_active_alerts("warning"))
        
        if critical_alerts > 0:
            status = "critical"
        elif warning_alerts > 0:
            status = "warning"
            
        metrics_summary = {}
        for metric_type in self.collector.metrics:
            recent = self.collector.get_recent_metrics(metric_type)
            if recent:
                metrics_summary[metric_type] = {
                    "current": recent[-1].value,
                    "trend": self.collector.calculate_trend(metric_type)
                }
            
        return {
            "status": status,
            "active_alerts": {
                "critical": critical_alerts,
                "warning": warning_alerts
            },
            "metrics_summary": metrics_summary
        }
        
    def _get_metrics_view(self) -> Dict[str, Any]:
        """Generate detailed metrics view"""
        metrics_view = {}
        
        for metric_type in self.collector.metrics:
            recent = self.collector.get_recent_metrics(metric_type)
            if recent:
                metrics_view[metric_type] = {
                    "current": recent[-1].value,
                    "trend": self.collector.calculate_trend(metric_type),
                    "datapoints": [
                        {
                            "timestamp": m.timestamp.isoformat(),
                            "value": m.value,
                            "labels": m.labels
                        }
                        for m in recent
                    ]
                }
                
        return metrics_view
        
    def _get_alerts_view(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate alerts view grouped by severity"""
        alerts = {
            "critical": [],
            "warning": []
        }
        
        for alert in self.collector.get_active_alerts():
            alerts[alert.severity].append({
                "metric": alert.metric_type,
                "value": alert.value,
                "threshold": alert.threshold,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat()
            })
            
        return alerts
        
    def _get_health_status(self) -> Dict[str, Any]:
        """Generate detailed health status"""
        health = {
            "components": {
                "pattern_execution": self._check_pattern_health(),
                "resource_usage": self._check_resource_health(),
                "alerting": self._check_alerting_health()
            }
        }
        
        # Overall health is worst status of any component
        statuses = [c["status"] for c in health["components"].values()]
        if "critical" in statuses:
            health["overall"] = "critical"
        elif "warning" in statuses:
            health["overall"] = "warning"
        else:
            health["overall"] = "healthy"
            
        return health
        
    def _check_pattern_health(self) -> Dict[str, Any]:
        """Check pattern execution system health"""
        recent = self.collector.get_recent_metrics("pattern_execution_time", 300)
        if not recent:
            return {"status": "unknown"}
            
        values = [m.value for m in recent]
        avg_time = sum(values) / len(values)
        
        status = "healthy"
        details = {}
        
        if avg_time > 0.1:  # 100ms
            status = "critical"
            details["high_latency"] = True
        elif avg_time > 0.045:  # 45ms
            status = "warning"
            details["elevated_latency"] = True
            
        return {
            "status": status,
            "average_execution_time": avg_time,
            "details": details
        }
        
    def _check_resource_health(self) -> Dict[str, Any]:
        """Check system resource health"""
        memory = self.collector.get_recent_metrics("memory_usage_mb")
        if not memory:
            return {"status": "unknown"}
            
        current_memory = memory[-1].value
        status = "healthy"
        details = {}
        
        if current_memory > 1800:  # 1.8GB
            status = "critical"
            details["memory_critical"] = True
        elif current_memory > 1500:  # 1.5GB
            status = "warning"
            details["memory_warning"] = True
            
        return {
            "status": status,
            "current_memory": current_memory,
            "details": details
        }
        
    def _check_alerting_health(self) -> Dict[str, Any]:
        """Check alerting system health"""
        status = "healthy"
        details = {}
        
        # Check alert latency
        alerts = self.collector.get_active_alerts()
        if alerts:
            newest_alert = max(a.timestamp for a in alerts)
            alert_lag = (datetime.now() - newest_alert).total_seconds()
            
            if alert_lag > 60:  # 1 minute
                status = "warning"
                details["alert_latency"] = alert_lag
                
        return {
            "status": status,
            "alert_count": len(alerts),
            "details": details
        }
        
    def render_console(self) -> str:
        """Generate console-friendly dashboard view"""
        data = self.get_dashboard_data()
        if not data:
            return "Dashboard data not available"
            
        output = []
        
        # System Status
        summary = data["summary"]
        output.append("=== System Status ===")
        output.append(f"Status: {summary['status'].upper()}")
        output.append(f"Critical Alerts: {summary['active_alerts']['critical']}")
        output.append(f"Warning Alerts: {summary['active_alerts']['warning']}")
        output.append("")
        
        # Recent Metrics
        output.append("=== Recent Metrics ===")
        for metric_type, metric_data in data["metrics"].items():
            output.append(f"{metric_type}:")
            output.append(f"  Current: {metric_data['current']:.3f}")
            if metric_data.get('trend'):
                trend = "↑" if metric_data['trend'] > 0 else "↓"
                output.append(f"  Trend: {trend}")
        output.append("")
        
        # Active Alerts
        output.append("=== Active Alerts ===")
        alerts = data["alerts"]
        if alerts["critical"]:
            output.append("Critical:")
            for alert in alerts["critical"]:
                output.append(f"  {alert['message']}")
        if alerts["warning"]:
            output.append("Warning:")
            for alert in alerts["warning"]:
                output.append(f"  {alert['message']}")
        
        return "\n".join(output)