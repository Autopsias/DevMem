"""Settings loader for hierarchical Claude Code settings system."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from dataclasses import asdict

from .schema import AgentConfigurationSchema, ConfigurationValidator
from .environment_handler import EnvironmentVariableHandler

logger = logging.getLogger(__name__)

class SettingsLoader:
    """Loads and merges configuration from Claude Code's hierarchical settings system."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize settings loader."""
        self.project_root = project_root or Path.cwd()
        self.env_handler = EnvironmentVariableHandler()
        self._cached_config: Optional[AgentConfigurationSchema] = None
        self._config_timestamps: Dict[str, float] = {}
        
    def load_configuration(self) -> AgentConfigurationSchema:
        """Load complete configuration from all sources with proper hierarchy."""
        logger.info("Loading agent configuration from Claude Code settings")
        
        # Load from all configuration sources
        configs = self._load_all_configs()
        
        # Merge configurations with proper precedence
        merged_config = self._merge_configurations(configs)
        
        # Apply environment variable overrides
        merged_config = self._apply_environment_overrides(merged_config)
        
        # Validate merged configuration
        errors = ConfigurationValidator.validate_config(merged_config)
        if errors:
            logger.warning(f"Configuration validation errors: {errors}")
            # Continue with warnings but don't fail
        
        # Convert to schema object
        config_schema = self._dict_to_schema(merged_config)
        
        self._cached_config = config_schema
        logger.info("Agent configuration loaded successfully")
        return config_schema
    
    def _load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load configuration from all sources in hierarchy order."""
        configs = {}
        
        # 1. Load user-level settings (~/.claude/settings.json)
        user_config_path = Path.home() / ".claude" / "settings.json"
        configs["user"] = self._load_config_file(user_config_path, "user")
        
        # 2. Load project-level settings (.claude/settings.json)
        project_config_path = self.project_root / ".claude" / "settings.json"
        configs["project"] = self._load_config_file(project_config_path, "project")
        
        # 3. Load local settings (.claude/settings.local.json)
        local_config_path = self.project_root / ".claude" / "settings.local.json"
        configs["local"] = self._load_config_file(local_config_path, "local")
        
        return configs
    
    def _load_config_file(self, config_path: Path, config_type: str) -> Dict[str, Any]:
        """Load configuration from a specific file."""
        if not config_path.exists():
            logger.debug(f"Configuration file not found: {config_path}")
            return {}
        
        try:
            # Update timestamp cache
            self._config_timestamps[str(config_path)] = config_path.stat().st_mtime
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.debug(f"Loaded {config_type} configuration from {config_path}")
            
            # Extract agent-related configuration
            return self._extract_agent_config(config)
            
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load {config_type} configuration from {config_path}: {e}")
            return {}
    
    def _extract_agent_config(self, full_config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract agent-specific configuration from full Claude Code settings."""
        agent_config = {}
        
        # Look for agent configuration in various places
        if "agents" in full_config:
            agent_config = full_config["agents"]
        elif "agent_framework" in full_config:
            agent_config = full_config["agent_framework"]
        elif "claude_agents" in full_config:
            agent_config = full_config["claude_agents"]
        
        # Also extract performance settings if they exist
        if "performance" in full_config:
            agent_config["performance"] = full_config["performance"]
        
        # Extract monitoring settings
        if "monitoring" in full_config:
            agent_config["monitoring"] = full_config["monitoring"]
        
        return agent_config
    
    def _merge_configurations(self, configs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Merge configurations with proper precedence: local > project > user."""
        # Start with default configuration
        default_config = asdict(AgentConfigurationSchema.create_default_config())
        
        # Merge in order: user -> project -> local (later ones override)
        merged = default_config.copy()
        
        for config_level in ["user", "project", "local"]:
            config = configs.get(config_level, {})
            if config:
                merged = self._deep_merge(merged, config)
                logger.debug(f"Merged {config_level} configuration")
        
        return merged
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _apply_environment_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration."""
        env_overrides = self.env_handler.get_environment_config()
        
        if env_overrides:
            config = self._deep_merge(config, env_overrides)
            logger.info("Applied environment variable overrides")
        
        return config
    
    def _dict_to_schema(self, config_dict: Dict[str, Any]) -> AgentConfigurationSchema:
        """Convert dictionary configuration to schema object."""
        try:
            # Handle the conversion carefully since dataclasses need specific handling
            schema = AgentConfigurationSchema()
            
            # Update fields that exist
            if "version" in config_dict:
                schema.version = config_dict["version"]
            
            if "global_settings" in config_dict:
                schema.global_settings.update(config_dict["global_settings"])
            
            if "performance" in config_dict:
                schema.performance.update(config_dict["performance"])
            
            if "monitoring" in config_dict:
                schema.monitoring.update(config_dict["monitoring"])
            
            if "environment_overrides" in config_dict:
                schema.environment_overrides.update(config_dict["environment_overrides"])
            
            # Handle agents configuration (more complex due to dataclass structure)
            if "agents" in config_dict and isinstance(config_dict["agents"], dict):
                # For now, store as custom settings - full dataclass conversion can be added later
                for agent_name, agent_config in config_dict["agents"].items():
                    if agent_name in schema.agents:
                        if isinstance(agent_config, dict):
                            schema.agents[agent_name].custom_settings.update(agent_config)
            
            return schema
            
        except Exception as e:
            logger.error(f"Failed to convert configuration to schema: {e}")
            # Return default configuration on error
            return AgentConfigurationSchema.create_default_config()
    
    def is_config_changed(self) -> bool:
        """Check if any configuration file has changed since last load."""
        config_paths = [
            Path.home() / ".claude" / "settings.json",
            self.project_root / ".claude" / "settings.json", 
            self.project_root / ".claude" / "settings.local.json"
        ]
        
        for config_path in config_paths:
            if not config_path.exists():
                continue
                
            path_str = str(config_path)
            current_mtime = config_path.stat().st_mtime
            
            if path_str not in self._config_timestamps:
                return True
                
            if current_mtime != self._config_timestamps[path_str]:
                return True
        
        return False
    
    def get_cached_config(self) -> Optional[AgentConfigurationSchema]:
        """Get cached configuration if available."""
        return self._cached_config
    
    def reload_if_changed(self) -> Optional[AgentConfigurationSchema]:
        """Reload configuration if files have changed."""
        if self.is_config_changed():
            logger.info("Configuration files changed, reloading...")
            return self.load_configuration()
        
        return self._cached_config