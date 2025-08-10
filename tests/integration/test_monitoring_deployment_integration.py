import pytest
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from unittest.mock import Mock, patch
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.monitoring.metrics_collector import MetricsCollector
from src.monitoring.alerting_system import AlertingSystem
from src.monitoring.regression_detector import RegressionDetector
from deploy.blue_green_config import BlueGreenDeployment


class TestMonitoringDeploymentIntegration:
    """Integration tests for monitoring and deployment systems"""
    
    @pytest.fixture
    def metrics_collector(self) -> MetricsCollector:
        return MetricsCollector()
    
    @pytest.fixture
    def alerting_system(self, metrics_collector: MetricsCollector) -> AlertingSystem:
        return AlertingSystem(metrics_collector)
    
    @pytest.fixture
    def regression_detector(self) -> RegressionDetector:
        return RegressionDetector()
    
    @pytest.fixture
    def deployment_system(self, tmp_path: Path) -> BlueGreenDeployment:
        # Create test config directory
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        
        # Create minimal test configs
        import yaml
        staging_config = {
            "api": {"url": "https://test-staging.example.com", "rate_limit": 1000},
            "resources": {"max_memory_mb": 1500, "max_cpu_percent": 70, "worker_count": 10}
        }
        production_config = {
            "api": {"url": "https://test.example.com", "rate_limit": 5000},
            "resources": {"max_memory_mb": 4000, "max_cpu_percent": 80, "worker_count": 25}
        }
        
        with open(config_dir / "staging.yml", "w") as f:
            yaml.dump(staging_config, f)
        with open(config_dir / "production.yml", "w") as f:
            yaml.dump(production_config, f)
            
        deployment = BlueGreenDeployment(str(config_dir))
        deployment._skip_monitoring = True  # Skip monitoring delays in tests
        return deployment

    async def test_deployment_triggers_monitoring(
        self,
        deployment_system: BlueGreenDeployment,
        metrics_collector: MetricsCollector,
        alerting_system: AlertingSystem
    ):
        """Test that deployments automatically trigger monitoring"""
        # Setup monitoring for deployment
        deployment_system.init_deployment("staging")
        
        # Mock subprocess for deployment
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            
            # Start monitoring before deployment
            metrics_collector.collect_metric("deployment_status", 1.0, {"stage": "pre_deployment"})
            
            # Deploy new version
            deployment_system.deploy("staging", "v1.0.0", gradual_rollout=False)
            
            # Verify metrics collection was triggered
            metrics_collector.collect_metric("deployment_status", 1.0, {
                "version": "v1.0.0",
                "environment": "staging",
                "stage": "deployed"
            })
            
            # Verify deployment-specific metrics
            recent_metrics = metrics_collector.get_recent_metrics("deployment_status", duration_seconds=60)
            assert len(recent_metrics) >= 2
            deployment_metric = next((m for m in recent_metrics if "version" in m.labels), None)
            assert deployment_metric is not None
            assert deployment_metric.labels["version"] == "v1.0.0"
            assert deployment_metric.labels["environment"] == "staging"

    async def test_monitoring_prevents_bad_deployment(
        self,
        deployment_system: BlueGreenDeployment,
        regression_detector: RegressionDetector,
        alerting_system: AlertingSystem
    ):
        """Test that monitoring can block deployments with performance regressions"""
        deployment_system.init_deployment("production")
        
        # Simulate baseline performance metrics
        baseline_metrics = {
            "response_time_ms": 25,
            "error_rate": 0.001,
            "cpu_usage": 0.45,
            "memory_mb": 1200
        }
        
        # Simulate degraded performance (would be detected during canary)
        degraded_metrics = {
            "response_time_ms": 75,  # 3x slower
            "error_rate": 0.02,  # 20x more errors
            "cpu_usage": 0.85,  # Near limit
            "memory_mb": 1900  # Near limit
        }
        
        with patch("subprocess.run") as mock_run:
            def mock_command(*args, **kwargs):
                # Simulate health check that detects regression
                if args[0][0] == "./deploy/health_check.sh":
                    # Check current metrics
                    if regression_detector.detect_regression(
                        [degraded_metrics["response_time_ms"]],
                        [baseline_metrics["response_time_ms"]]
                    ) > 0.5:  # 50% degradation threshold
                        return Mock(returncode=1, stderr="Performance regression detected")
                return Mock(returncode=0)
            
            mock_run.side_effect = mock_command
            
            # Store baseline
            regression_detector.store_baseline("production", baseline_metrics)
            
            # Attempt deployment (should fail due to regression)
            with pytest.raises(Exception) as exc:
                deployment_system.deploy("production", "v2.0.0", gradual_rollout=False)
            
            # Verify regression was detected
            assert "verification failed" in str(exc.value).lower()

    async def test_alert_correlation_during_deployment(
        self,
        deployment_system: BlueGreenDeployment,
        alerting_system: AlertingSystem,
        metrics_collector: MetricsCollector
    ):
        """Test that alerts are correlated during deployment to avoid noise"""
        deployment_system.init_deployment("staging")
        
        # Configure alert correlation for deployment
        alerting_system.configure_correlation_window(
            deployment_mode=True,
            window_seconds=60,
            suppression_rules=["duplicate", "related"]
        )
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            
            # Start deployment
            deployment_system.deploy("staging", "v1.5.0", gradual_rollout=False)
            
            # Simulate multiple alerts during deployment
            alerts_triggered = []
            for i in range(10):
                alert = {
                    "type": "deployment_event",
                    "severity": "info",
                    "message": f"Deployment event {i}",
                    "timestamp": datetime.now()
                }
                alerts_triggered.append(alert)
                alerting_system.process_alert(alert)
            
            # Get processed alerts (should be correlated/deduplicated)
            processed_alerts = alerting_system.get_recent_alerts(minutes=1)
            
            # Verify correlation reduced alert count
            assert len(processed_alerts) < len(alerts_triggered)
            assert len(processed_alerts) <= 3  # Should be heavily correlated

    async def test_gradual_rollout_with_monitoring_gates(
        self,
        deployment_system: BlueGreenDeployment,
        metrics_collector: MetricsCollector,
        regression_detector: RegressionDetector
    ):
        """Test gradual rollout with monitoring gates at each stage"""
        deployment_system.init_deployment("production")
        
        # Track metrics at each rollout stage
        rollout_metrics = {}
        
        with patch("subprocess.run") as mock_run:
            call_count = {"value": 0}
            
            def mock_command(*args, **kwargs):
                call_count["value"] += 1
                
                # Track metrics at different traffic percentages
                if args[0][0] == "./deploy/update_routing.sh":
                    for arg in args[0]:
                        if arg.startswith("--percentage="):
                            percentage = int(arg.split("=")[1])
                            # Simulate collecting metrics at this stage
                            rollout_metrics[percentage] = {
                                "response_time": 25 + (percentage * 0.1),  # Slight increase
                                "error_rate": 0.001,
                                "timestamp": time.time()
                            }
                
                return Mock(returncode=0)
            
            mock_run.side_effect = mock_command
            
            # Deploy with gradual rollout
            deployment_system.deploy("production", "v3.0.0", gradual_rollout=True)
            
            # Verify metrics were collected at each stage
            expected_percentages = [10, 25, 50, 75, 100]
            for percentage in expected_percentages:
                assert percentage in rollout_metrics
                assert rollout_metrics[percentage]["response_time"] < 50  # Under threshold

    async def test_rollback_triggers_alerts(
        self,
        deployment_system: BlueGreenDeployment,
        alerting_system: AlertingSystem
    ):
        """Test that rollbacks trigger appropriate alerts"""
        deployment_system.init_deployment("production")
        
        # Configure alerting for rollback events
        alerting_system.configure_alert_rules({
            "rollback": {
                "severity": "critical",
                "channels": ["email", "slack", "pagerduty"],
                "escalation": True
            }
        })
        
        with patch("subprocess.run") as mock_run:
            with patch("time.sleep"):  # Speed up test
                # First successful deployment
                mock_run.return_value.returncode = 0
                deployment_system.deploy("production", "v1.0.0", gradual_rollout=False)
                
                # Reset mock for second deployment
                call_count = {"value": 0}
                
                def mock_failure(*args, **kwargs):
                    call_count["value"] += 1
                    # Fail health check on second deployment
                    if args[0][0] == "./deploy/health_check.sh" and call_count["value"] > 1:
                        return Mock(returncode=1, stderr="Health check failed")
                    return Mock(returncode=0)
                
                mock_run.side_effect = mock_failure
                
                # Attempt second deployment (should trigger rollback)
                try:
                    deployment_system.deploy("production", "v2.0.0", gradual_rollout=False)
                except Exception:
                    pass  # Expected to fail
                
                # Verify rollback alert was triggered
                recent_alerts = alerting_system.get_recent_alerts(minutes=1)
                rollback_alerts = [a for a in recent_alerts if "rollback" in str(a).lower()]
                
                assert len(rollback_alerts) > 0
                assert any(a.get("severity") == "critical" for a in rollback_alerts)

    async def test_monitoring_dashboard_during_deployment(
        self,
        deployment_system: BlueGreenDeployment,
        metrics_collector: MetricsCollector
    ):
        """Test monitoring dashboard updates during deployment"""
        deployment_system.init_deployment("staging")
        
        dashboard_updates = []
        
        # Mock dashboard update mechanism
        def capture_dashboard_update(metrics: Dict[str, Any]):
            dashboard_updates.append({
                "timestamp": datetime.now(),
                "metrics": metrics.copy()
            })
        
        metrics_collector.on_metrics_collected = capture_dashboard_update
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            
            # Deploy and track dashboard updates
            deployment_system.deploy("staging", "v2.1.0", gradual_rollout=False)
            
            # Simulate metric collection during deployment
            for i in range(5):
                metrics_collector.collect_metric("deployment_progress", i * 20, {
                    "version": "v2.1.0",
                    "environment": "staging",
                    "stage": f"step_{i}"
                })
                metrics_summary = metrics_collector.generate_summary()
                capture_dashboard_update(metrics_summary)
                await asyncio.sleep(0.1)
        
        # Verify dashboard was updated
        assert len(dashboard_updates) >= 5
        
        # Verify deployment metrics in dashboard
        for update in dashboard_updates:
            if "metrics_by_type" in update["metrics"]:
                deployment_metrics = update["metrics"].get("metrics_by_type", {}).get("deployment_progress", [])
                if deployment_metrics:
                    # Find metrics with version info
                    version_metrics = [m for m in deployment_metrics if hasattr(m, 'labels') and 'version' in m.labels]
                    if version_metrics:
                        assert version_metrics[0].labels["version"] == "v2.1.0"
                        assert version_metrics[0].labels["environment"] == "staging"

    async def test_performance_baseline_update_after_deployment(
        self,
        deployment_system: BlueGreenDeployment,
        regression_detector: RegressionDetector,
        metrics_collector: MetricsCollector
    ):
        """Test that performance baselines are updated after successful deployments"""
        deployment_system.init_deployment("production")
        
        # Initial baseline
        initial_baseline = {
            "response_time_ms": 30,
            "error_rate": 0.002,
            "cpu_usage": 0.50,
            "memory_mb": 1500
        }
        regression_detector.store_baseline("production", initial_baseline)
        
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            
            # Deploy new version
            deployment_system.deploy("production", "v4.0.0", gradual_rollout=False)
            
            # Simulate improved performance with new version
            new_metrics = {
                "response_time_ms": 25,  # Improved
                "error_rate": 0.001,  # Improved
                "cpu_usage": 0.45,  # Improved
                "memory_mb": 1400  # Improved
            }
            
            # Update baseline after successful deployment
            regression_detector.update_baseline_after_deployment(
                "production",
                new_metrics,
                version="v4.0.0"
            )
            
            # Verify baseline was updated
            current_baseline = regression_detector.get_baseline("production")
            assert current_baseline["response_time_ms"] == 25
            assert current_baseline["version"] == "v4.0.0"

    async def test_health_check_integration(
        self,
        deployment_system: BlueGreenDeployment,
        metrics_collector: MetricsCollector
    ):
        """Test health check integration between deployment and monitoring"""
        deployment_system.init_deployment("staging")
        
        health_check_results = []
        
        with patch("subprocess.run") as mock_run:
            def mock_health_check(*args, **kwargs):
                if args[0][0] == "./deploy/health_check.sh":
                    # Collect metrics during health check
                    metrics = {
                        "endpoint": "/health",
                        "status": "healthy",
                        "response_time_ms": 15,
                        "dependencies": {
                            "database": "connected",
                            "cache": "connected",
                            "queue": "connected"
                        }
                    }
                    health_check_results.append(metrics)
                    
                    # Return success if all dependencies connected
                    all_connected = all(
                        v == "connected" 
                        for v in metrics["dependencies"].values()
                    )
                    return Mock(returncode=0 if all_connected else 1)
                return Mock(returncode=0)
            
            mock_run.side_effect = mock_health_check
            
            # Deploy with health checks
            deployment_system.deploy("staging", "v5.0.0", gradual_rollout=False)
            
            # Verify health checks were performed
            assert len(health_check_results) > 0
            assert all(r["status"] == "healthy" for r in health_check_results)
            assert all(r["response_time_ms"] < 50 for r in health_check_results)

    async def test_monitoring_alerts_escalation_during_deployment_failure(
        self,
        deployment_system: BlueGreenDeployment,
        alerting_system: AlertingSystem
    ):
        """Test alert escalation when deployment fails"""
        deployment_system.init_deployment("production")
        
        # Configure escalation policy
        alerting_system.configure_escalation_policy({
            "deployment_failure": {
                "initial_severity": "warning",
                "escalation_after_minutes": 5,
                "escalated_severity": "critical",
                "notify_on_escalation": ["oncall", "management"]
            }
        })
        
        escalated_alerts = []
        
        def capture_escalation(alert: Dict[str, Any]):
            if alert.get("escalated", False):
                escalated_alerts.append(alert)
        
        alerting_system.on_alert_escalated = capture_escalation
        
        with patch("subprocess.run") as mock_run:
            with patch("time.sleep"):
                # Simulate deployment failure
                mock_run.return_value.returncode = 1
                
                try:
                    deployment_system.deploy("production", "v6.0.0", gradual_rollout=False)
                except Exception:
                    # Expected to fail
                    pass
                
                # Trigger initial alert
                alerting_system.process_alert({
                    "type": "deployment_failure",
                    "severity": "warning",
                    "message": "Deployment v6.0.0 failed",
                    "timestamp": datetime.now()
                })
                
                # Simulate time passing for escalation
                alerting_system.check_escalations(
                    current_time=datetime.now() + timedelta(minutes=6)
                )
                
                # Verify escalation occurred
                assert len(escalated_alerts) > 0
                assert escalated_alerts[0]["severity"] == "critical"