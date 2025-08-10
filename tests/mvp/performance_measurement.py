import time
from functools import wraps
from typing import Callable, Any, Dict
from statistics import mean, stdev

class PerformanceMeasurement:
    def __init__(self):
        self.measurements: Dict[str, list[float]] = {}
        
    def measure(self, name: str) -> Callable:
        """Decorator to measure execution time of a function"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start = time.time()
                result = func(*args, **kwargs)
                duration = (time.time() - start) * 1000  # Convert to ms
                
                if name not in self.measurements:
                    self.measurements[name] = []
                self.measurements[name].append(duration)
                return result
            return wrapper
        return decorator
        
    def get_stats(self, name: str) -> Dict[str, float]:
        """Get performance statistics for a measured operation"""
        if name not in self.measurements:
            raise ValueError(f"No measurements found for {name}")
            
        times = self.measurements[name]
        return {
            "avg_ms": mean(times),
            "min_ms": min(times),
            "max_ms": max(times),
            "stddev_ms": stdev(times) if len(times) > 1 else 0,
            "count": len(times)
        }

    def print_stats(self, name: str) -> None:
        """Print performance statistics for a measured operation"""
        stats = self.get_stats(name)
        print(f"\nPerformance stats for {name}:")
        print(f"  Average: {stats['avg_ms']:.2f}ms")
        print(f"  Min: {stats['min_ms']:.2f}ms")
        print(f"  Max: {stats['max_ms']:.2f}ms")
        print(f"  StdDev: {stats['stddev_ms']:.2f}ms")
        print(f"  Count: {stats['count']}")

    def assert_performance(self, name: str, max_avg_ms: float) -> None:
        """Assert that average execution time is within limit"""
        stats = self.get_stats(name)
        assert stats["avg_ms"] <= max_avg_ms, \
            f"{name} average time {stats['avg_ms']:.2f}ms exceeds limit {max_avg_ms}ms"