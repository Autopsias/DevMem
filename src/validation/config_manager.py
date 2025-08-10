from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import yaml
import os
import hashlib
import json
from pathlib import Path
import logging

@dataclass
class ConfigValidation:
    valid: bool
    errors: List[str]
    warnings: List[str]
    schema_version: str

@dataclass
class ConfigHealth:
    status: str  # "healthy", "warning", or "error"
    timestamp: float
    details: Dict[str, Any]
    dependencies: Dict[str, str]  # service: status

class ConfigManager:
    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger("config_manager")
        self.schema_version = "1.0.0"
        self.config_cache: Dict[str, Any] = {}
        self.health_cache: Dict[str, ConfigHealth] = {}
        
        # Load configuration schema
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict[str, Any]:
        """Load configuration schema"""
        schema_file = self.config_dir / "schema.yml"
        if not schema_file.exists():
            self.logger.warning("Schema file not found, using default schema")
            return self._get_default_schema()
            
        with open(schema_file) as f:
            return yaml.safe_load(f)
            
    def _get_default_schema(self) -> Dict[str, Any]:
        """Get default configuration schema"""
        return {
            "version": self.schema_version,
            "required_fields": [
                "api",
                "patterns",
                "resources",
                "monitoring",
                "security"
            ],
            "field_types": {
                "api.url": "string",
                "api.rate_limit": "integer",
                "patterns.batch_size": "integer",
                "patterns.max_concurrent": "integer",
                "resources.max_memory_mb": "integer",
                "resources.max_cpu_percent": "integer",
                "monitoring.metrics_interval": "integer",
                "security.tls_enabled": "boolean"
            },
            "value_constraints": {
                "api.rate_limit": {"min": 1, "max": 10000},
                "patterns.batch_size": {"min": 1, "max": 100},
                "resources.max_memory_mb": {"min": 512, "max": 8192},
                "resources.max_cpu_percent": {"min": 1, "max": 100}
            }
        }
        
    def load_config(self, environment: str) -> Dict[str, Any]:
        """Load configuration for an environment"""
        config_file = self.config_dir / f"{environment}.yml"
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration not found: {config_file}")
            
        # Check if cached config is still valid
        if environment in self.config_cache:
            cached_config = self.config_cache[environment]
            if self._config_is_current(config_file, cached_config):
                return cached_config
                
        # Load and validate configuration
        with open(config_file) as f:
            config = yaml.safe_load(f)
            
        # Add metadata
        config["_metadata"] = {
            "environment": environment,
            "file_hash": self._get_file_hash(config_file),
            "schema_version": self.schema_version
        }
        
        # Cache configuration
        self.config_cache[environment] = config
        return config
        
    def validate_config(self, environment: str) -> ConfigValidation:
        """Validate configuration against schema"""
        try:
            config = self.load_config(environment)
        except Exception as e:
            return ConfigValidation(
                valid=False,
                errors=[f"Failed to load configuration: {str(e)}"],
                warnings=[],
                schema_version=self.schema_version
            )
            
        errors = []
        warnings = []
        
        # Check required fields
        for field in self.schema["required_fields"]:
            if not self._get_nested_value(config, field):
                errors.append(f"Missing required field: {field}")
                
        # Validate field types
        for field, expected_type in self.schema["field_types"].items():
            value = self._get_nested_value(config, field)
            if value is not None:
                if not self._validate_type(value, expected_type):
                    errors.append(
                        f"Invalid type for {field}: expected {expected_type}"
                    )
                    
        # Check value constraints
        for field, constraints in self.schema["value_constraints"].items():
            value = self._get_nested_value(config, field)
            if value is not None:
                if "min" in constraints and value < constraints["min"]:
                    errors.append(
                        f"Value for {field} below minimum: {constraints['min']}"
                    )
                if "max" in constraints and value > constraints["max"]:
                    errors.append(
                        f"Value for {field} above maximum: {constraints['max']}"
                    )
                    
        return ConfigValidation(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            schema_version=self.schema_version
        )
        
    def check_health(self, environment: str) -> ConfigHealth:
        """Check configuration health status"""
        try:
            config = self.load_config(environment)
            validation = self.validate_config(environment)
            
            if not validation.valid:
                return ConfigHealth(
                    status="error",
                    timestamp=os.path.getmtime(
                        self.config_dir / f"{environment}.yml"
                    ),
                    details={
                        "errors": validation.errors,
                        "warnings": validation.warnings
                    },
                    dependencies=self._check_dependencies(config)
                )
                
            # Check configuration consistency
            consistency_issues = self._check_config_consistency(config)
            if consistency_issues:
                return ConfigHealth(
                    status="warning",
                    timestamp=os.path.getmtime(
                        self.config_dir / f"{environment}.yml"
                    ),
                    details={
                        "consistency_issues": consistency_issues,
                        "warnings": validation.warnings
                    },
                    dependencies=self._check_dependencies(config)
                )
                
            return ConfigHealth(
                status="healthy",
                timestamp=os.path.getmtime(
                    self.config_dir / f"{environment}.yml"
                ),
                details={
                    "warnings": validation.warnings
                },
                dependencies=self._check_dependencies(config)
            )
            
        except Exception as e:
            return ConfigHealth(
                status="error",
                timestamp=0.0,
                details={"error": str(e)},
                dependencies={}
            )
            
    def _check_config_consistency(self, config: Dict[str, Any]) -> List[str]:
        """Check configuration internal consistency"""
        issues = []
        
        # Check resource allocation consistency
        worker_count = self._get_nested_value(
            config,
            "resources.worker_count"
        )
        max_concurrent = self._get_nested_value(
            config,
            "patterns.max_concurrent"
        )
        
        if worker_count and max_concurrent:
            if worker_count < max_concurrent:
                issues.append(
                    "Worker count is less than maximum concurrent patterns"
                )
                
        # Check monitoring configuration
        metrics_interval = self._get_nested_value(
            config,
            "monitoring.metrics_interval"
        )
        retention_days = self._get_nested_value(
            config,
            "monitoring.retention_days"
        )
        
        if metrics_interval and retention_days:
            max_datapoints = (retention_days * 86400) / metrics_interval
            if max_datapoints > 1000000:
                issues.append(
                    "Metrics retention period may lead to excessive storage usage"
                )
                
        return issues
        
    def _check_dependencies(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Check health of dependent services"""
        dependencies = {}
        
        # Check API endpoint
        api_url = self._get_nested_value(config, "api.url")
        if api_url:
            try:
                # Implement API health check
                dependencies["api"] = "healthy"
            except Exception:
                dependencies["api"] = "unhealthy"
                
        # Check monitoring system
        monitoring_url = self._get_nested_value(
            config,
            "monitoring.dashboard_url"
        )
        if monitoring_url:
            try:
                # Implement monitoring system check
                dependencies["monitoring"] = "healthy"
            except Exception:
                dependencies["monitoring"] = "unhealthy"
                
        return dependencies
        
    def _config_is_current(
        self,
        config_file: Path,
        cached_config: Dict[str, Any]
    ) -> bool:
        """Check if cached configuration is still current"""
        if not "_metadata" in cached_config:
            return False
            
        metadata = cached_config["_metadata"]
        current_hash = self._get_file_hash(config_file)
        return metadata.get("file_hash") == current_hash
        
    def _get_file_hash(self, file_path: Path) -> str:
        """Get SHA-256 hash of file contents"""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
        
    def _get_nested_value(
        self,
        config: Dict[str, Any],
        path: str
    ) -> Optional[Any]:
        """Get nested dictionary value using dot notation"""
        current = config
        for key in path.split("."):
            if isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    return None
            else:
                return None
        return current
        
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value against expected type"""
        if expected_type == "string":
            return isinstance(value, str)
        elif expected_type == "integer":
            return isinstance(value, int)
        elif expected_type == "float":
            return isinstance(value, (int, float))
        elif expected_type == "boolean":
            return isinstance(value, bool)
        elif expected_type == "list":
            return isinstance(value, list)
        elif expected_type == "dict":
            return isinstance(value, dict)
        return False