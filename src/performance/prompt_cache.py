"""
Prompt Caching System for Agent Coordination Performance Optimization

Implements intelligent caching for agent coordination patterns to reduce
repeated overhead by at least 40% as specified in story acceptance criteria.
"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
import threading
from dataclasses import dataclass, asdict
from enum import Enum


class CacheStrategy(Enum):
    """Cache strategies for different types of coordination patterns."""
    AGENT_COORDINATION = "agent_coordination"
    PROMPT_TEMPLATES = "prompt_templates"
    CONTEXT_PATTERNS = "context_patterns"
    SEQUENTIAL_FLOWS = "sequential_flows"
    PARALLEL_PATTERNS = "parallel_patterns"


@dataclass
class CacheEntry:
    """Represents a cached prompt or coordination pattern."""
    key: str
    content: str
    strategy: CacheStrategy
    created_at: datetime
    last_accessed: datetime
    access_count: int
    context_hash: Optional[str] = None
    agent_types: Optional[Set[str]] = None
    expiry_time: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        if self.expiry_time is None:
            return False
        return datetime.now() > self.expiry_time
    
    def update_access(self) -> None:
        """Update last accessed time and increment access count."""
        self.last_accessed = datetime.now()
        self.access_count += 1


@dataclass
class CacheStats:
    """Statistics for cache performance monitoring."""
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    evictions: int = 0
    storage_size_bytes: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.cache_hits / self.total_requests) * 100.0
    
    @property
    def miss_rate(self) -> float:
        """Calculate cache miss rate percentage."""
        return 100.0 - self.hit_rate


class PromptCacheManager:
    """
    Manages prompt caching for agent coordination patterns.
    
    Features:
    - Intelligent cache keys based on coordination patterns
    - LRU eviction with configurable size limits
    - Cache invalidation for dynamic content
    - Performance metrics and monitoring
    - Thread-safe operations
    """
    
    def __init__(self, 
                 max_entries: int = 1000,
                 max_memory_mb: int = 100,
                 default_ttl_hours: int = 24):
        """
        Initialize prompt cache manager.
        
        Args:
            max_entries: Maximum number of cache entries
            max_memory_mb: Maximum memory usage in MB
            default_ttl_hours: Default time-to-live in hours
        """
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.default_ttl = timedelta(hours=default_ttl_hours)
        
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = CacheStats()
        self._lock = threading.RLock()
        
        # Cache persistence
        self.cache_dir = Path.home() / ".claude" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "prompt_cache.json"
        
        # Load existing cache if available
        self._load_cache()
    
    def _generate_cache_key(self, 
                           prompt_template: str,
                           context: Dict[str, Any],
                           strategy: CacheStrategy,
                           agent_types: Optional[Set[str]] = None) -> str:
        """
        Generate cache key for coordination pattern.
        
        Args:
            prompt_template: The prompt template
            context: Context dictionary for the prompt
            strategy: Cache strategy type
            agent_types: Set of involved agent types
            
        Returns:
            Unique cache key string
        """
        # Create deterministic content for hashing
        key_content = {
            "template": prompt_template,
            "context": sorted(context.items()) if context else [],
            "strategy": strategy.value,
            "agents": sorted(list(agent_types)) if agent_types else []
        }
        
        # Generate hash
        content_str = json.dumps(key_content, sort_keys=True)
        cache_key = hashlib.sha256(content_str.encode()).hexdigest()[:16]
        
        return f"{strategy.value}_{cache_key}"
    
    def _context_hash(self, context: Dict[str, Any]) -> str:
        """Generate hash for context to detect changes."""
        if not context:
            return ""
        content_str = json.dumps(context, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()[:8]
    
    def get_cached_prompt(self,
                         prompt_template: str,
                         context: Dict[str, Any],
                         strategy: CacheStrategy,
                         agent_types: Optional[Set[str]] = None) -> Optional[str]:
        """
        Retrieve cached prompt if available and valid.
        
        Args:
            prompt_template: The prompt template
            context: Context for the prompt
            strategy: Cache strategy
            agent_types: Involved agent types
            
        Returns:
            Cached prompt content or None if not found/expired
        """
        with self._lock:
            self._stats.total_requests += 1
            
            cache_key = self._generate_cache_key(
                prompt_template, context, strategy, agent_types
            )
            
            entry = self._cache.get(cache_key)
            
            if entry is None:
                self._stats.cache_misses += 1
                return None
            
            # Check expiration
            if entry.is_expired():
                del self._cache[cache_key]
                self._stats.cache_misses += 1
                self._stats.evictions += 1
                return None
            
            # Check context changes for dynamic content
            if entry.context_hash:
                current_hash = self._context_hash(context)
                if current_hash != entry.context_hash:
                    # Context changed, invalidate cache
                    del self._cache[cache_key]
                    self._stats.cache_misses += 1
                    self._stats.evictions += 1
                    return None
            
            # Cache hit
            entry.update_access()
            self._stats.cache_hits += 1
            return entry.content
    
    def cache_prompt(self,
                    prompt_template: str,
                    context: Dict[str, Any],
                    strategy: CacheStrategy,
                    rendered_prompt: str,
                    agent_types: Optional[Set[str]] = None,
                    ttl_hours: Optional[int] = None) -> None:
        """
        Cache a rendered prompt for future use.
        
        Args:
            prompt_template: The prompt template
            context: Context used for rendering
            strategy: Cache strategy
            rendered_prompt: The final rendered prompt
            agent_types: Involved agent types
            ttl_hours: Time-to-live in hours (uses default if None)
        """
        with self._lock:
            cache_key = self._generate_cache_key(
                prompt_template, context, strategy, agent_types
            )
            
            # Calculate expiry time
            ttl = timedelta(hours=ttl_hours) if ttl_hours else self.default_ttl
            expiry_time = datetime.now() + ttl
            
            # Create cache entry
            entry = CacheEntry(
                key=cache_key,
                content=rendered_prompt,
                strategy=strategy,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=0,
                context_hash=self._context_hash(context) if self._is_dynamic_context(context) else None,
                agent_types=agent_types.copy() if agent_types else None,
                expiry_time=expiry_time
            )
            
            # Check if we need to evict entries
            self._maybe_evict_entries(len(rendered_prompt))
            
            # Store entry
            self._cache[cache_key] = entry
            self._update_storage_stats()
    
    def _is_dynamic_context(self, context: Dict[str, Any]) -> bool:
        """Check if context contains dynamic content that should trigger invalidation."""
        dynamic_keys = {'timestamp', 'session_id', 'request_id', 'current_time'}
        return bool(dynamic_keys.intersection(context.keys()))
    
    def _maybe_evict_entries(self, new_entry_size: int) -> None:
        """Evict entries if necessary to stay within limits."""
        # Check entry count limit
        while len(self._cache) >= self.max_entries:
            self._evict_lru_entry()
        
        # Check memory limit (approximate)
        current_size = sum(len(entry.content) for entry in self._cache.values())
        
        while (current_size + new_entry_size) > self.max_memory_bytes and self._cache:
            self._evict_lru_entry()
            current_size = sum(len(entry.content) for entry in self._cache.values())
    
    def _evict_lru_entry(self) -> None:
        """Evict least recently used entry."""
        if not self._cache:
            return
        
        # Find LRU entry
        lru_key = min(self._cache.keys(), 
                     key=lambda k: self._cache[k].last_accessed)
        
        del self._cache[lru_key]
        self._stats.evictions += 1
    
    def _update_storage_stats(self) -> None:
        """Update storage size statistics."""
        self._stats.storage_size_bytes = sum(
            len(entry.content) for entry in self._cache.values()
        )
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.
        
        Args:
            pattern: Pattern to match against cache keys
            
        Returns:
            Number of entries invalidated
        """
        with self._lock:
            keys_to_remove = [
                key for key in self._cache.keys() 
                if pattern in key
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
                self._stats.evictions += 1
            
            self._update_storage_stats()
            return len(keys_to_remove)
    
    def invalidate_agent_type(self, agent_type: str) -> int:
        """
        Invalidate cache entries for specific agent type.
        
        Args:
            agent_type: Agent type to invalidate
            
        Returns:
            Number of entries invalidated
        """
        with self._lock:
            keys_to_remove = []
            
            for key, entry in self._cache.items():
                if entry.agent_types and agent_type in entry.agent_types:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self._cache[key]
                self._stats.evictions += 1
            
            self._update_storage_stats()
            return len(keys_to_remove)
    
    def clear_expired_entries(self) -> int:
        """
        Clear all expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            keys_to_remove = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
                self._stats.evictions += 1
            
            self._update_storage_stats()
            return len(keys_to_remove)
    
    def get_stats(self) -> CacheStats:
        """Get current cache statistics."""
        with self._lock:
            self._update_storage_stats()
            return CacheStats(
                total_requests=self._stats.total_requests,
                cache_hits=self._stats.cache_hits,
                cache_misses=self._stats.cache_misses,
                evictions=self._stats.evictions,
                storage_size_bytes=self._stats.storage_size_bytes
            )
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information."""
        with self._lock:
            stats = self.get_stats()
            
            return {
                "stats": asdict(stats),
                "entries_count": len(self._cache),
                "max_entries": self.max_entries,
                "max_memory_mb": self.max_memory_bytes // (1024 * 1024),
                "strategies": list(set(entry.strategy.value for entry in self._cache.values())),
                "oldest_entry": min(
                    (entry.created_at.isoformat() for entry in self._cache.values()),
                    default=None
                ),
                "most_accessed": max(
                    (entry.access_count for entry in self._cache.values()),
                    default=0
                )
            }
    
    def _save_cache(self) -> None:
        """Save cache to persistent storage."""
        try:
            cache_data = {}
            
            for key, entry in self._cache.items():
                cache_data[key] = {
                    "content": entry.content,
                    "strategy": entry.strategy.value,
                    "created_at": entry.created_at.isoformat(),
                    "last_accessed": entry.last_accessed.isoformat(),
                    "access_count": entry.access_count,
                    "context_hash": entry.context_hash,
                    "agent_types": list(entry.agent_types) if entry.agent_types else None,
                    "expiry_time": entry.expiry_time.isoformat() if entry.expiry_time else None
                }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            # Don't fail if cache save fails
            print(f"Warning: Failed to save cache: {e}")
    
    def _load_cache(self) -> None:
        """Load cache from persistent storage."""
        try:
            if not self.cache_file.exists():
                return
            
            with open(self.cache_file) as f:
                cache_data = json.load(f)
            
            for key, data in cache_data.items():
                try:
                    entry = CacheEntry(
                        key=key,
                        content=data["content"],
                        strategy=CacheStrategy(data["strategy"]),
                        created_at=datetime.fromisoformat(data["created_at"]),
                        last_accessed=datetime.fromisoformat(data["last_accessed"]),
                        access_count=data["access_count"],
                        context_hash=data.get("context_hash"),
                        agent_types=set(data["agent_types"]) if data.get("agent_types") else None,
                        expiry_time=datetime.fromisoformat(data["expiry_time"]) if data.get("expiry_time") else None
                    )
                    
                    # Skip expired entries
                    if not entry.is_expired():
                        self._cache[key] = entry
                        
                except (ValueError, KeyError) as e:
                    # Skip malformed entries
                    continue
            
            self._update_storage_stats()
            
        except Exception as e:
            # Don't fail if cache load fails
            print(f"Warning: Failed to load cache: {e}")
    
    def shutdown(self) -> None:
        """Save cache and clean up resources."""
        with self._lock:
            self._save_cache()


# Global cache manager instance
_cache_manager: Optional[PromptCacheManager] = None


def get_cache_manager() -> PromptCacheManager:
    """Get or create global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = PromptCacheManager()
    return _cache_manager


def cache_agent_coordination_prompt(prompt_template: str,
                                  context: Dict[str, Any],
                                  rendered_prompt: str,
                                  agent_types: Optional[Set[str]] = None,
                                  ttl_hours: int = 24) -> None:
    """
    Convenience function to cache agent coordination prompt.
    
    Args:
        prompt_template: The prompt template
        context: Context used for rendering
        rendered_prompt: The final rendered prompt  
        agent_types: Involved agent types
        ttl_hours: Time-to-live in hours
    """
    cache_manager = get_cache_manager()
    cache_manager.cache_prompt(
        prompt_template=prompt_template,
        context=context,
        strategy=CacheStrategy.AGENT_COORDINATION,
        rendered_prompt=rendered_prompt,
        agent_types=agent_types,
        ttl_hours=ttl_hours
    )


def get_cached_agent_coordination_prompt(prompt_template: str,
                                       context: Dict[str, Any],
                                       agent_types: Optional[Set[str]] = None) -> Optional[str]:
    """
    Convenience function to retrieve cached agent coordination prompt.
    
    Args:
        prompt_template: The prompt template
        context: Context for the prompt
        agent_types: Involved agent types
        
    Returns:
        Cached prompt content or None if not found
    """
    cache_manager = get_cache_manager()
    return cache_manager.get_cached_prompt(
        prompt_template=prompt_template,
        context=context,
        strategy=CacheStrategy.AGENT_COORDINATION,
        agent_types=agent_types
    )