import pytest
from datetime import datetime
from unittest.mock import Mock, patch, call
import subprocess
import time
from pathlib import Path
import yaml

from deploy.blue_green_config import BlueGreenDeployment, DeploymentTarget

@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    """Create temporary configuration directory with test configs"""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Create test configs
    staging_config = {
        "api": {
            "url": "https://test-staging.example.com",
            "rate_limit": 1000
        },
        "resources": {
            "max_memory_mb": 1500,
            "max_cpu_percent": 70,
            "worker_count": 10
        }
    }
    
    production_config = {
        "api": {
            "url": "https://test.example.com",
            "rate_limit": 5000
        },
        "resources": {
            "max_memory_mb": 4000,
            "max_cpu_percent": 80,
            "worker_count": 25
        }
    }
    
    with open(config_dir / "staging.yml", "w") as f:
        yaml.dump(staging_config, f)
        
    with open(config_dir / "production.yml", "w") as f:
        yaml.dump(production_config, f)
        
    return config_dir

@pytest.fixture
def deployment(config_dir: Path) -> BlueGreenDeployment:
    """Create BlueGreenDeployment instance with test configuration"""
    deployment = BlueGreenDeployment(str(config_dir))
    return deployment

def test_initialization(deployment: BlueGreenDeployment):
    """Test deployment initialization"""
    # Verify environments loaded
    assert "staging" in deployment.environments
    assert "production" in deployment.environments
    
    # Verify environment configurations
    staging = deployment.environments["staging"]
    assert staging.url == "https://test-staging.example.com"
    assert staging.resource_limits["max_memory_mb"] == 1500
    
    production = deployment.environments["production"]
    assert production.url == "https://test.example.com"
    assert production.resource_limits["max_memory_mb"] == 4000

def test_init_deployment(deployment: BlueGreenDeployment):
    """Test deployment target initialization"""
    deployment.init_deployment("staging")
    
    # Verify both targets created
    assert "staging_blue" in deployment.targets
    assert "staging_green" in deployment.targets
    
    # Verify target properties
    blue = deployment.targets["staging_blue"]
    assert blue.color == "blue"
    assert blue.status == "inactive"
    assert not blue.version
    assert not blue.deployed_at
    
    green = deployment.targets["staging_green"]
    assert green.color == "green"
    assert green.status == "inactive"
    assert not green.version
    assert not green.deployed_at

@patch("subprocess.run")
def test_successful_deployment(
    mock_run: Mock,
    deployment: BlueGreenDeployment
):
    """Test successful deployment process"""
    # Mock successful command execution
    mock_run.return_value.returncode = 0
    
    # Initialize deployment
    deployment.init_deployment("staging")
    
    # Deploy new version
    deployment.deploy("staging", "v1.0.0", gradual_rollout=False)
    
    # Verify deployment commands
    deploy_call = mock_run.call_args_list[0]
    assert deploy_call.args[0][0] == "./deploy/deploy.sh"
    assert "staging" in deploy_call.args[0]
    assert "--target=blue" in deploy_call.args[0]
    assert "--version=v1.0.0" in deploy_call.args[0]
    
    # Verify health check called
    health_call = mock_run.call_args_list[1]
    assert health_call.args[0][0] == "./deploy/health_check.sh"
    assert "staging" in health_call.args[0]
    assert "--target=blue" in health_call.args[0]
    
    # Verify traffic routing update
    routing_call = mock_run.call_args_list[2]
    assert routing_call.args[0][0] == "./deploy/update_routing.sh"
    assert "--percentage=100" in routing_call.args[0]
    
    # Verify target status
    blue_target = deployment.targets["staging_blue"]
    assert blue_target.status == "active"
    assert blue_target.version == "v1.0.0"
    assert isinstance(blue_target.deployed_at, datetime)

@patch("subprocess.run")
def test_gradual_rollout(
    mock_run: Mock,
    deployment: BlueGreenDeployment
):
    """Test gradual traffic rollout"""
    # Mock successful command execution
    mock_run.return_value.returncode = 0
    
    # Skip monitoring delays in test
    deployment._skip_monitoring = True
    
    # Initialize deployment
    deployment.init_deployment("staging")
    
    # Deploy with gradual rollout
    deployment.deploy("staging", "v1.0.0", gradual_rollout=True)
    
    # Verify traffic routing updates
    routing_calls = [
        call for call in mock_run.call_args_list
        if call.args[0][0] == "./deploy/update_routing.sh"
    ]
    
    # Should have 5 traffic updates (10%, 25%, 50%, 75%, 100%)
    assert len(routing_calls) == 5
    
    percentages = [10, 25, 50, 75, 100]
    for call, expected_percent in zip(routing_calls, percentages):
        assert f"--percentage={expected_percent}" in call.args[0]

@patch("time.sleep")
@patch("subprocess.run")
def test_deployment_failure(
    mock_run: Mock,
    mock_sleep: Mock,
    deployment: BlueGreenDeployment
):
    """Test deployment failure and rollback"""
    # Mock sleep to speed up test
    mock_sleep.return_value = None
    
    # Track call counts by deployment
    call_counts = {'health_checks': 0, 'current_deployment': 1}
    
    # Mock successful first deployment, failed second
    def mock_command(*args, **kwargs):
        if args[0][0] == "./deploy/health_check.sh":
            call_counts['health_checks'] += 1
            # First deployment health check succeeds
            if call_counts['current_deployment'] == 1:
                if call_counts['health_checks'] == 1:
                    call_counts['current_deployment'] = 2
                    return Mock(returncode=0)
            # Second deployment health checks all fail
            return Mock(returncode=1, stderr="Health check failed")
        return Mock(returncode=0)
        
    mock_run.side_effect = mock_command
    
    # Initialize deployment
    deployment.init_deployment("staging")
    
    # Deploy initial version successfully
    deployment.deploy("staging", "v1.0.0", gradual_rollout=False)
    
    # Attempt to deploy new version (should fail)
    with pytest.raises(Exception) as exc:
        deployment.deploy("staging", "v1.0.1", gradual_rollout=False)
    assert "Deployment verification failed" in str(exc.value)
    
    # Verify rollback occurred
    routing_calls = [
        call for call in mock_run.call_args_list
        if call.args[0][0] == "./deploy/update_routing.sh"
    ]
    last_routing = routing_calls[-1]
    assert "--target=blue" in last_routing.args[0]
    assert "--percentage=100" in last_routing.args[0]
    
    # Verify target status
    blue_target = deployment.targets["staging_blue"]
    assert blue_target.status == "active"
    assert blue_target.version == "v1.0.0"
    
    green_target = deployment.targets["staging_green"]
    assert green_target.status == "unhealthy"

def test_deployment_status(deployment: BlueGreenDeployment):
    """Test deployment status reporting"""
    # Initialize deployment
    deployment.init_deployment("staging")
    
    # Set up test state
    blue_target = deployment.targets["staging_blue"]
    blue_target.status = "active"
    blue_target.version = "v1.0.0"
    blue_target.deployed_at = datetime.now()
    blue_target.health_status = {"status": "healthy"}
    
    green_target = deployment.targets["staging_green"]
    green_target.status = "inactive"
    green_target.version = "v0.9.0"
    green_target.deployed_at = datetime.now()
    green_target.health_status = {"status": "inactive"}
    
    # Get status
    status = deployment.get_deployment_status("staging")
    
    # Verify status structure
    assert status["environment"] == "staging"
    assert "blue" in status["targets"]
    assert "green" in status["targets"]
    
    # Verify blue target status
    blue_status = status["targets"]["blue"]
    assert blue_status["status"] == "active"
    assert blue_status["version"] == "v1.0.0"
    assert isinstance(blue_status["deployed_at"], datetime)
    assert blue_status["health_status"] == {"status": "healthy"}
    
    # Verify green target status
    green_status = status["targets"]["green"]
    assert green_status["status"] == "inactive"
    assert green_status["version"] == "v0.9.0"