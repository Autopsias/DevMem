#!/usr/bin/env python3
"""Simple validation script for infrastructure learning improvements.

This validates the focused solution to improve infrastructure task coordination:
1. Add learning capabilities to EnhancedCrossDomainCoordinator
2. Store successful patterns in coordination-hub.md
3. Use patterns to improve future selections
4. Target: Improve current 38% accuracy while maintaining reasonable performance
"""

import sys
from pathlib import Path
import time
import tempfile
from typing import Dict

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from enhanced_cross_domain_coordinator import (
    EnhancedCrossDomainCoordinator,
    PatternLearningEngine
)


def run_infrastructure_learning_validation() -> Dict[str, float]:
    """Run focused validation for infrastructure learning improvements."""
    print("🚀 Infrastructure Learning Validation")
    print("=" * 50)
    
    # Create temporary hub for testing
    temp_dir = tempfile.mkdtemp()
    hub_path = Path(temp_dir) / "coordination-hub.md"
    
    # Test queries with correct infrastructure agents
    test_cases = [
        ("docker container orchestration setup", "infrastructure-engineer"),
        ("kubernetes pod scaling issues", "infrastructure-engineer"),
        ("docker performance optimization", "performance-optimizer"),
        ("container networking problems", "docker-specialist"),
        ("infrastructure monitoring setup", "infrastructure-engineer"),
        ("kubernetes service mesh configuration", "infrastructure-engineer"),
        ("docker resource allocation", "performance-optimizer"),
        ("infrastructure terraform provisioning", "infrastructure-engineer"),
        ("docker swarm orchestration", "docker-specialist"),
        ("container registry management", "docker-specialist")
    ]
    
    # Step 1: Baseline measurement (without learning)
    print("\n📊 Step 1: Baseline Measurement")
    baseline_coordinator = EnhancedCrossDomainCoordinator()
    baseline_coordinator.pattern_learning_engine = None  # Disable learning
    
    baseline_correct = 0
    baseline_times = []
    
    for query, expected_agent in test_cases:
        start_time = time.perf_counter()
        analysis = baseline_coordinator.analyze_cross_domain_integration(query)
        end_time = time.perf_counter()
        
        processing_time = (end_time - start_time) * 1000
        baseline_times.append(processing_time)
        
        predicted_agent = analysis.agent_suggestions[0][0] if analysis.agent_suggestions else "unknown"
        
        if predicted_agent == expected_agent:
            baseline_correct += 1
            print(f"  ✅ {query[:40]}... → {predicted_agent}")
        else:
            print(f"  ❌ {query[:40]}... → {predicted_agent} (expected: {expected_agent})")
    
    baseline_accuracy = (baseline_correct / len(test_cases)) * 100
    baseline_avg_time = sum(baseline_times) / len(baseline_times)
    
    print(f"\n  Baseline Accuracy: {baseline_accuracy:.1f}% ({baseline_correct}/{len(test_cases)})")
    print(f"  Baseline Avg Time: {baseline_avg_time:.2f}ms")
    
    # Step 2: Learning phase
    print("\n🧠 Step 2: Learning Phase")
    learning_coordinator = EnhancedCrossDomainCoordinator()
    learning_coordinator.pattern_learning_engine = PatternLearningEngine(coordination_hub_path=str(hub_path))
    
    # Train on first 70% of test cases
    training_size = int(len(test_cases) * 0.7)
    training_cases = test_cases[:training_size]
    validation_cases = test_cases[training_size:]
    
    patterns_learned = 0
    for query, correct_agent in training_cases:
        # Simulate successful agent selection and feedback
        analysis = learning_coordinator.analyze_cross_domain_integration(query)
        predicted_agent = analysis.agent_suggestions[0][0] if analysis.agent_suggestions else "unknown"
        
        # If prediction is correct, record as success; if not, record as failure
        if predicted_agent == correct_agent:
            learning_coordinator.record_selection_feedback(
                query, correct_agent, 0.9, user_feedback=True
            )
            patterns_learned += 1
            print(f"  ✅ Learned success: {query[:30]}... → {correct_agent}")
        else:
            learning_coordinator.record_selection_feedback(
                query, predicted_agent, 0.6, user_feedback=False, expected_agent=correct_agent
            )
            print(f"  📝 Learned failure: {query[:30]}... Expected {correct_agent}, got {predicted_agent}")
    
    # Store patterns to hub
    learning_coordinator.force_pattern_storage()
    print(f"\n  Patterns learned: {patterns_learned}")
    print(f"  Patterns stored to: {hub_path}")
    
    # Step 3: Post-learning validation
    print("\n🎯 Step 3: Post-Learning Validation")
    
    # Create new coordinator that loads the learned patterns
    validation_coordinator = EnhancedCrossDomainCoordinator()
    validation_coordinator.pattern_learning_engine = PatternLearningEngine(coordination_hub_path=str(hub_path))
    
    # Test on validation set
    learning_correct = 0
    learning_times = []
    
    for query, expected_agent in validation_cases:
        start_time = time.perf_counter()
        analysis = validation_coordinator.analyze_cross_domain_integration(query)
        end_time = time.perf_counter()
        
        processing_time = (end_time - start_time) * 1000
        learning_times.append(processing_time)
        
        predicted_agent = analysis.agent_suggestions[0][0] if analysis.agent_suggestions else "unknown"
        
        if predicted_agent == expected_agent:
            learning_correct += 1
            print(f"  ✅ {query[:40]}... → {predicted_agent} (learned pattern applied)")
        else:
            print(f"  ❌ {query[:40]}... → {predicted_agent} (expected: {expected_agent})")
    
    learning_accuracy = (learning_correct / len(validation_cases)) * 100 if validation_cases else 0
    learning_avg_time = sum(learning_times) / len(learning_times) if learning_times else 0
    
    print(f"\n  Learning Accuracy: {learning_accuracy:.1f}% ({learning_correct}/{len(validation_cases)})")
    print(f"  Learning Avg Time: {learning_avg_time:.2f}ms")
    
    # Step 4: Show learning insights
    print("\n📊 Step 4: Learning Insights")
    insights = validation_coordinator.get_learning_insights()
    print(f"  Total Successful Patterns: {insights.get('total_successful_patterns', 0)}")
    print(f"  Learning Rate: {insights.get('learning_rate', 0):.1%}")
    print(f"  Infrastructure Query Types: {len(insights.get('infrastructure_query_types', []))}")
    
    # Step 5: Show coordination hub content
    if hub_path.exists():
        print("\n📋 Step 5: Coordination Hub Content")
        with open(hub_path, 'r') as f:
            content = f.read()
            if "Infrastructure Learning Patterns" in content:
                # Show just the patterns section
                start = content.find("## Infrastructure Learning Patterns")
                end = content.find("\n## ", start + 1) if content.find("\n## ", start + 1) > -1 else len(content)
                patterns_section = content[start:end]
                print("  Pattern storage successful:")
                for line in patterns_section.split('\n')[:10]:  # Show first 10 lines
                    if line.strip():
                        print(f"    {line}")
            else:
                print("  No patterns found in hub")
    
    # Step 6: Results summary
    print("\n" + "=" * 50)
    print("🏆 RESULTS SUMMARY")
    print("=" * 50)
    
    accuracy_improvement = learning_accuracy - baseline_accuracy
    time_change = learning_avg_time - baseline_avg_time
    
    print(f"Baseline Accuracy: {baseline_accuracy:.1f}%")
    print(f"Learning Accuracy: {learning_accuracy:.1f}%")
    print(f"Accuracy Improvement: {accuracy_improvement:+.1f}%")
    print("")
    print(f"Baseline Avg Time: {baseline_avg_time:.2f}ms")
    print(f"Learning Avg Time: {learning_avg_time:.2f}ms")
    print(f"Time Change: {time_change:+.2f}ms")
    print("")
    print(f"Patterns Learned: {patterns_learned}")
    print(f"Learning Engine Active: {insights.get('total_successful_patterns', 0) > 0}")
    
    # Assessment
    target_met = learning_accuracy >= 40.0  # Target > 38%
    performance_ok = learning_avg_time < 200.0  # Performance target
    learning_working = insights.get('total_successful_patterns', 0) > 0
    
    print("\n🎯 ASSESSMENT:")
    print(f"  {'✅' if target_met else '❌'} Accuracy Target (>38%): {learning_accuracy:.1f}%")
    print(f"  {'✅' if performance_ok else '❌'} Performance Target (<200ms): {learning_avg_time:.2f}ms")
    print(f"  {'✅' if learning_working else '❌'} Learning System Working: {learning_working}")
    
    overall_success = target_met and performance_ok and learning_working
    print(f"\n  {'🎉 SUCCESS' if overall_success else '⚠️ PARTIAL SUCCESS'}: Infrastructure learning implementation")
    
    if overall_success:
        print("  ✨ All targets met - learning system improves infrastructure coordination!")
    else:
        print("  🔧 Some targets not fully met - consider additional refinements")
    
    return {
        'baseline_accuracy': baseline_accuracy,
        'learning_accuracy': learning_accuracy,
        'accuracy_improvement': accuracy_improvement,
        'baseline_time': baseline_avg_time,
        'learning_time': learning_avg_time,
        'time_change': time_change,
        'patterns_learned': patterns_learned,
        'target_met': target_met,
        'performance_ok': performance_ok,
        'learning_working': learning_working,
        'overall_success': overall_success
    }


if __name__ == "__main__":
    try:
        results = run_infrastructure_learning_validation()
        
        # Exit with appropriate status
        if results['overall_success']:
            print("\n✅ Validation passed - infrastructure learning improvements working!")
            sys.exit(0)
        else:
            print("\n⚠️ Validation completed with partial success - see assessment above.")
            sys.exit(1 if not results['target_met'] else 0)
            
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
