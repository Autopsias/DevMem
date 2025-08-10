import pytest
import yaml
from pathlib import Path
import time
from typing import Dict, Any

from src.validation.config_manager import ConfigManager, ConfigValidation, ConfigHealth

@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    """Create temporary configuration directory with test configs"""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Create schema file
    schema = {
        "version": "1.0.0",
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
    
    with open(config_dir / "schema.yml", "w") as f:
        yaml.dump(schema, f)
        
    return config_dir

@pytest.fixture
def valid_config() -> Dict[str, Any]:
    """Create valid test configuration"""
    return {
        "api": {
            "url": "https://test.example.com",
            "rate_limit": 1000
        },
        "patterns": {
            "batch_size": 25,
            "max_concurrent": 10
        },
        "resources": {
            "max_memory_mb": 1024,
            "max_cpu_percent": 70,
            "worker_count": 10
        },
        "monitoring": {
            "metrics_interval": 60,
            "retention_days": 30,
            "dashboard_url": "https://metrics.example.com"
        },
        "security": {
            "tls_enabled": True,
            "min_tls_version": "1.2"
        }
    }

def test_load_config(config_dir: Path, valid_config: Dict[str, Any]):
    """Test configuration loading"""
    # Create test config file
    with open(config_dir / "staging.yml", "w") as f:
        yaml.dump(valid_config, f)
        
    manager = ConfigManager(str(config_dir))
    loaded_config = manager.load_config("staging")
    
    assert loaded_config["api"]["url"] == valid_config["api"]["url"]
    assert loaded_config["patterns"]["batch_size"] == valid_config["patterns"]["batch_size"]
    assert loaded_config["_metadata"]["environment"] == "staging"
    assert loaded_config["_metadata"]["schema_version"] == "1.0.0"

def test_config_validation(config_dir: Path, valid_config: Dict[str, Any]):
    """Test configuration validation"""
    # Create test config file
    with open(config_dir / "staging.yml", "w") as f:
        yaml.dump(valid_config, f)
        
    manager = ConfigManager(str(config_dir))
    validation = manager.validate_config("staging")
    
    assert validation.valid
    assert not validation.errors
    assert not validation.warnings
    assert validation.schema_version == "1.0.0"

def test_invalid_config(config_dir: Path, valid_config: Dict[str, Any]):
    """Test validation of invalid configuration"""
    # Remove required field
    del valid_config["security"]
    
    # Add invalid value
    valid_config["resources"]["max_memory_mb"] = 9000  # Above max
    
    with open(config_dir / "staging.yml", "w") as f:
        yaml.dump(valid_config, f)
        
    manager = ConfigManager(str(config_dir))
    validation = manager.validate_config("staging")
    
    assert not validation.valid
    assert len(validation.errors) == 2
    assert any("Missing required field: security" in e for e in validation.errors)
    assert any("above maximum" in e for e in validation.errors)

def test_config_consistency(config_dir: Path, valid_config: Dict[str, Any]):
    """Test configuration consistency checks"""
    # Create inconsistent config
    valid_config["resources"]["worker_count"] = 5
    valid_config["patterns"]["max_concurrent"] = 10
    
    with open(config_dir / "staging.yml", "w") as f:
        yaml.dump(valid_config, f)
        
    manager = ConfigManager(str(config_dir))
    health = manager.check_health("staging")
    
    assert health.status == "warning"
    assert any(
        "Worker count is less than maximum concurrent patterns"
        in issue
        for issue in health.details.get("consistency_issues", [])
    )

def test_config_caching(config_dir: Path, valid_config: Dict[str, Any]):
    """Test configuration caching"""
    config_file = config_dir / "staging.yml"
    
    # Create initial config
    with open(config_file, "w") as f:
        yaml.dump(valid_config, f)
        
    manager = ConfigManager(str(config_dir))
    
    # Load config twice
    first_load = manager.load_config("staging")
    second_load = manager.load_config("staging")
    
    # Should use cached version (same object)
    assert id(first_load) == id(second_load)
    
    # Modify config file
    valid_config["api"]["rate_limit"] = 2000
    time.sleep(0.1)  # Ensure file timestamp changes
    with open(config_file, "w") as f:
        yaml.dump(valid_config, f)
        
    # Load again - should get new version
    updated_load = manager.load_config("staging")
    assert updated_load["api"]["rate_limit"] == 2000
    assert id(updated_load) != id(first_load)

def test_health_check(config_dir: Path, valid_config: Dict[str, Any]):
    """Test configuration health check"""
    with open(config_dir / "staging.yml", "w") as f:
        yaml.dump(valid_config, f)
        
    manager = ConfigManager(str(config_dir))
    health = manager.check_health("staging")
    
    assert health.status == "healthy"
    assert isinstance(health.timestamp, float)
    assert "warnings" in health.details
    assert "api" in health.dependencies
    assert "monitoring" in health.dependencies