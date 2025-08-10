import pytest
from datetime import datetime, timedelta
import numpy as np
from typing import List

from src.monitoring.regression_detector import RegressionDetector, RegressionResult

class TestRegressionDetector:
    @pytest.fixture
    def detector(self) -> RegressionDetector:
        return RegressionDetector()
    
    def test_basic_regression_detection(self, detector: RegressionDetector):
        # Set baseline data (stable values around 100ms)
        baseline_values = [0.100 + np.random.normal(0, 0.005) for _ in range(20)]
        detector.set_baseline("pattern_execution_time", baseline_values)
        
        # Add current data showing degradation (values around 150ms)
        for _ in range(20):
            detector.add_metric_value(
                "pattern_execution_time",
                0.150 + np.random.normal(0, 0.005)
            )
            
        # Detect regression
        result = detector.detect_regression("pattern_execution_time")
        
        assert result is not None
        assert result.severity == "critical"  # 50% increase should trigger critical
        assert result.relative_change > 0.4  # Should detect ~50% increase
        assert result.p_value < 0.05  # Should be statistically significant
        
    def test_gradual_regression_detection(self, detector: RegressionDetector):
        # Set baseline data
        baseline_values = [1000 + np.random.normal(0, 10) for _ in range(20)]
        detector.set_baseline("memory_usage_mb", baseline_values)
        
        # Add gradually increasing values
        for i in range(20):
            detector.add_metric_value(
                "memory_usage_mb",
                1000 + i * 10 + np.random.normal(0, 10)
            )
            
        # Detect regression
        result = detector.detect_regression("memory_usage_mb")
        
        assert result is not None
        assert result.severity in ["warning", "critical"]
        assert result.relative_change > 0
        assert result.p_value < 0.05
        
    def test_false_positive_resistance(self, detector: RegressionDetector):
        # Set baseline data with high variance
        baseline_values = [0.100 + np.random.normal(0, 0.020) for _ in range(20)]
        detector.set_baseline("pattern_execution_time", baseline_values)
        
        # Add similar data with high variance
        for _ in range(20):
            detector.add_metric_value(
                "pattern_execution_time",
                0.105 + np.random.normal(0, 0.020)
            )
            
        # Detect regression
        result = detector.detect_regression("pattern_execution_time")
        
        # Should not detect regression due to high variance
        assert result is None or result.severity == "none"
        
    def test_minimum_samples_requirement(self, detector: RegressionDetector):
        # Set insufficient baseline data
        detector.set_baseline("pattern_execution_time", [0.100, 0.101, 0.099])
        
        # Add insufficient current data
        for value in [0.150, 0.151, 0.149]:
            detector.add_metric_value("pattern_execution_time", value)
            
        # Attempt to detect regression
        result = detector.detect_regression("pattern_execution_time")
        
        # Should not detect regression due to insufficient data
        assert result is None
        
    def test_regression_history(self, detector: RegressionDetector):
        # Generate some regressions
        baseline_values = [0.100 + np.random.normal(0, 0.005) for _ in range(20)]
        detector.set_baseline("pattern_execution_time", baseline_values)
        
        # Generate multiple regression events
        regression_levels = [0.120, 0.150, 0.180]  # Increasing severity
        for level in regression_levels:
            for _ in range(20):
                detector.add_metric_value(
                    "pattern_execution_time",
                    level + np.random.normal(0, 0.005)
                )
            detector.detect_regression("pattern_execution_time")
            
        # Get history
        history = detector.get_detection_history(
            metric_type="pattern_execution_time",
            duration_seconds=3600
        )
        
        assert len(history) == len(regression_levels)
        assert all(isinstance(result, RegressionResult) for result in history)
        
        # Verify increasing severity
        severities = [result.severity for result in reversed(history)]
        assert severities.count("critical") >= 1
        
    def test_regression_stats(self, detector: RegressionDetector):
        # Generate regressions for multiple metrics
        metrics = ["pattern_execution_time", "memory_usage_mb"]
        
        for metric in metrics:
            # Set baseline
            baseline_values = [100 + np.random.normal(0, 2) for _ in range(20)]
            detector.set_baseline(metric, baseline_values)
            
            # Generate regression
            for _ in range(20):
                detector.add_metric_value(
                    metric,
                    150 + np.random.normal(0, 2)
                )
            detector.detect_regression(metric)
            
        # Get stats
        stats = detector.get_regression_stats()
        
        assert stats["total_regressions"] > 0
        assert "by_severity" in stats
        assert "by_metric" in stats
        assert all(
            metric in stats["by_metric"]
            for metric in metrics
        )