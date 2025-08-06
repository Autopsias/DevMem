"""Configuration management for Claude Code agent ecosystem."""

from .settings_loader import SettingsLoader
from .schema import AgentConfigurationSchema, ConfigurationValidator
from .environment_handler import EnvironmentVariableHandler
from .hot_reload import HotReloadManager, ConfigurationManager
from .defaults import DefaultConfigurationProvider
from .profiles import ConfigurationProfileManager, ConfigurationProfile
from .adaptive import AdaptiveConfigurationManager, MetricType
from .monitoring import ConfigurationMonitor
from .validation import ValidationIssue, ValidationSeverity
from .error_handling import ConfigurationErrorHandler

__all__ = [
    # Core configuration
    "SettingsLoader",
    "AgentConfigurationSchema",
    "ConfigurationValidator",
    "EnvironmentVariableHandler",
    "HotReloadManager",
    "ConfigurationManager",
    
    # Defaults and profiles
    "DefaultConfigurationProvider",
    "ConfigurationProfileManager",
    "ConfigurationProfile",
    
    # Dynamic and adaptive features
    "AdaptiveConfigurationManager",
    "MetricType",
    "ConfigurationMonitor",
    
    # Validation and error handling
    "ValidationIssue",
    "ValidationSeverity",
    "ConfigurationErrorHandler"
]