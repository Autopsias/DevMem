"""
Real-time Usage Tracking and Budget Monitoring Dashboard

Provides real-time monitoring of token usage, cost tracking, and budget alerts
for Claude Code agent coordination system.
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from .token_estimation import (
    TokenUsageTracker, TokenEstimator, ModelType, PromptType,
    get_usage_tracker, get_token_estimator
)
from .prompt_cache import get_cache_manager


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Alert:
    """Represents a usage alert."""
    timestamp: datetime
    level: AlertLevel
    message: str
    metric_value: float
    threshold_value: float
    alert_type: str


class BudgetMonitor:
    """
    Real-time budget monitoring with threshold alerts.
    
    Features:
    - Configurable budget thresholds
    - Real-time usage tracking
    - Alert notifications
    - Usage projections
    """
    
    def __init__(self, 
                 daily_budget_usd: float = 10.0,
                 warning_threshold: float = 0.8,
                 critical_threshold: float = 0.95):
        """
        Initialize budget monitor.
        
        Args:
            daily_budget_usd: Daily budget limit
            warning_threshold: Warning threshold (fraction of budget)
            critical_threshold: Critical threshold (fraction of budget)
        """
        self.daily_budget_usd = daily_budget_usd
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        self._lock = threading.RLock()
        
        # Get usage tracker and add warning callback
        self.usage_tracker = get_usage_tracker()
        self.usage_tracker.add_warning_callback(self._on_usage_warning)
    
    def _on_usage_warning(self, message: str, current_cost: float, budget: float) -> None:
        """Handle usage warnings from tracker."""
        usage_percent = (current_cost / budget) * 100
        
        if usage_percent >= self.critical_threshold * 100:
            level = AlertLevel.CRITICAL
        elif usage_percent >= self.warning_threshold * 100:
            level = AlertLevel.WARNING
        else:
            level = AlertLevel.INFO
        
        alert = Alert(
            timestamp=datetime.now(),
            level=level,
            message=message,
            metric_value=current_cost,
            threshold_value=budget * (self.critical_threshold if level == AlertLevel.CRITICAL else self.warning_threshold),
            alert_type="budget_threshold"
        )
        
        self._add_alert(alert)
    
    def _add_alert(self, alert: Alert) -> None:
        """Add alert and trigger callbacks."""
        with self._lock:
            self.alerts.append(alert)
            
            # Keep only recent alerts (last 100)
            if len(self.alerts) > 100:
                self.alerts = self.alerts[-100:]
            
            # Trigger callbacks
            for callback in self.alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    print(f"Alert callback error: {e}")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Add callback for alert notifications."""
        self.alert_callbacks.append(callback)
    
    def check_usage_projection(self) -> Optional[Alert]:
        """
        Check if current usage trend will exceed budget.
        
        Returns:
            Alert if projection exceeds budget, None otherwise
        """
        today_stats = self.usage_tracker.get_daily_usage()
        if not today_stats or today_stats.total_requests < 5:
            return None  # Not enough data for projection
        
        # Calculate hourly rate
        now = datetime.now()
        hours_elapsed = now.hour + (now.minute / 60.0)
        
        if hours_elapsed < 1:
            return None  # Too early in the day
        
        hourly_cost = today_stats.total_cost / hours_elapsed
        projected_daily_cost = hourly_cost * 24
        
        if projected_daily_cost > self.daily_budget_usd:
            alert = Alert(
                timestamp=now,
                level=AlertLevel.WARNING,
                message=f"Projected daily cost ${projected_daily_cost:.4f} exceeds budget ${self.daily_budget_usd:.2f}",
                metric_value=projected_daily_cost,
                threshold_value=self.daily_budget_usd,
                alert_type="budget_projection"
            )
            
            self._add_alert(alert)
            return alert
        
        return None
    
    def get_recent_alerts(self, hours: int = 24) -> List[Alert]:
        """Get recent alerts within specified hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        with self._lock:
            return [alert for alert in self.alerts if alert.timestamp > cutoff]


class PerformanceMonitor:
    """
    Monitors cache performance and coordination efficiency.
    
    Features:
    - Cache hit rate monitoring
    - Response time tracking
    - Performance regression detection
    """
    
    def __init__(self):
        """Initialize performance monitor."""
        self.cache_manager = get_cache_manager()
        self.performance_history: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        
        # Start periodic monitoring
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._collect_performance_metrics()
                time.sleep(60)  # Collect metrics every minute
            except Exception as e:
                print(f"Performance monitoring error: {e}")
    
    def _collect_performance_metrics(self) -> None:
        """Collect and store performance metrics."""
        cache_stats = self.cache_manager.get_stats()
        cache_info = self.cache_manager.get_cache_info()
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cache_hit_rate": cache_stats.hit_rate,
            "cache_miss_rate": cache_stats.miss_rate,
            "total_requests": cache_stats.total_requests,
            "storage_size_mb": cache_stats.storage_size_bytes / (1024 * 1024),
            "entries_count": cache_info["entries_count"],
            "evictions": cache_stats.evictions
        }
        
        with self._lock:
            self.performance_history.append(metrics)
            
            # Keep only recent history (last 24 hours)
            cutoff_time = datetime.now() - timedelta(hours=24)
            cutoff_iso = cutoff_time.isoformat()
            
            self.performance_history = [
                m for m in self.performance_history
                if m["timestamp"] > cutoff_iso
            ]
    
    def get_performance_summary(self, hours: int = 1) -> Dict[str, Any]:
        """
        Get performance summary for recent period.
        
        Args:
            hours: Hours to analyze
            
        Returns:
            Performance summary
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_iso = cutoff_time.isoformat()
        
        with self._lock:
            recent_metrics = [
                m for m in self.performance_history
                if m["timestamp"] > cutoff_iso
            ]
        
        if not recent_metrics:
            return {"error": "No performance data available"}
        
        # Calculate averages
        total_metrics = len(recent_metrics)
        avg_hit_rate = sum(m["cache_hit_rate"] for m in recent_metrics) / total_metrics
        avg_storage_mb = sum(m["storage_size_mb"] for m in recent_metrics) / total_metrics
        
        latest = recent_metrics[-1] if recent_metrics else {}
        
        return {
            "period_hours": hours,
            "average_cache_hit_rate": round(avg_hit_rate, 2),
            "average_storage_mb": round(avg_storage_mb, 2),
            "current_entries_count": latest.get("entries_count", 0),
            "current_hit_rate": round(latest.get("cache_hit_rate", 0), 2),
            "total_evictions": latest.get("evictions", 0),
            "data_points": total_metrics
        }
    
    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.monitoring = False


class UsageDashboard:
    """
    Main dashboard for real-time usage monitoring and reporting.
    
    Combines budget monitoring, performance tracking, and alert management
    into a unified interface.
    """
    
    def __init__(self, 
                 daily_budget_usd: float = 10.0,
                 auto_alerts: bool = True):
        """
        Initialize usage dashboard.
        
        Args:
            daily_budget_usd: Daily budget limit
            auto_alerts: Enable automatic alert monitoring
        """
        self.daily_budget_usd = daily_budget_usd
        self.auto_alerts = auto_alerts
        
        # Components
        self.usage_tracker = get_usage_tracker()
        self.token_estimator = get_token_estimator()
        self.cache_manager = get_cache_manager()
        self.budget_monitor = BudgetMonitor(daily_budget_usd)
        self.performance_monitor = PerformanceMonitor()
        
        # Dashboard state
        self.dashboard_data = {}
        self._lock = threading.RLock()
        
        # Auto-refresh dashboard data
        if auto_alerts:
            self.refresh_thread = threading.Thread(target=self._auto_refresh, daemon=True)
            self.refresh_thread.start()
    
    def _auto_refresh(self) -> None:
        """Auto-refresh dashboard data."""
        while True:
            try:
                self.refresh_dashboard()
                time.sleep(30)  # Refresh every 30 seconds
            except Exception as e:
                print(f"Dashboard refresh error: {e}")
    
    def refresh_dashboard(self) -> None:
        """Refresh all dashboard data."""
        with self._lock:
            self.dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "budget_status": self._get_budget_status(),
                "usage_summary": self._get_usage_summary(),
                "cache_performance": self._get_cache_performance(),
                "recent_alerts": self._get_recent_alerts(),
                "projections": self._get_projections()
            }
    
    def _get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status."""
        today_stats = self.usage_tracker.get_daily_usage()
        
        if not today_stats:
            return {
                "daily_budget_usd": self.daily_budget_usd,
                "spent_today_usd": 0.0,
                "remaining_usd": self.daily_budget_usd,
                "utilization_percent": 0.0,
                "status": "within_budget"
            }
        
        remaining = max(0, self.daily_budget_usd - today_stats.total_cost)
        utilization = (today_stats.total_cost / self.daily_budget_usd) * 100
        
        if utilization >= 95:
            status = "budget_exceeded"
        elif utilization >= 80:
            status = "budget_warning"
        else:
            status = "within_budget"
        
        return {
            "daily_budget_usd": self.daily_budget_usd,
            "spent_today_usd": round(today_stats.total_cost, 6),
            "remaining_usd": round(remaining, 6),
            "utilization_percent": round(utilization, 1),
            "status": status,
            "total_requests_today": today_stats.total_requests
        }
    
    def _get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary."""
        weekly_report = self.usage_tracker.get_weekly_report()
        usage_by_type = self.usage_tracker.get_usage_by_prompt_type(days=1)
        
        return {
            "weekly_summary": weekly_report.get("summary", {}),
            "today_by_prompt_type": {
                ptype: {
                    "requests": stats.total_requests,
                    "cost_usd": round(stats.total_cost, 6),
                    "tokens": stats.total_input_tokens + stats.total_output_tokens
                }
                for ptype, stats in usage_by_type.items()
            }
        }
    
    def _get_cache_performance(self) -> Dict[str, Any]:
        """Get cache performance metrics."""
        cache_stats = self.cache_manager.get_stats()
        perf_summary = self.performance_monitor.get_performance_summary(hours=1)
        
        return {
            "hit_rate_percent": round(cache_stats.hit_rate, 1),
            "total_requests": cache_stats.total_requests,
            "storage_mb": round(cache_stats.storage_size_bytes / (1024 * 1024), 2),
            "recent_performance": perf_summary
        }
    
    def _get_recent_alerts(self) -> List[Dict[str, Any]]:
        """Get recent alerts."""
        alerts = self.budget_monitor.get_recent_alerts(hours=24)
        
        return [
            {
                "timestamp": alert.timestamp.isoformat(),
                "level": alert.level.value,
                "message": alert.message,
                "alert_type": alert.alert_type
            }
            for alert in alerts[-10:]  # Last 10 alerts
        ]
    
    def _get_projections(self) -> Dict[str, Any]:
        """Get usage projections."""
        remaining_budget = self.usage_tracker.estimate_remaining_budget_requests()
        
        # Check projection alert
        projection_alert = self.budget_monitor.check_usage_projection()
        
        projections = {
            "remaining_budget": remaining_budget,
            "projection_alert": None
        }
        
        if projection_alert:
            projections["projection_alert"] = {
                "message": projection_alert.message,
                "projected_cost": projection_alert.metric_value
            }
        
        return projections
    
    def get_dashboard_data(self, refresh: bool = False) -> Dict[str, Any]:
        """
        Get current dashboard data.
        
        Args:
            refresh: Force refresh before returning data
            
        Returns:
            Complete dashboard data
        """
        if refresh or not self.dashboard_data:
            self.refresh_dashboard()
        
        with self._lock:
            return self.dashboard_data.copy()
    
    def get_real_time_status(self) -> Dict[str, Any]:
        """Get real-time status summary."""
        budget_status = self._get_budget_status()
        cache_stats = self.cache_manager.get_stats()
        recent_alerts = self.budget_monitor.get_recent_alerts(hours=1)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "budget_utilization": budget_status["utilization_percent"],
            "budget_status": budget_status["status"],
            "cache_hit_rate": round(cache_stats.hit_rate, 1),
            "active_alerts": len([a for a in recent_alerts if a.level != AlertLevel.INFO]),
            "requests_today": budget_status.get("total_requests_today", 0)
        }
    
    def export_usage_report(self, days: int = 7) -> Dict[str, Any]:
        """
        Export comprehensive usage report.
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Detailed usage report
        """
        weekly_report = self.usage_tracker.get_weekly_report()
        usage_by_type = self.usage_tracker.get_usage_by_prompt_type(days=days)
        cache_info = self.cache_manager.get_cache_info()
        perf_summary = self.performance_monitor.get_performance_summary(hours=24)
        
        return {
            "report_period_days": days,
            "generated_at": datetime.now().isoformat(),
            "usage_summary": weekly_report,
            "usage_by_prompt_type": {
                ptype: asdict(stats) for ptype, stats in usage_by_type.items()
            },
            "cache_performance": {
                "cache_info": cache_info,
                "performance_summary": perf_summary
            },
            "budget_analysis": {
                "daily_budget": self.daily_budget_usd,
                "average_daily_cost": weekly_report.get("summary", {}).get("daily_average_cost", 0),
                "budget_efficiency": round(
                    (weekly_report.get("summary", {}).get("daily_average_cost", 0) / self.daily_budget_usd) * 100, 1
                )
            }
        }
    
    def shutdown(self) -> None:
        """Shutdown dashboard and cleanup resources."""
        self.performance_monitor.stop_monitoring()


# Global dashboard instance
_dashboard: Optional[UsageDashboard] = None


def get_usage_dashboard(daily_budget_usd: float = 10.0) -> UsageDashboard:
    """Get or create global usage dashboard."""
    global _dashboard
    if _dashboard is None:
        _dashboard = UsageDashboard(daily_budget_usd=daily_budget_usd)
    return _dashboard


def print_dashboard_status() -> None:
    """Print current dashboard status to console."""
    dashboard = get_usage_dashboard()
    status = dashboard.get_real_time_status()
    
    print("📊 Claude Code Performance Dashboard")
    print("=" * 40)
    print(f"🕐 Timestamp: {status['timestamp']}")
    print(f"💰 Budget Utilization: {status['budget_utilization']}%")
    print(f"📈 Budget Status: {status['budget_status']}")
    print(f"🎯 Cache Hit Rate: {status['cache_hit_rate']}%")
    print(f"⚠️  Active Alerts: {status['active_alerts']}")
    print(f"📋 Requests Today: {status['requests_today']}")
    print("=" * 40)


def export_dashboard_report(output_file: Optional[Path] = None) -> Path:
    """
    Export dashboard report to JSON file.
    
    Args:
        output_file: Output file path (defaults to timestamped file)
        
    Returns:
        Path to exported file
    """
    dashboard = get_usage_dashboard()
    report = dashboard.export_usage_report(days=7)
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path.home() / ".claude" / "reports" / f"usage_report_{timestamp}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Usage report exported to: {output_file}")
    return output_file