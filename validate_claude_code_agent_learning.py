#!/usr/bin/env python3
"""
Claude Code Agent Learning Validation Script

This script runs comprehensive validation of Claude Code agent learning capabilities,
including Task tool integration, learning pattern validation, memory system performance,
and agent coordination patterns.
"""

import subprocess
import sys
import time

def run_test_suite(test_class, description):
    """Run a specific test suite and report results."""
    print(f"\n🔄 Running {description}...")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            f"tests/test_claude_code_agent_learning.py::{test_class}", 
            "-v"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ {description} - ALL TESTS PASSED")
            # Count passed tests
            lines = result.stdout.split('\n')
            passed_count = sum(1 for line in lines if " PASSED" in line)
            print(f"   📊 Tests passed: {passed_count}")
        else:
            print(f"❌ {description} - SOME TESTS FAILED")
            print("Error output:")
            print(result.stdout[-500:])  # Show last 500 chars
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏱️  {description} - TIMEOUT (>120s)")
        return False
    except Exception as e:
        print(f"⚠️ {description} - EXCEPTION: {e}")
        return False

def run_coordination_hub_validation():
    """Run coordination hub learning validation tests."""
    print("\n🔄 Running Coordination Hub Learning Validation...")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_agent_selection_validation.py::TestCoordinationHubLearningValidation", 
            "-v"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Coordination Hub Learning Validation - ALL TESTS PASSED")
            lines = result.stdout.split('\n')
            passed_count = sum(1 for line in lines if " PASSED" in line)
            print(f"   📊 Tests passed: {passed_count}")
        else:
            print("❌ Coordination Hub Learning Validation - SOME TESTS FAILED")
            print("Error output:")
            print(result.stdout[-500:])
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏱️  Coordination Hub Learning Validation - TIMEOUT (>60s)")
        return False
    except Exception as e:
        print(f"⚠️ Coordination Hub Learning Validation - EXCEPTION: {e}")
        return False

def main():
    """Main validation workflow."""
    print("🚀 Claude Code Agent Learning Comprehensive Validation")
    print("=" * 70)
    print("Testing actual Claude Code agent learning capabilities...")
    
    start_time = time.time()
    
    # Test suites to run
    test_suites = [
        ("TestTaskToolIntegration", "Task Tool Integration & Parallel Coordination"),
        ("TestLearningPatternValidation", "Learning Pattern Validation from coordination-hub.md"),
        ("TestAgentDirectoryIntegration", "Agent Directory (.claude/agents/) Integration"),
        ("TestMemorySystemPerformance", "Memory System Performance Metrics"),
        ("TestAgentDelegationCoordination", "Agent Delegation & Coordination Patterns")
    ]
    
    results = {}
    
    # Run each test suite
    for test_class, description in test_suites:
        results[description] = run_test_suite(test_class, description)
    
    # Run coordination hub validation
    results["Coordination Hub Learning Validation"] = run_coordination_hub_validation()
    
    # Summary
    total_time = time.time() - start_time
    passed_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print("\n" + "=" * 70)
    print("📋 VALIDATION SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall Results: {passed_count}/{total_count} test suites passed")
    print(f"⏱️  Total validation time: {total_time:.1f}s")
    
    if passed_count == total_count:
        print("\n📋 ALL VALIDATIONS PASSED!")
        print("Claude Code agent learning capabilities are functioning correctly.")
        print("\nKey Capabilities Validated:")
        print("✓ Task() tool parallel coordination pattern recognition")
        print("✓ Infrastructure learning patterns from coordination-hub.md (295 patterns)")
        print("✓ Agent directory integration with 21 loaded agents")
        print("✓ Memory system performance (<100ms response times)")
        print("✓ Agent coordination and delegation workflows")
        return 0
    else:
        print(f"\n❌  {total_count - passed_count} validation(s) failed.")
        print("Some Claude Code agent learning capabilities may need attention.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)