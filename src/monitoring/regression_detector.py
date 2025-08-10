from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from collections import deque
from scipy import stats

@dataclass
class RegressionThreshold:
    warning_threshold: float  # Relative change that triggers warning
    critical_threshold: float  # Relative change that triggers critical alert
    minimum_samples: int  # Minimum samples required for detection
    window_size: int  # Window size for moving average
    confidence_level: float  # Required statistical confidence (0-1)

@dataclass
class RegressionResult:
    metric_type: str
    timestamp: datetime
    baseline_mean: float
    current_mean: float
    relative_change: float
    p_value: float
    confidence_level: float
    severity: str  # "none", "warning", or "critical"
    message: str

class RegressionDetector:
    def __init__(self):
        self.thresholds: Dict[str, RegressionThreshold] = {}
        self.baseline_data: Dict[str, List[float]] = {}
        self.current_data: Dict[str, deque] = {}
        self.detection_history: Dict[str, List[RegressionResult]] = {}
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
        
    def _initialize_default_thresholds(self) -> None:
        self.thresholds = {
            "pattern_execution_time": RegressionThreshold(
                warning_threshold=0.20,   # 20% increase
                critical_threshold=0.40,  # 40% increase
                minimum_samples=10,
                window_size=20,
                confidence_level=0.99  # Higher confidence to resist false positives
            ),
            "pattern_success_rate": RegressionThreshold(
                warning_threshold=-0.05,   # 5% decrease
                critical_threshold=-0.10,  # 10% decrease
                minimum_samples=10,
                window_size=20,
                confidence_level=0.95
            ),
            "memory_usage_mb": RegressionThreshold(
                warning_threshold=0.08,   # 8% increase
                critical_threshold=0.15,  # 15% increase
                minimum_samples=10,
                window_size=20,
                confidence_level=0.95
            )
        }
        
    def add_metric_value(
        self,
        metric_type: str,
        value: float,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Add a new metric value for regression analysis"""
        if metric_type not in self.current_data:
            self.current_data[metric_type] = deque(maxlen=self.thresholds[metric_type].window_size)
            
        self.current_data[metric_type].append(value)
        
    def set_baseline(self, metric_type: str, values: List[float]) -> None:
        """Set baseline data for a metric type"""
        self.baseline_data[metric_type] = list(values)
        
    def detect_regression(self, metric_type: str) -> Optional[RegressionResult]:
        """Detect performance regression using statistical analysis"""
        if metric_type not in self.thresholds:
            return None
            
        threshold = self.thresholds[metric_type]
        
        # Check if we have enough data
        if (
            metric_type not in self.baseline_data
            or metric_type not in self.current_data
            or len(self.baseline_data[metric_type]) < threshold.minimum_samples
            or len(self.current_data[metric_type]) < threshold.minimum_samples
        ):
            return None
            
        # Calculate statistics
        baseline_mean = np.mean(self.baseline_data[metric_type])
        current_mean = np.mean(self.current_data[metric_type])
        relative_change = (current_mean - baseline_mean) / baseline_mean
        
        # Perform statistical test
        t_stat, p_value = stats.ttest_ind(
            self.baseline_data[metric_type],
            list(self.current_data[metric_type])
        )
        
        # Determine severity
        severity = "none"
        if p_value < (1 - threshold.confidence_level):
            if abs(relative_change) >= abs(threshold.critical_threshold):
                severity = "critical"
            elif abs(relative_change) >= abs(threshold.warning_threshold):
                severity = "warning"
                
        # Generate result
        result = RegressionResult(
            metric_type=metric_type,
            timestamp=datetime.now(),
            baseline_mean=baseline_mean,
            current_mean=current_mean,
            relative_change=relative_change,
            p_value=p_value,
            confidence_level=threshold.confidence_level,
            severity=severity,
            message=self._generate_regression_message(
                metric_type,
                baseline_mean,
                current_mean,
                relative_change,
                p_value,
                severity
            )
        )
        
        # Update history
        if metric_type not in self.detection_history:
            self.detection_history[metric_type] = []
        self.detection_history[metric_type].append(result)
        
        return result
        
    def _generate_regression_message(
        self,
        metric_type: str,
        baseline_mean: float,
        current_mean: float,
        relative_change: float,
        p_value: float,
        severity: str
    ) -> str:
        direction = "increased" if relative_change > 0 else "decreased"
        percentage = abs(relative_change * 100)
        
        message = (
            f"{severity.upper()}: {metric_type} has {direction} by "
            f"{percentage:.1f}% ({baseline_mean:.3f} → {current_mean:.3f})\n"
        )
        
        if severity != "none":
            message += (
                f"Statistical significance: p-value = {p_value:.3f} "
                f"(confidence = {(1 - p_value) * 100:.1f}%)"
            )
        
        return message.strip()
        
    def detect_all_regressions(self) -> Dict[str, RegressionResult]:
        """Detect regressions for all metrics with data"""
        results = {}
        for metric_type in self.current_data:
            result = self.detect_regression(metric_type)
            if result and result.severity != "none":
                results[metric_type] = result
                
        return results
        
    def get_detection_history(
        self,
        metric_type: Optional[str] = None,
        severity: Optional[str] = None,
        duration_seconds: int = 3600
    ) -> List[RegressionResult]:
        """Get regression detection history with optional filtering"""
        cutoff = datetime.now() - timedelta(seconds=duration_seconds)
        
        results = []
        for m_type, history in self.detection_history.items():
            if metric_type and m_type != metric_type:
                continue
                
            results.extend([
                result for result in history
                if result.timestamp > cutoff
                and (not severity or result.severity == severity)
            ])
            
        return sorted(results, key=lambda x: x.timestamp, reverse=True)
        
    def get_regression_stats(
        self,
        duration_seconds: int = 3600
    ) -> Dict[str, Any]:
        """Get regression detection statistics"""
        detections = self.get_detection_history(duration_seconds=duration_seconds)
        
        return {
            "total_regressions": len([d for d in detections if d.severity != "none"]),
            "by_severity": {
                "critical": len([d for d in detections if d.severity == "critical"]),
                "warning": len([d for d in detections if d.severity == "warning"])
            },
            "by_metric": {
                metric: len([
                    d for d in detections
                    if d.metric_type == metric and d.severity != "none"
                ])
                for metric in self.thresholds
            }
        }