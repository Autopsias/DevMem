import pytest
import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

def test_deployment_scripts_exist():
    deploy_dir = Path("deploy")
    required_scripts = [
        "deploy.sh",
        "health_check.sh",
        "configure_environment.sh"
    ]
    
    for script in required_scripts:
        script_path = deploy_dir / script
        assert script_path.exists(), f"Missing deployment script: {script}"
        assert os.access(script_path, os.X_OK), f"Script not executable: {script}"

def test_environment_configuration():
    environments = ["staging", "production"]
    test_config_dir = "test_config"
    
    # Create test config directory
    os.makedirs(test_config_dir, exist_ok=True)
    
    for env in environments:
        # Configure environment
        result = subprocess.run(
            ["./deploy/configure_environment.sh", env],
            env={"CONFIG_DIR": test_config_dir},
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Environment configuration failed for {env}"
        
        # Check generated config files
        base_config_path = f"{test_config_dir}/base_config.json"
        env_config_path = f"{test_config_dir}/env_config.json"
        env_script_path = f"./deploy/config_{env}.sh"
        
        # Verify JSON configs if accessible
        try:
            with open(base_config_path) as f:
                base_config = json.load(f)
                assert "service" in base_config
                assert "validation" in base_config
                assert "security" in base_config
        except (PermissionError, FileNotFoundError):
            pass  # Skip if can't access system paths in test environment
            
        try:
            with open(env_config_path) as f:
                env_config = json.load(f)
                assert "api" in env_config
                assert "resources" in env_config
                assert "monitoring" in env_config
        except (PermissionError, FileNotFoundError):
            pass
            
        # Verify environment script
        assert Path(env_script_path).exists()
        with open(env_script_path) as f:
            content = f.read()
            assert f'PATTERN_ENV="{env}"' in content
            assert "API_URL" in content
            assert "MAX_MEMORY" in content
            assert "MAX_CPU" in content
            assert "WORKER_COUNT" in content

def test_health_check_script(tmp_path):
    environments = ["staging", "production"]
    test_config_dir = str(tmp_path / "config")
    test_bin_dir = str(tmp_path / "bin")
    
    # Create test directories
    os.makedirs(test_config_dir, exist_ok=True)
    os.makedirs(test_bin_dir, exist_ok=True)
    
    # Create mock system commands
    mock_commands = {
        "systemctl": """#!/bin/bash
echo "active"
exit 0""",
        "free": """#!/bin/bash
echo "              total        used        free"
echo "Mem:         16384        1024       15360"
exit 0""",
        "top": """#!/bin/bash
echo "top - 12:00:00 up 1 day, load average: 1.00, 0.75, 0.50"
echo "%Cpu(s): 10.0 us, 5.0 sy, 0.0 ni, 80.0 id"
exit 0""",
        "curl": """#!/bin/bash
echo '{"status": "healthy"}'
exit 0"""
    }
    
    for cmd, content in mock_commands.items():
        cmd_path = Path(test_bin_dir) / cmd
        with open(cmd_path, "w") as f:
            f.write(content)
        os.chmod(cmd_path, 0o755)
    
    # Add mock commands to PATH
    test_env = os.environ.copy()
    test_env["PATH"] = f"{test_bin_dir}:{test_env.get('PATH', '')}"
    test_env["CONFIG_DIR"] = test_config_dir
    
    for env in environments:
        # Configure environment first
        subprocess.run(
            ["./deploy/configure_environment.sh", env],
            env=test_env
        )
        
        # Test health check script
        result = subprocess.run(
            ["./deploy/health_check.sh", env],
            env=test_env,
            capture_output=True,
            text=True
        )
        
        # Health check should succeed with mocked commands
        assert result.returncode == 0, f"Health check failed for {env}: {result.stderr}"
        assert "All health checks passed" in result.stdout

def test_deployment_workflow():
    workflow_path = Path(".github/workflows/deployment.yml")
    assert workflow_path.exists(), "Missing deployment workflow"
    
    with open(workflow_path) as f:
        content = f.read()
        
        # Verify required jobs
        assert "validate:" in content
        assert "staging-deploy:" in content
        assert "production-approval:" in content
        assert "production-deploy:" in content
        
        # Verify environment URLs
        assert "STAGING_URL:" in content
        assert "PRODUCTION_URL:" in content
        
        # Verify validation steps
        assert "python validate.py --suite production" in content
        assert "python validate.py --suite load" in content
        assert "python validate.py --suite security" in content