"""Settings override hierarchy system for Claude Code configuration."""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class ConfigurationLevel(Enum):
    """Configuration hierarchy levels in override precedence order."""
    DEFAULT = 0
    USER = 1
    PROJECT = 2
    LOCAL = 3
    ENVIRONMENT = 4
    
    @classmethod
    def get_override_order(cls) -> List['ConfigurationLevel']:
        """Get configuration levels in override order (lowest to highest precedence)."""
        return [cls.DEFAULT, cls.USER, cls.PROJECT, cls.LOCAL, cls.ENVIRONMENT]

@dataclass
class ConfigurationSource:
    """Represents a configuration source with metadata."""
    level: ConfigurationLevel
    data: Dict[str, Any]
    source_path: Optional[str] = None
    loaded_at: Optional[str] = None
    
class HierarchicalConfigurationManager:
    """Manages hierarchical configuration with proper override precedence."""
    
    def __init__(self):
        """Initialize hierarchical configuration manager."""
        self._sources: Dict[ConfigurationLevel, ConfigurationSource] = {}
        self._merged_cache: Optional[Dict[str, Any]] = None
        self._cache_valid = False
    
    def add_configuration_source(self, level: ConfigurationLevel, data: Dict[str, Any], 
                                source_path: Optional[str] = None) -> None:
        """Add configuration source at specific hierarchy level."""
        self._sources[level] = ConfigurationSource(
            level=level,
            data=data,
            source_path=source_path
        )
        self._invalidate_cache()
        logger.debug(f"Added configuration source at level {level.name}")
    
    def remove_configuration_source(self, level: ConfigurationLevel) -> None:
        """Remove configuration source at specific level."""
        if level in self._sources:
            del self._sources[level]
            self._invalidate_cache()
            logger.debug(f"Removed configuration source at level {level.name}")
    
    def get_merged_configuration(self) -> Dict[str, Any]:
        """Get merged configuration with proper hierarchy precedence."""
        if not self._cache_valid or self._merged_cache is None:
            self._merged_cache = self._merge_configurations()
            self._cache_valid = True
        
        return self._merged_cache.copy()
    
    def _merge_configurations(self) -> Dict[str, Any]:
        """Merge all configuration sources with proper precedence."""
        merged = {}
        
        # Process in override order (lowest to highest precedence)
        for level in ConfigurationLevel.get_override_order():
            if level in self._sources:
                source = self._sources[level]
                merged = self._deep_merge(merged, source.data)
                logger.debug(f"Merged configuration from level {level.name}")
        
        return merged
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries with override precedence."""
        result = base.copy()
        
        for key, value in override.items():
            if (key in result and 
                isinstance(result[key], dict) and 
                isinstance(value, dict)):
                # Recursively merge nested dictionaries
                result[key] = self._deep_merge(result[key], value)
            else:
                # Override with new value
                result[key] = value
        
        return result
    
    def _invalidate_cache(self) -> None:
        """Invalidate the merged configuration cache."""
        self._cache_valid = False
        self._merged_cache = None
    
    def get_configuration_sources(self) -> Dict[ConfigurationLevel, ConfigurationSource]:
        """Get all configuration sources."""
        return self._sources.copy()
    
    def get_configuration_trace(self, key_path: str) -> List[Dict[str, Any]]:
        """Trace the source of a specific configuration key through the hierarchy."""
        trace = []
        key_parts = key_path.split('.')
        
        for level in ConfigurationLevel.get_override_order():
            if level not in self._sources:
                continue
                
            source = self._sources[level]
            value = self._get_nested_value(source.data, key_parts)
            
            if value is not None:
                trace.append({
                    "level": level.name,
                    "value": value,
                    "source_path": source.source_path,
                    "overridden": False  # Will be updated below
                })
        
        # Mark all but the last as overridden
        for item in trace[:-1]:
            item["overridden"] = True
        
        return trace
    
    def _get_nested_value(self, data: Dict[str, Any], key_parts: List[str]) -> Any:
        """Get nested value from dictionary using key parts."""
        current = data
        
        for part in key_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current
    
    def validate_hierarchy(self) -> List[str]:
        """Validate the configuration hierarchy for consistency."""
        warnings = []
        
        # Check for common configuration conflicts
        merged = self.get_merged_configuration()
        
        # Validate agent consistency
        if "agents" in merged:
            for agent_name, agent_config in merged["agents"].items():
                if isinstance(agent_config, dict):
                    # Check for conflicting settings
                    if agent_config.get("enabled", True) is False:
                        if "performance" in agent_config or "coordination" in agent_config:
                            warnings.append(
                                f"Agent '{agent_name}' is disabled but has performance/coordination settings"
                            )
        
        # Validate global vs agent-specific conflicts
        global_settings = merged.get("global_settings", {})
        if global_settings.get("framework_enabled", True) is False:
            if any(agent.get("enabled", True) for agent in merged.get("agents", {}).values() 
                   if isinstance(agent, dict)):
                warnings.append(
                    "Framework is disabled globally but some agents are explicitly enabled"
                )
        
        return warnings
    
    def export_hierarchy_report(self) -> Dict[str, Any]:
        """Export detailed hierarchy report for debugging."""
        report = {
            "hierarchy_levels": [level.name for level in ConfigurationLevel.get_override_order()],
            "active_sources": {},
            "merged_configuration": self.get_merged_configuration(),
            "validation_warnings": self.validate_hierarchy()
        }
        
        for level, source in self._sources.items():
            report["active_sources"][level.name] = {
                "source_path": source.source_path,
                "data_keys": list(source.data.keys()) if isinstance(source.data, dict) else None,
                "data_size": len(str(source.data))
            }
        
        return report