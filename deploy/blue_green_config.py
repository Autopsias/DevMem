from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Literal
from datetime import datetime
import yaml
import subprocess
import time
import logging
from pathlib import Path

@dataclass
class EnvironmentConfig:
    name: str
    url: str
    port: int
    health_endpoint: str
    resource_limits: Dict[str, Any]
    environment_vars: Dict[str, str]

@dataclass
class DeploymentTarget:
    name: str
    color: Literal["blue", "green"]
    status: Literal["active", "inactive", "deploying", "healthy", "unhealthy"]
    version: str
    deployed_at: Optional[datetime]
    health_status: Dict[str, Any]

class BlueGreenDeployment:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.environments: Dict[str, EnvironmentConfig] = {}
        self.targets: Dict[str, DeploymentTarget] = {}
        self.logger = logging.getLogger("blue_green_deployment")
        
        # Load environment configurations
        self._load_configs()
        
    def _load_configs(self) -> None:
        """Load environment configurations from yaml files"""
        for env_file in ["staging.yml", "production.yml"]:
            config_file = self.config_path / env_file
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_file}")
                
            with open(config_file) as f:
                config = yaml.safe_load(f)
                
            env_name = env_file.replace(".yml", "")
            self.environments[env_name] = EnvironmentConfig(
                name=env_name,
                url=config["api"]["url"],
                port=config.get("port", 8000),
                health_endpoint="/health",
                resource_limits=config["resources"],
                environment_vars={
                    "APP_ENV": env_name,
                    "API_URL": config["api"]["url"],
                    "MAX_MEMORY": str(config["resources"]["max_memory_mb"]),
                    "MAX_CPU": str(config["resources"]["max_cpu_percent"]),
                    "WORKER_COUNT": str(config["resources"]["worker_count"])
                }
            )
            
    def init_deployment(self, environment: str) -> None:
        """Initialize blue-green deployment for an environment"""
        if environment not in self.environments:
            raise ValueError(f"Unknown environment: {environment}")
            
        # Initialize blue and green targets
        self.targets[f"{environment}_blue"] = DeploymentTarget(
            name=f"{environment}_blue",
            color="blue",
            status="inactive",
            version="",
            deployed_at=None,
            health_status={}
        )
        
        self.targets[f"{environment}_green"] = DeploymentTarget(
            name=f"{environment}_green",
            color="green",
            status="inactive",
            version="",
            deployed_at=None,
            health_status={}
        )
        
    def deploy(
        self,
        environment: str,
        version: str,
        gradual_rollout: bool = True
    ) -> None:
        """Deploy a new version using blue-green deployment"""
        if environment not in self.environments:
            raise ValueError(f"Unknown environment: {environment}")
            
        # Get current active and inactive targets
        active_target = self._get_active_target(environment)
        inactive_color = "green" if active_target and active_target.color == "blue" else "blue"
        target_name = f"{environment}_{inactive_color}"
        
        # Update target status
        self.targets[target_name].status = "deploying"
        self.targets[target_name].version = version
        self.targets[target_name].deployed_at = datetime.now()
        
        try:
            # Deploy to inactive target
            self._deploy_target(environment, target_name, version)
            
            # Verify deployment
            if not self._verify_deployment(environment, target_name):
                raise Exception("Deployment verification failed")
                
            # Update target status
            self.targets[target_name].status = "healthy"
            
            if gradual_rollout:
                # Gradually shift traffic
                self._gradual_traffic_shift(environment, target_name)
            else:
                # Immediate cutover
                self._cutover_traffic(environment, target_name)
                
            # Update statuses
            if active_target:
                active_target.status = "inactive"
            self.targets[target_name].status = "active"
            
        except Exception as e:
            # Rollback on failure
            self.logger.error(f"Deployment failed: {str(e)}")
            self.targets[target_name].status = "unhealthy"
            self._rollback(environment)
            raise
            
    def _deploy_target(self, environment: str, target_name: str, version: str) -> None:
        """Deploy application to a specific target"""
        env_config = self.environments[environment]
        target = self.targets[target_name]
        
        # Prepare deployment
        deploy_cmd = [
            "./deploy/deploy.sh",
            environment,
            f"--target={target.color}",
            f"--version={version}"
        ]
        
        # Add environment variables
        for key, value in env_config.environment_vars.items():
            deploy_cmd.extend(["-e", f"{key}={value}"])
            
        # Execute deployment
        result = subprocess.run(deploy_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Deployment failed: {result.stderr}")
            
    def _verify_deployment(self, environment: str, target_name: str) -> bool:
        """Verify deployment health"""
        env_config = self.environments[environment]
        target = self.targets[target_name]
        
        # Run health checks
        health_cmd = [
            "./deploy/health_check.sh",
            environment,
            f"--target={target.color}"
        ]
        
        max_retries = 5
        retry_delay = 10
        
        for attempt in range(max_retries):
            result = subprocess.run(health_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return True
                
            if attempt < max_retries - 1:
                self.logger.warning(
                    f"Health check failed, attempt {attempt + 1}/{max_retries}. "
                    f"Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)
                
        return False
        
    def _gradual_traffic_shift(self, environment: str, target_name: str) -> None:
        """Gradually shift traffic to new target"""
        traffic_percentages = [10, 25, 50, 75, 100]
        check_duration = 60  # seconds between percentage increases
        
        for percentage in traffic_percentages:
            # Update traffic routing
            self._update_traffic_routing(environment, target_name, percentage)
            
            # Skip monitoring during tests
            if hasattr(self, '_skip_monitoring') and self._skip_monitoring:
                continue
                
            # Monitor health during transition
            start_time = time.time()
            while time.time() - start_time < check_duration:
                if not self._verify_deployment(environment, target_name):
                    raise Exception(
                        f"Health check failed at {percentage}% traffic"
                    )
                time.sleep(10)
                
    def _update_traffic_routing(
        self,
        environment: str,
        target_name: str,
        percentage: int
    ) -> None:
        """Update traffic routing configuration"""
        update_cmd = [
            "./deploy/update_routing.sh",
            environment,
            f"--target={self.targets[target_name].color}",
            f"--percentage={percentage}"
        ]
        
        result = subprocess.run(update_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to update traffic routing: {result.stderr}")
            
    def _cutover_traffic(self, environment: str, target_name: str) -> None:
        """Immediately cutover all traffic to new target"""
        self._update_traffic_routing(environment, target_name, 100)
        
    def _rollback(self, environment: str) -> None:
        """Rollback to previous deployment"""
        active_target = self._get_active_target(environment)
        if not active_target:
            self.logger.warning("No active target to rollback to")
            return
            
        # Restore traffic to active target
        self._update_traffic_routing(environment, active_target.name, 100)
        
    def _get_active_target(self, environment: str) -> Optional[DeploymentTarget]:
        """Get currently active deployment target"""
        for target in self.targets.values():
            if target.name.startswith(environment) and target.status == "active":
                return target
        return None
        
    def get_deployment_status(self, environment: str) -> Dict[str, Any]:
        """Get current deployment status"""
        status = {
            "environment": environment,
            "targets": {}
        }
        
        for target in self.targets.values():
            if target.name.startswith(environment):
                status["targets"][target.color] = {
                    "status": target.status,
                    "version": target.version,
                    "deployed_at": target.deployed_at,
                    "health_status": target.health_status
                }
                
        return status