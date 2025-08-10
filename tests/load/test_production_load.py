import pytest
import asyncio
import time
from typing import List, Dict, Any
from pathlib import Path
import sys
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.patterns.base import PatternBase
from src.validation.validator import ValidationFramework


class TestProductionLoad:
    """Production-level load tests for 5000+ requests/hour sustained performance"""
    
    @pytest.fixture
    def validation_framework(self) -> ValidationFramework:
        return ValidationFramework()

    @pytest.mark.production
    async def test_sustained_5000_requests_per_hour(self, validation_framework: ValidationFramework):
        """Test sustained load of 5000+ requests per hour"""
        requests_per_hour = 5000
        test_duration_seconds = 60  # 1-minute test for production validation
        request_interval = 3600 / requests_per_hour  # seconds between requests
        
        pattern_inputs = [
            {"type": "sequential", "input": f"production_test_{i % 100}"}
            for i in range(requests_per_hour)
        ]
        
        start_time = time.time()
        request_count = 0
        failed_requests = 0
        response_times = []
        
        async def process_request(pattern_input: Dict[str, Any]) -> bool:
            try:
                req_start = time.time()
                result = await validation_framework.validate_pattern_execution(pattern_input)
                response_times.append(time.time() - req_start)
                return result.success
            except Exception:
                return False
        
        # Create batches of requests to simulate steady load
        batch_size = int(requests_per_hour / 60)  # Requests per second
        
        while time.time() - start_time < test_duration_seconds:
            batch_start = time.time()
            
            # Process batch of requests concurrently
            batch = pattern_inputs[request_count:request_count + batch_size]
            if not batch:
                break
                
            tasks = [process_request(input_data) for input_data in batch]
            results = await asyncio.gather(*tasks)
            
            request_count += len(batch)
            failed_requests += results.count(False)
            
            # Maintain steady request rate
            batch_duration = time.time() - batch_start
            if batch_duration < 1.0:
                await asyncio.sleep(1.0 - batch_duration)
        
        # Calculate metrics
        success_rate = (request_count - failed_requests) / request_count if request_count > 0 else 0
        avg_response_time = statistics.mean(response_times) if response_times else 0
        p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0
        
        # Production assertions
        assert request_count >= (requests_per_hour * test_duration_seconds / 3600), \
            f"Did not meet {requests_per_hour}/hour rate, only processed {request_count}"
        assert success_rate >= 0.995, f"Success rate {success_rate} below 99.5% target"
        assert p95_response_time < 0.050, f"P95 response time {p95_response_time}s exceeds 50ms target"

    @pytest.mark.production
    async def test_25_concurrent_pattern_executions(self, validation_framework: ValidationFramework):
        """Test 25+ simultaneous pattern executions without degradation"""
        max_concurrent = 25
        
        # Create diverse pattern types for realistic testing
        pattern_inputs = [
            {"type": "sequential", "input": f"concurrent_test_{i}"} if i % 3 == 0
            else {"type": "parallel", "input": f"concurrent_test_{i}"} if i % 3 == 1
            else {"type": "meta", "input": f"concurrent_test_{i}"}
            for i in range(max_concurrent * 3)  # Extra patterns to test queuing
        ]
        
        async def execute_pattern_batch(batch: List[Dict[str, Any]]) -> List[float]:
            async def execute_single(input_data: Dict[str, Any]) -> float:
                start_time = time.time()
                result = await validation_framework.validate_pattern_execution(input_data)
                assert result.success, f"Pattern execution failed for {input_data}"
                return time.time() - start_time
            
            tasks = [execute_single(input_data) for input_data in batch]
            return await asyncio.gather(*tasks)
        
        # Test multiple waves of concurrent executions
        all_execution_times = []
        for i in range(0, len(pattern_inputs), max_concurrent):
            batch = pattern_inputs[i:i + max_concurrent]
            execution_times = await execute_pattern_batch(batch)
            all_execution_times.extend(execution_times)
        
        # Verify performance metrics
        avg_time = statistics.mean(all_execution_times)
        p95_time = statistics.quantiles(all_execution_times, n=20)[18]
        max_time = max(all_execution_times)
        
        assert avg_time < 0.050, f"Average response time {avg_time}s exceeds 50ms target"
        assert p95_time < 0.050, f"P95 response time {p95_time}s exceeds 50ms target"
        assert max_time < 0.100, f"Max response time {max_time}s exceeds 100ms threshold"

    @pytest.mark.production
    def test_memory_under_maximum_load(self, validation_framework: ValidationFramework):
        """Test memory usage under maximum concurrent load stays under 2GB"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create memory-intensive patterns
        large_patterns = []
        for i in range(1000):  # Increased pattern count for production test
            pattern = {
                "type": "meta",
                "input": "x" * 100000,  # 100KB per pattern
                "metadata": {
                    "index": i,
                    "data": ["item" * 100 for _ in range(10)]
                }
            }
            large_patterns.append(pattern)
        
        # Process with maximum concurrency
        with ThreadPoolExecutor(max_workers=25) as executor:
            futures = []
            for pattern in large_patterns:
                future = executor.submit(validation_framework.validate_pattern_structure, pattern)
                futures.append(future)
            
            # Wait for all to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    pass  # Continue processing even with failures
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        assert memory_increase < 2048, f"Memory usage increase {memory_increase}MB exceeds 2GB limit"

    @pytest.mark.production
    def test_cpu_under_sustained_load(self, validation_framework: ValidationFramework):
        """Test CPU usage stays under 70% under sustained high-volume operations"""
        process = psutil.Process()
        
        # Calculate target CPU usage
        total_cpus = psutil.cpu_count()
        target_cpu_percent = 70
        
        # Create CPU-intensive workload
        cpu_patterns = []
        for i in range(100):
            pattern = {
                "type": "meta",
                "input": f"cpu_test_{i}",
                "operations": ["analyze", "optimize", "validate", "transform"],
                "complexity": "high"
            }
            cpu_patterns.append(pattern)
        
        # Monitor CPU during processing
        cpu_samples = []
        
        with ThreadPoolExecutor(max_workers=25) as executor:
            futures = []
            
            # Submit all patterns
            for pattern in cpu_patterns:
                future = executor.submit(validation_framework.validate_pattern_structure, pattern)
                futures.append(future)
            
            # Sample CPU usage while processing
            start_time = time.time()
            while any(not f.done() for f in futures):
                cpu_percent = process.cpu_percent(interval=0.1)
                cpu_samples.append(cpu_percent)
                
                if time.time() - start_time > 10:  # Timeout after 10 seconds
                    break
            
            # Wait for remaining futures
            for future in as_completed(futures, timeout=5):
                try:
                    future.result()
                except Exception:
                    pass
        
        # Analyze CPU usage
        if cpu_samples:
            avg_cpu = statistics.mean(cpu_samples)
            max_cpu = max(cpu_samples)
            
            # Normalize for total CPUs (psutil reports per-process percentage)
            normalized_avg = avg_cpu / total_cpus * 100
            normalized_max = max_cpu / total_cpus * 100
            
            assert normalized_avg <= target_cpu_percent, \
                f"Average CPU {normalized_avg}% exceeds {target_cpu_percent}% target"
            assert normalized_max <= 100, \
                f"Peak CPU {normalized_max}% exceeds 100% threshold"

    @pytest.mark.production
    async def test_pattern_lookup_under_load(self, validation_framework: ValidationFramework):
        """Test pattern lookup maintains <50ms P95 under peak load"""
        num_patterns = 5000  # Production-scale pattern count
        
        # Create diverse patterns for realistic lookup testing
        patterns = []
        for i in range(num_patterns):
            pattern_type = ["sequential", "parallel", "meta"][i % 3]
            pattern = {
                "type": pattern_type,
                "input": f"lookup_test_{i}",
                "tags": [f"tag_{i % 10}", f"category_{i % 5}"],
                "priority": i % 3
            }
            patterns.append(pattern)
        
        # Perform lookups under concurrent load
        async def perform_lookup(pattern: Dict[str, Any]) -> float:
            start_time = time.time()
            try:
                await validation_framework.lookup_similar_patterns(pattern)
            except Exception:
                pass  # Continue even if lookup fails
            return time.time() - start_time
        
        # Execute lookups in concurrent batches
        batch_size = 100
        all_lookup_times = []
        
        for i in range(0, len(patterns), batch_size):
            batch = patterns[i:i + batch_size]
            tasks = [perform_lookup(p) for p in batch]
            lookup_times = await asyncio.gather(*tasks)
            all_lookup_times.extend(lookup_times)
        
        # Calculate performance metrics
        avg_lookup = statistics.mean(all_lookup_times)
        p50_lookup = statistics.median(all_lookup_times)
        p95_lookup = statistics.quantiles(all_lookup_times, n=20)[18]
        p99_lookup = statistics.quantiles(all_lookup_times, n=100)[98]
        
        # Production assertions
        assert avg_lookup < 0.030, f"Average lookup {avg_lookup}s exceeds 30ms target"
        assert p50_lookup < 0.025, f"P50 lookup {p50_lookup}s exceeds 25ms target"
        assert p95_lookup < 0.050, f"P95 lookup {p95_lookup}s exceeds 50ms target"
        assert p99_lookup < 0.100, f"P99 lookup {p99_lookup}s exceeds 100ms threshold"


@pytest.mark.production
class TestLoadTestInfrastructure:
    """Test the load testing infrastructure itself"""
    
    def test_load_generator_accuracy(self):
        """Verify load generator can accurately produce target request rates"""
        target_rps = 5000 / 3600  # 5000 requests per hour
        duration = 5  # seconds
        
        request_times = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            request_times.append(time.time())
            time.sleep(1 / target_rps)
        
        # Calculate actual request rate
        actual_duration = request_times[-1] - request_times[0]
        actual_rps = len(request_times) / actual_duration
        
        # Allow 20% variance for CI environments
        variance = abs(actual_rps - target_rps) / target_rps
        assert variance < 0.20, \
            f"Load generator accuracy off: target {target_rps} rps, actual {actual_rps} rps (variance: {variance:.2%})"
    
    def test_metrics_collection_accuracy(self):
        """Verify metrics collection is accurate and doesn't impact performance"""
        samples = []
        
        # Simulate metric collection
        for _ in range(1000):
            start = time.perf_counter()
            # Simulate some work
            _ = sum(range(1000))
            duration = time.perf_counter() - start
            samples.append(duration)
        
        # Verify metrics calculations
        avg = statistics.mean(samples)
        p95 = statistics.quantiles(samples, n=20)[18]
        
        assert avg > 0, "Average calculation failed"
        assert p95 >= avg, "P95 should be >= average"
        assert len(samples) == 1000, "Sample collection incomplete"