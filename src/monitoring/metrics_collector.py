from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import numpy as np
from collections import deque

@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    metric_type: str
    labels: Dict[str, str]

@dataclass
class AlertThreshold:
    metric_type: str
    warning_threshold: float
    critical_threshold: float
    comparison: str  # "above" or "below"
    duration_seconds: int  # Alert after threshold exceeded for this duration

@dataclass
class Alert:
    metric_type: str
    severity: str  # "warning" or "critical"
    value: float
    threshold: float
    timestamp: datetime
    message: str

class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, List[MetricPoint]] = {}
        self.alert_thresholds: Dict[str, AlertThreshold] = {}
        self.alerts: List[Alert] = []
        self.metric_windows: Dict[str, deque] = {}  # Rolling windows for trend analysis
        self.window_size = 100  # Default window size
        self.subscribers: Dict[str, List[Any]] = {}  # Subscribers for real-time updates
        self.metric_buffer: Dict[str, List[MetricPoint]] = {}  # Buffer for batched updates
        self.batch_size = 10  # Number of metrics to process in a batch
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
        
    def _initialize_default_thresholds(self) -> None:
        self.alert_thresholds = {
            "pattern_execution_time": AlertThreshold(
                metric_type="pattern_execution_time",
                warning_threshold=0.045,  # 45ms
                critical_threshold=0.1,    # 100ms
                comparison="above",
                duration_seconds=60
            ),
            "pattern_success_rate": AlertThreshold(
                metric_type="pattern_success_rate",
                warning_threshold=0.95,
                critical_threshold=0.90,
                comparison="below",
                duration_seconds=300
            ),
            "memory_usage_mb": AlertThreshold(
                metric_type="memory_usage_mb",
                warning_threshold=1500,
                critical_threshold=1800,
                comparison="above",
                duration_seconds=120
            )
        }
    
    def collect_metric(
        self,
        metric_type: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        metric = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            metric_type=metric_type,
            labels=labels or {}
        )
        
        if metric_type not in self.metrics:
            self.metrics[metric_type] = []
        self.metrics[metric_type].append(metric)
        
        # Update rolling window
        if metric_type not in self.metric_windows:
            self.metric_windows[metric_type] = deque(maxlen=self.window_size)
        self.metric_windows[metric_type].append(value)
        
        # Buffer and process metric
        if metric_type not in self.metric_buffer:
            self.metric_buffer[metric_type] = []
        self.metric_buffer[metric_type].append(metric)
        
        # Process buffer if it reaches batch size
        if len(self.metric_buffer[metric_type]) >= self.batch_size:
            self._process_metric_batch(metric_type)

    def _process_metric_batch(self, metric_type: str) -> None:
        metrics = self.metric_buffer[metric_type]
        self.metric_buffer[metric_type] = []
        
        # Update metrics storage
        if metric_type not in self.metrics:
            self.metrics[metric_type] = []
        self.metrics[metric_type].extend(metrics)
        
        # Update rolling windows
        if metric_type not in self.metric_windows:
            self.metric_windows[metric_type] = deque(maxlen=self.window_size)
        for metric in metrics:
            self.metric_windows[metric_type].append(metric.value)
        
        # Process each metric
        for metric in metrics:
            self._check_thresholds(metric)
            self._notify_subscribers(metric_type, metric)
        
    def _check_thresholds(self, metric: MetricPoint) -> None:
        if metric.metric_type not in self.alert_thresholds:
            return
            
        threshold = self.alert_thresholds[metric.metric_type]
        recent_metrics = [
            m for m in self.metrics[metric.metric_type]
            if (datetime.now() - m.timestamp).total_seconds() <= threshold.duration_seconds
        ]
        
        if not recent_metrics:
            return
            
        avg_value = np.mean([m.value for m in recent_metrics])
        
        # Check warning threshold
        if self._threshold_exceeded(avg_value, threshold.warning_threshold, threshold.comparison):
            self._create_alert(metric.metric_type, "warning", avg_value, threshold.warning_threshold)
            
        # Check critical threshold
        if self._threshold_exceeded(avg_value, threshold.critical_threshold, threshold.comparison):
            self._create_alert(metric.metric_type, "critical", avg_value, threshold.critical_threshold)
    
    def _threshold_exceeded(self, value: float, threshold: float, comparison: str) -> bool:
        if comparison == "above":
            return value > threshold
        return value < threshold
    
    def _create_alert(
        self,
        metric_type: str,
        severity: str,
        value: float,
        threshold: float
    ) -> None:
        alert = Alert(
            metric_type=metric_type,
            severity=severity,
            value=value,
            threshold=threshold,
            timestamp=datetime.now(),
            message=f"{severity.upper()}: {metric_type} = {value:.3f} ({threshold:.3f} threshold)"
        )
        self.alerts.append(alert)
    
    def get_recent_metrics(
        self,
        metric_type: str,
        duration_seconds: int = 300
    ) -> List[MetricPoint]:
        if metric_type not in self.metrics:
            return []
            
        cutoff = datetime.now().timestamp() - duration_seconds
        return [
            m for m in self.metrics[metric_type]
            if m.timestamp.timestamp() > cutoff
        ]
    
    def get_active_alerts(
        self,
        severity: Optional[str] = None,
        duration_seconds: int = 300
    ) -> List[Alert]:
        cutoff = datetime.now().timestamp() - duration_seconds
        filtered = [
            a for a in self.alerts
            if a.timestamp.timestamp() > cutoff
        ]
        
        if severity:
            filtered = [a for a in filtered if a.severity == severity]
            
        return filtered
    
    def calculate_trend(self, metric_type: str) -> Optional[float]:
        if metric_type not in self.metric_windows:
            return None
            
        values = list(self.metric_windows[metric_type])
        if len(values) < 2:
            return None
            
        # Simple linear regression slope
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        return slope
    
    def generate_summary(self, duration_seconds: int = 300) -> Dict[str, Any]:
        summary = {
            "metrics": {},
            "alerts": {
                "warning": len([a for a in self.get_active_alerts("warning") if a]),
                "critical": len([a for a in self.get_active_alerts("critical") if a])
            },
            "trends": {}
        }
        
        for metric_type in self.metrics:
            recent = self.get_recent_metrics(metric_type, duration_seconds)
            if recent:
                values = [m.value for m in recent]
                summary["metrics"][metric_type] = {
                    "current": values[-1],
                    "min": min(values),
                    "max": max(values),
                    "avg": np.mean(values)
                }
                
                trend = self.calculate_trend(metric_type)
                if trend is not None:
                    summary["trends"][metric_type] = trend
                    
        return summary

    def subscribe(self, metric_type: str, callback: Any) -> None:
        if metric_type not in self.subscribers:
            self.subscribers[metric_type] = []
        self.subscribers[metric_type].append(callback)
    
    def unsubscribe(self, metric_type: str, callback: Any) -> None:
        if metric_type in self.subscribers:
            if callback in self.subscribers[metric_type]:
                self.subscribers[metric_type].remove(callback)
    
    def _notify_subscribers(self, metric_type: str, metric: MetricPoint) -> None:
        if metric_type in self.subscribers:
            for callback in self.subscribers[metric_type]:
                try:
                    callback(metric)
                except Exception as e:
                    print(f"Error notifying subscriber: {e}")
    
    def flush_metrics(self) -> None:
        for metric_type in list(self.metric_buffer.keys()):
            if self.metric_buffer[metric_type]:
                self._process_metric_batch(metric_type)