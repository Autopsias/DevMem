"""Hot-reload capability for Claude Code configuration changes."""

import threading
from typing import Callable, Optional, Dict, Any
from pathlib import Path
import logging
from datetime import datetime

from .settings_loader import SettingsLoader
from .schema import AgentConfigurationSchema

logger = logging.getLogger(__name__)

class HotReloadManager:
    """Manages hot-reload capability for agent configuration changes."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize hot reload manager."""
        self.project_root = project_root or Path.cwd()
        self.settings_loader = SettingsLoader(project_root)
        self._callbacks: Dict[str, Callable[[AgentConfigurationSchema], None]] = {}
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()
        self._monitor_interval = 2.0  # Check every 2 seconds
        self._last_reload_time: Optional[datetime] = None
        
    def register_callback(self, name: str, callback: Callable[[AgentConfigurationSchema], None]) -> None:
        """Register callback to be called when configuration changes."""
        self._callbacks[name] = callback
        logger.debug(f"Registered configuration callback: {name}")
    
    def unregister_callback(self, name: str) -> None:
        """Unregister a configuration callback."""
        if name in self._callbacks:
            del self._callbacks[name]
            logger.debug(f"Unregistered configuration callback: {name}")
    
    def start_monitoring(self) -> None:
        """Start monitoring configuration files for changes."""
        if self._monitor_thread and self._monitor_thread.is_alive():
            logger.warning("Hot reload monitoring is already running")
            return
        
        self._stop_monitoring.clear()
        self._monitor_thread = threading.Thread(
            target=self._monitor_config_changes,
            daemon=True,
            name="ConfigHotReload"
        )
        self._monitor_thread.start()
        logger.info("Started hot reload monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring configuration files."""
        if not self._monitor_thread:
            return
        
        self._stop_monitoring.set()
        self._monitor_thread.join(timeout=5.0)
        
        if self._monitor_thread.is_alive():
            logger.warning("Hot reload monitoring thread did not stop cleanly")
        else:
            logger.info("Stopped hot reload monitoring")
        
        self._monitor_thread = None
    
    def _monitor_config_changes(self) -> None:
        """Monitor configuration files for changes in background thread."""
        logger.debug("Hot reload monitoring started")
        
        while not self._stop_monitoring.wait(self._monitor_interval):
            try:
                if self.settings_loader.is_config_changed():
                    self._handle_config_change()
            except Exception as e:
                logger.error(f"Error during configuration monitoring: {e}")
    
    def _handle_config_change(self) -> None:
        """Handle detected configuration change."""
        try:
            logger.info("Configuration change detected, reloading...")
            
            # Reload configuration
            new_config = self.settings_loader.load_configuration()
            self._last_reload_time = datetime.now()
            
            # Notify all registered callbacks
            for callback_name, callback in self._callbacks.items():
                try:
                    callback(new_config)
                    logger.debug(f"Notified callback '{callback_name}' of configuration change")
                except Exception as e:
                    logger.error(f"Error in configuration callback '{callback_name}': {e}")
            
            logger.info("Configuration hot-reload completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to handle configuration change: {e}")
    
    def force_reload(self) -> AgentConfigurationSchema:
        """Force immediate reload of configuration."""
        logger.info("Forcing configuration reload...")
        
        new_config = self.settings_loader.load_configuration()
        self._last_reload_time = datetime.now()
        
        # Notify callbacks
        for callback_name, callback in self._callbacks.items():
            try:
                callback(new_config)
                logger.debug(f"Notified callback '{callback_name}' of forced reload")
            except Exception as e:
                logger.error(f"Error in configuration callback '{callback_name}': {e}")
        
        logger.info("Forced configuration reload completed")
        return new_config
    
    def get_status(self) -> Dict[str, Any]:
        """Get hot reload manager status."""
        return {
            "monitoring_active": self._monitor_thread is not None and self._monitor_thread.is_alive(),
            "monitor_interval": self._monitor_interval,
            "registered_callbacks": list(self._callbacks.keys()),
            "last_reload_time": self._last_reload_time.isoformat() if self._last_reload_time else None
        }
    
    def set_monitor_interval(self, interval: float) -> None:
        """Set the monitoring interval in seconds."""
        if interval < 0.5:
            raise ValueError("Monitor interval must be at least 0.5 seconds")
        
        self._monitor_interval = interval
        logger.debug(f"Set monitor interval to {interval} seconds")

class ConfigurationManager:
    """Main configuration manager with hot-reload capability."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize configuration manager."""
        self.project_root = project_root or Path.cwd()
        self.hot_reload_manager = HotReloadManager(project_root)
        self._current_config: Optional[AgentConfigurationSchema] = None
        self._initialized = False
    
    def initialize(self) -> AgentConfigurationSchema:
        """Initialize configuration system with hot reload."""
        if self._initialized:
            return self._current_config
        
        # Load initial configuration
        self._current_config = self.hot_reload_manager.settings_loader.load_configuration()
        
        # Register self as callback for config changes
        self.hot_reload_manager.register_callback("config_manager", self._on_config_changed)
        
        # Start hot reload monitoring if enabled
        if self._current_config.global_settings.get("hot_reload", True):
            self.hot_reload_manager.start_monitoring()
        
        self._initialized = True
        logger.info("Configuration manager initialized with hot reload")
        return self._current_config
    
    def _on_config_changed(self, new_config: AgentConfigurationSchema) -> None:
        """Handle configuration change notification."""
        self._current_config = new_config
        logger.info("Configuration updated via hot reload")
    
    def get_config(self) -> AgentConfigurationSchema:
        """Get current configuration."""
        if not self._initialized:
            return self.initialize()
        
        return self._current_config
    
    def reload_config(self) -> AgentConfigurationSchema:
        """Force reload configuration."""
        self._current_config = self.hot_reload_manager.force_reload()
        return self._current_config
    
    def shutdown(self) -> None:
        """Shutdown configuration manager."""
        if self._initialized:
            self.hot_reload_manager.stop_monitoring()
            self._initialized = False
            logger.info("Configuration manager shutdown")