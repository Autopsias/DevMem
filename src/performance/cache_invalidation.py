"""
Cache Invalidation System for Dynamic Agent Coordination Content

Handles intelligent cache invalidation for dynamic content to ensure
cache consistency while maintaining performance benefits.
"""

import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

from .prompt_cache import PromptCacheManager, get_cache_manager


class InvalidationReason(Enum):
    """Reasons for cache invalidation."""
    AGENT_CONFIG_CHANGED = "agent_config_changed"
    CONTEXT_CHANGED = "context_changed" 
    MANUAL_INVALIDATION = "manual_invalidation"
    TIME_BASED_EXPIRY = "time_based_expiry"
    MEMORY_PRESSURE = "memory_pressure"
    AGENT_UPDATE = "agent_update"
    PATTERN_UPDATE = "pattern_update"


@dataclass
class InvalidationEvent:
    """Represents a cache invalidation event."""
    timestamp: datetime
    reason: InvalidationReason
    pattern: Optional[str] = None
    agent_type: Optional[str] = None
    entries_affected: int = 0
    description: Optional[str] = None


class FileWatcher:
    """Watches agent configuration files for changes."""
    
    def __init__(self, watch_paths: List[Path], callback: Callable[[Path], None]):
        """
        Initialize file watcher.
        
        Args:
            watch_paths: Paths to monitor for changes
            callback: Function to call when changes detected
        """
        self.watch_paths = watch_paths
        self.callback = callback
        self.file_times: Dict[Path, float] = {}
        self.running = False
        self._thread: Optional[threading.Thread] = None
        
        # Initialize file modification times
        self._update_file_times()
    
    def _update_file_times(self) -> None:
        """Update stored modification times for watched files."""
        for path in self.watch_paths:
            if path.exists():
                if path.is_file():
                    self.file_times[path] = path.stat().st_mtime
                elif path.is_dir():
                    # Watch all files in directory recursively
                    for file_path in path.rglob("*.md"):
                        self.file_times[file_path] = file_path.stat().st_mtime
    
    def start(self) -> None:
        """Start watching for file changes."""
        if self.running:
            return
        
        self.running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop watching for file changes."""
        self.running = False
        if self._thread:
            self._thread.join()
    
    def _watch_loop(self) -> None:
        """Main watch loop."""
        while self.running:
            try:
                self._check_for_changes()
                time.sleep(1.0)  # Check every second
            except Exception as e:
                print(f"File watcher error: {e}")
    
    def _check_for_changes(self) -> None:
        """Check for file changes and trigger callbacks."""
        current_times = {}
        
        # Get current modification times
        for path in self.watch_paths:
            if path.exists():
                if path.is_file():
                    current_times[path] = path.stat().st_mtime
                elif path.is_dir():
                    for file_path in path.rglob("*.md"):
                        current_times[file_path] = file_path.stat().st_mtime
        
        # Check for changes
        for file_path, current_time in current_times.items():
            stored_time = self.file_times.get(file_path, 0)
            
            if current_time > stored_time:
                # File changed
                self.callback(file_path)
                self.file_times[file_path] = current_time
        
        # Update stored times
        self.file_times.update(current_times)


class CacheInvalidationManager:
    """
    Manages cache invalidation for agent coordination system.
    
    Features:
    - File-based invalidation for agent configuration changes
    - Context-based invalidation for dynamic content
    - Pattern-based invalidation for specific coordination types
    - Event logging and monitoring
    - Automatic cleanup and maintenance
    """
    
    def __init__(self, cache_manager: Optional[PromptCacheManager] = None):
        """
        Initialize cache invalidation manager.
        
        Args:
            cache_manager: Cache manager instance to invalidate
        """
        self.cache_manager = cache_manager or get_cache_manager()
        self.invalidation_history: List[InvalidationEvent] = []
        self._lock = threading.RLock()
        
        # File watching setup
        self.agent_dirs = [
            Path.home() / ".claude" / "agents",
            Path.home() / ".claude" / "memory"
        ]
        
        # Check for project-specific agent directories
        project_agent_dir = Path.cwd() / ".claude" / "agents"
        if project_agent_dir.exists():
            self.agent_dirs.append(project_agent_dir)
        
        project_memory_dir = Path.cwd() / ".claude" / "memory"  
        if project_memory_dir.exists():
            self.agent_dirs.append(project_memory_dir)
        
        self.file_watcher = FileWatcher(self.agent_dirs, self._on_file_changed)
        
        # Context invalidation patterns
        self.dynamic_context_patterns = {
            "timestamp", "current_time", "session_id", "request_id",
            "user_input", "dynamic_data", "runtime_config"
        }
        
        # Start file watcher
        self.file_watcher.start()
    
    def _on_file_changed(self, file_path: Path) -> None:
        """Handle file change events."""
        try:
            # Determine what type of file changed
            if "agents" in str(file_path):
                self._invalidate_agent_file_cache(file_path)
            elif "memory" in str(file_path):
                self._invalidate_memory_pattern_cache(file_path)
            else:
                self._invalidate_general_cache(file_path)
                
        except Exception as e:
            print(f"Error handling file change for {file_path}: {e}")
    
    def _invalidate_agent_file_cache(self, file_path: Path) -> None:
        """Invalidate cache entries related to specific agent file."""
        agent_name = file_path.stem
        
        with self._lock:
            # Invalidate by agent type
            affected = self.cache_manager.invalidate_agent_type(agent_name)
            
            # Also invalidate by pattern matching
            pattern_affected = self.cache_manager.invalidate_pattern(agent_name)
            
            total_affected = affected + pattern_affected
            
            if total_affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.AGENT_CONFIG_CHANGED,
                    agent_type=agent_name,
                    entries_affected=total_affected,
                    description=f"Agent configuration file changed: {file_path}"
                )
                
                self.invalidation_history.append(event)
                print(f"Invalidated {total_affected} cache entries due to agent {agent_name} changes")
    
    def _invalidate_memory_pattern_cache(self, file_path: Path) -> None:
        """Invalidate cache entries related to memory pattern file."""
        pattern = file_path.stem
        
        with self._lock:
            affected = self.cache_manager.invalidate_pattern(pattern)
            
            if affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.PATTERN_UPDATE,
                    pattern=pattern,
                    entries_affected=affected,
                    description=f"Memory pattern file changed: {file_path}"
                )
                
                self.invalidation_history.append(event)
                print(f"Invalidated {affected} cache entries due to pattern {pattern} changes")
    
    def _invalidate_general_cache(self, file_path: Path) -> None:
        """Invalidate cache entries for general file changes."""
        with self._lock:
            # For general changes, clear expired entries as a conservative measure
            affected = self.cache_manager.clear_expired_entries()
            
            if affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.AGENT_UPDATE,
                    entries_affected=affected,
                    description=f"General configuration file changed: {file_path}"
                )
                
                self.invalidation_history.append(event)
    
    def invalidate_by_context_change(self, context_keys: Set[str]) -> int:
        """
        Invalidate cache entries that depend on changed context keys.
        
        Args:
            context_keys: Set of context keys that changed
            
        Returns:
            Number of entries invalidated
        """
        with self._lock:
            total_affected = 0
            
            # Check if any dynamic context patterns are present
            if self.dynamic_context_patterns.intersection(context_keys):
                # Invalidate entries with context hashes (dynamic content)
                for key, entry in list(self.cache_manager._cache.items()):
                    if entry.context_hash is not None:
                        del self.cache_manager._cache[key]
                        self.cache_manager._stats.evictions += 1
                        total_affected += 1
            
            if total_affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.CONTEXT_CHANGED,
                    entries_affected=total_affected,
                    description=f"Context keys changed: {', '.join(context_keys)}"
                )
                
                self.invalidation_history.append(event)
                self.cache_manager._update_storage_stats()
            
            return total_affected
    
    def manual_invalidate_pattern(self, pattern: str, reason: str = "") -> int:
        """
        Manually invalidate cache entries matching pattern.
        
        Args:
            pattern: Pattern to match against cache keys
            reason: Reason for manual invalidation
            
        Returns:
            Number of entries invalidated
        """
        with self._lock:
            affected = self.cache_manager.invalidate_pattern(pattern)
            
            if affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.MANUAL_INVALIDATION,
                    pattern=pattern,
                    entries_affected=affected,
                    description=reason or f"Manual invalidation of pattern: {pattern}"
                )
                
                self.invalidation_history.append(event)
            
            return affected
    
    def manual_invalidate_agent(self, agent_type: str, reason: str = "") -> int:
        """
        Manually invalidate cache entries for specific agent.
        
        Args:
            agent_type: Agent type to invalidate
            reason: Reason for manual invalidation
            
        Returns:
            Number of entries invalidated
        """
        with self._lock:
            affected = self.cache_manager.invalidate_agent_type(agent_type)
            
            if affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.MANUAL_INVALIDATION,
                    agent_type=agent_type,
                    entries_affected=affected,
                    description=reason or f"Manual invalidation of agent: {agent_type}"
                )
                
                self.invalidation_history.append(event)
            
            return affected
    
    def cleanup_expired_entries(self) -> int:
        """
        Clean up expired cache entries.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            affected = self.cache_manager.clear_expired_entries()
            
            if affected > 0:
                event = InvalidationEvent(
                    timestamp=datetime.now(),
                    reason=InvalidationReason.TIME_BASED_EXPIRY,
                    entries_affected=affected,
                    description="Routine cleanup of expired entries"
                )
                
                self.invalidation_history.append(event)
            
            return affected
    
    def get_invalidation_history(self, 
                               limit: Optional[int] = None,
                               since: Optional[datetime] = None) -> List[InvalidationEvent]:
        """
        Get invalidation history events.
        
        Args:
            limit: Maximum number of events to return
            since: Only return events after this timestamp
            
        Returns:
            List of invalidation events
        """
        with self._lock:
            events = self.invalidation_history
            
            if since:
                events = [event for event in events if event.timestamp > since]
            
            # Sort by timestamp (newest first)
            events = sorted(events, key=lambda e: e.timestamp, reverse=True)
            
            if limit:
                events = events[:limit]
            
            return events
    
    def get_invalidation_stats(self) -> Dict[str, Any]:
        """Get invalidation statistics."""
        with self._lock:
            total_events = len(self.invalidation_history)
            
            if total_events == 0:
                return {
                    "total_events": 0,
                    "events_by_reason": {},
                    "total_entries_affected": 0,
                    "most_recent": None
                }
            
            # Count by reason
            events_by_reason = {}
            total_affected = 0
            
            for event in self.invalidation_history:
                reason = event.reason.value
                events_by_reason[reason] = events_by_reason.get(reason, 0) + 1
                total_affected += event.entries_affected
            
            # Get most recent event
            most_recent = max(self.invalidation_history, key=lambda e: e.timestamp)
            
            return {
                "total_events": total_events,
                "events_by_reason": events_by_reason,
                "total_entries_affected": total_affected,
                "most_recent": {
                    "timestamp": most_recent.timestamp.isoformat(),
                    "reason": most_recent.reason.value,
                    "entries_affected": most_recent.entries_affected,
                    "description": most_recent.description
                }
            }
    
    def shutdown(self) -> None:
        """Shutdown invalidation manager and cleanup resources."""
        self.file_watcher.stop()


# Global invalidation manager instance
_invalidation_manager: Optional[CacheInvalidationManager] = None


def get_invalidation_manager() -> CacheInvalidationManager:
    """Get or create global cache invalidation manager."""
    global _invalidation_manager
    if _invalidation_manager is None:
        _invalidation_manager = CacheInvalidationManager()
    return _invalidation_manager


def invalidate_agent_cache(agent_type: str, reason: str = "") -> int:
    """
    Convenience function to invalidate cache for specific agent.
    
    Args:
        agent_type: Agent type to invalidate
        reason: Reason for invalidation
        
    Returns:
        Number of entries invalidated
    """
    manager = get_invalidation_manager()
    return manager.manual_invalidate_agent(agent_type, reason)


def invalidate_pattern_cache(pattern: str, reason: str = "") -> int:
    """
    Convenience function to invalidate cache by pattern.
    
    Args:
        pattern: Pattern to match
        reason: Reason for invalidation
        
    Returns:
        Number of entries invalidated  
    """
    manager = get_invalidation_manager()
    return manager.manual_invalidate_pattern(pattern, reason)


def invalidate_dynamic_context() -> int:
    """
    Convenience function to invalidate dynamic context cache entries.
    
    Returns:
        Number of entries invalidated
    """
    manager = get_invalidation_manager()
    return manager.invalidate_by_context_change({"timestamp", "current_time", "dynamic_data"})