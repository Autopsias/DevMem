#!/usr/bin/env python3
"""Quick validation script for enhanced agent selection."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent_selector import EnhancedAgentSelector, select_best_agent

def test_basic_functionality():
    """Test basic functionality of enhanced agent selector."""
    print("Testing Enhanced Agent Selection System")
    print("=" * 50)
    
    # Test basic instantiation
    try:
        selector = EnhancedAgentSelector()
        print("✓ Enhanced agent selector created successfully")
    except Exception as e:
        print(f"✗ Failed to create selector: {e}")
        return False
    
    # Test basic selection
    test_cases = [
        ("pytest test failing with async mock configuration", "test-specialist"),
        ("docker orchestration issues with container networking", "infrastructure-engineer"),
        ("security vulnerability scan reveals credential leaks", "security-enforcer"),
        ("performance bottleneck in latency optimization", "performance-optimizer"),
        ("refactor code with better variable naming", "intelligent-enhancer")
    ]
    
    success_count = 0
    for query, expected_agent in test_cases:
        try:
            result = selector.select_agent(query)
            
            if result.agent_name == expected_agent:
                print(f"✓ '{query[:40]}...' -> {result.agent_name} (confidence: {result.confidence_score:.2f})")
                success_count += 1
            else:
                print(f"✗ '{query[:40]}...' -> {result.agent_name} (expected {expected_agent})")
                
        except Exception as e:
            print(f"✗ Error processing '{query[:40]}...': {e}")
    
    # Test global function
    try:
        global_result = select_best_agent("test query")
        print(f"✓ Global select_best_agent() function works: {global_result.agent_name}")
    except Exception as e:
        print(f"✗ Global function failed: {e}")
        return False
    
    # Test edge cases
    try:
        empty_result = selector.select_agent("")
        print(f"✓ Empty query handled: {empty_result.agent_name} (confidence: {empty_result.confidence_score:.2f})")
    except Exception as e:
        print(f"✗ Empty query handling failed: {e}")
        return False
    
    # Test multi-suggestions
    try:
        suggestions = selector.get_agent_suggestions("docker container testing performance", top_n=3)
        print(f"✓ Multi-suggestions work: {len(suggestions)} suggestions returned")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"    {i}. {suggestion.agent_name} (confidence: {suggestion.confidence_score:.2f})")
    except Exception as e:
        print(f"✗ Multi-suggestions failed: {e}")
        return False
    
    # Test statistics
    try:
        stats = selector.get_selection_stats()
        if stats:
            print(f"✓ Statistics tracking works: {stats.get('total_selections', 0)} selections tracked")
        else:
            print("✓ Statistics tracking initialized (no selections yet)")
    except Exception as e:
        print(f"✗ Statistics tracking failed: {e}")
        return False
    
    accuracy = success_count / len(test_cases)
    print("\nTest Results:")
    print(f"  Accuracy: {accuracy:.1%} ({success_count}/{len(test_cases)})")
    print(f"  Overall: {'PASS' if accuracy >= 0.8 else 'FAIL'}")
    
    return accuracy >= 0.8

def test_performance():
    """Test basic performance characteristics."""
    print("\nTesting Performance")
    print("=" * 30)
    
    import time
    selector = EnhancedAgentSelector()
    
    # Test single query performance
    query = "pytest async test mock configuration failing"
    start_time = time.perf_counter()
    result = selector.select_agent(query)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    print(f"Single query: {elapsed_ms:.2f}ms (target: <3ms)")
    print(f"Result: {result.agent_name} (confidence: {result.confidence_score:.2f})")
    
    # Test batch performance
    queries = [
        "test failing",
        "docker issue", 
        "security problem",
        "performance slow",
        "refactor code"
    ] * 20  # 100 total queries
    
    start_time = time.perf_counter()
    _ = [selector.select_agent(q) for q in queries]
    total_time_ms = (time.perf_counter() - start_time) * 1000
    avg_time_ms = total_time_ms / len(queries)
    
    print(f"Batch performance ({len(queries)} queries): {avg_time_ms:.2f}ms avg (target: <2ms)")
    print(f"Total time: {total_time_ms:.1f}ms")
    
    performance_ok = elapsed_ms < 5.0 and avg_time_ms < 3.0  # Relaxed targets for validation
    print(f"Performance: {'PASS' if performance_ok else 'FAIL'}")
    
    return performance_ok

def main():
    """Main validation function."""
    functionality_ok = test_basic_functionality()
    performance_ok = test_performance()
    
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Functionality: {'PASS' if functionality_ok else 'FAIL'}")
    print(f"Performance:   {'PASS' if performance_ok else 'FAIL'}")
    
    overall_pass = functionality_ok and performance_ok
    print(f"Overall:       {'PASS' if overall_pass else 'FAIL'}")
    
    if overall_pass:
        print("\n✅ Enhanced agent selection system is working correctly!")
        print("Ready to run comprehensive tests with: make test-agent-matching")
    else:
        print("\n❌ Enhanced agent selection system has issues.")
        print("Please check the implementation and run tests for detailed diagnostics.")
    
    return 0 if overall_pass else 1

if __name__ == '__main__':
    exit(main())
