from typing import Dict, Any, Optional
import yaml
from pathlib import Path


class EnvironmentManager:
    """Manages environment-specific configurations"""
    
    def __init__(self, config_path: str = "config"):
        self.config_path = Path(config_path)
        self.environments = {}
        self._load_environments()
    
    def _load_environments(self) -> None:
        """Load all environment configurations"""
        for env_file in self.config_path.glob("*.yml"):
            if env_file.stem in ["staging", "production", "dev"]:
                with open(env_file) as f:
                    self.environments[env_file.stem] = yaml.safe_load(f)
    
    def get_config(self, environment: str) -> Dict[str, Any]:
        """Get configuration for a specific environment"""
        if environment not in self.environments:
            raise ValueError(f"Unknown environment: {environment}")
        return self.environments[environment]
    
    def update_config(self, environment: str, config: Dict[str, Any]) -> None:
        """Update configuration for an environment"""
        self.environments[environment] = config
        
        # Persist to file
        config_file = self.config_path / f"{environment}.yml"
        with open(config_file, "w") as f:
            yaml.dump(config, f)
    
    def validate_config(self, environment: str) -> bool:
        """Validate environment configuration"""
        if environment not in self.environments:
            return False
        
        config = self.environments[environment]
        
        # Check required fields
        required_fields = ["api", "resources"]
        for field in required_fields:
            if field not in config:
                return False
        
        # Validate resource limits
        resources = config.get("resources", {})
        if resources.get("max_memory_mb", 0) <= 0:
            return False
        if resources.get("max_cpu_percent", 0) <= 0:
            return False
        
        return True
    
    def get_resource_limits(self, environment: str) -> Dict[str, int]:
        """Get resource limits for an environment"""
        config = self.get_config(environment)
        return config.get("resources", {})
    
    def sync_environments(self) -> Dict[str, bool]:
        """Synchronize configurations across environments"""
        sync_status = {}
        
        # Ensure all environments have consistent structure
        base_structure = set()
        for env, config in self.environments.items():
            base_structure.update(config.keys())
        
        for env in self.environments:
            missing_keys = base_structure - set(self.environments[env].keys())
            if missing_keys:
                sync_status[env] = False
            else:
                sync_status[env] = True
        
        return sync_status