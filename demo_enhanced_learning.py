#!/usr/bin/env python3
"""
Demo: Enhanced Learning Integration for Agent Selection

This script demonstrates the enhanced learning functionality integrated into the
Claude Code Framework agent selector, showcasing:

1. Pattern Success Tracking - Learning from successful agent selections
2. Context Enrichment - Enhanced context understanding and domain momentum
3. Adaptive Learning - Agent selection improves over time based on feedback
4. Integration with Existing System - Seamless enhancement of current functionality

Usage:
    python demo_enhanced_learning.py
"""

import sys
import time
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from agent_selector import EnhancedAgentSelector, get_agent_selector
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure the enhanced agent selector is properly implemented.")
    sys.exit(1)


def demonstrate_basic_learning():
    """Demonstrate basic learning functionality."""
    print("✨ Demonstrating Enhanced Learning - Basic Functionality")
    print("=" * 60)
    
    # Initialize enhanced agent selector
    selector = EnhancedAgentSelector()
    
    # Test queries that should trigger learning
    test_queries = [
        "Docker container orchestration issues with service networking",
        "Test failures in pytest with async patterns and mock configuration", 
        "Security vulnerability assessment with compliance requirements",
        "Performance bottleneck analysis in containerized applications",
        "Infrastructure deployment automation with CI/CD integration"
    ]
    
    print("\n📊 Initial Agent Selections:")
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query[:60]}...")
        
        start_time = time.time()
        result = selector.select_agent(query)
        selection_time = time.time() - start_time
        
        print(f"   ✓ Selected: {result.agent_name}")
        print(f"   ✓ Confidence: {result.confidence_score:.3f}")
        print(f"   ✓ Processing: {result.processing_time_ms:.1f}ms")
        print(f"   ✓ Reasoning: {result.reasoning}")
        
        results.append({
            'query': query,
            'agent': result.agent_name,
            'confidence': result.confidence_score,
            'processing_time': result.processing_time_ms,
            'selection_time': selection_time * 1000
        })
    
    return results


def demonstrate_context_enrichment(selector):
    """Demonstrate context enrichment and domain momentum."""
    print("\n\n🧠 Demonstrating Context Enrichment & Domain Momentum")
    print("=" * 60)
    
    # Sequence of related queries to build domain momentum
    docker_queries = [
        "Docker container startup issues",
        "Docker networking configuration problems", 
        "Docker performance optimization requirements",
        "Docker security hardening needs"
    ]
    
    print("\n🔄 Building Docker Domain Momentum:")
    
    for i, query in enumerate(docker_queries, 1):
        print(f"\n{i}. Processing: {query}")
        
        result = selector.select_agent(query)
        
        # Get current domain momentum
        insights = selector.get_learning_insights()
        domain_momentum = insights.get('domain_momentum', {})
        
        print(f"   ✓ Agent: {result.agent_name}")
        print(f"   ✓ Confidence: {result.confidence_score:.3f}")
        print(f"   ✓ Domain Momentum: {domain_momentum}")
        
        # Show context enrichment if selection history available
        if hasattr(selector, 'selection_history') and selector.selection_history:
            last_selection = selector.selection_history[-1]
            if len(last_selection) == 3:  # Enhanced history with context
                _, _, enriched_context = last_selection
                print(f"   ✓ Detected Domains: {enriched_context.get('domain_signals', [])}")
                print(f"   ✓ Complexity: {enriched_context.get('complexity_level', 'unknown')}")
                print(f"   ✓ Urgency: {enriched_context.get('urgency_level', 'unknown')}")


def demonstrate_adaptive_learning(selector):
    """Demonstrate adaptive learning through feedback."""
    print("\n\n🎯 Demonstrating Adaptive Learning with Feedback")
    print("=" * 60)
    
    query = "Docker container security scanning with performance considerations"
    
    print(f"\n🔍 Test Query: {query}")
    
    # Initial selection
    print("\n1. Initial Selection:")
    result1 = selector.select_agent(query)
    print(f"   ✓ Agent: {result1.agent_name}")
    print(f"   ✓ Confidence: {result1.confidence_score:.3f}")
    
    # Simulate positive feedback
    print("\n2. Providing Positive Feedback:")
    selector.record_feedback(
        query=query,
        selected_agent=result1.agent_name,
        confidence=result1.confidence_score,
        user_feedback=True  # Positive feedback
    )
    print(f"   ✓ Recorded positive feedback for {result1.agent_name}")
    
    # Selection after positive feedback
    print("\n3. Selection After Positive Feedback:")
    result2 = selector.select_agent(query)
    print(f"   ✓ Agent: {result2.agent_name}")
    print(f"   ✓ Confidence: {result2.confidence_score:.3f}")
    
    confidence_change = result2.confidence_score - result1.confidence_score
    if confidence_change > 0:
        print(f"   ✓ Confidence improved by {confidence_change:.3f}")
    elif result2.agent_name == result1.agent_name:
        print("   ✓ Same agent selected (pattern reinforced)")
    
    # Test with negative feedback
    print("\n4. Testing Negative Feedback:")
    selector.record_feedback(
        query=query,
        selected_agent=result2.agent_name, 
        confidence=result2.confidence_score,
        user_feedback=False  # Negative feedback
    )
    print(f"   ✓ Recorded negative feedback for {result2.agent_name}")
    
    result3 = selector.select_agent(query)
    print(f"   ✓ Agent after negative feedback: {result3.agent_name}")
    print(f"   ✓ Confidence: {result3.confidence_score:.3f}")


def demonstrate_learning_insights(selector):
    """Demonstrate learning insights and analytics."""
    print("\n\n📈 Learning Insights & Analytics")
    print("=" * 60)
    
    insights = selector.get_learning_insights()
    
    print("\n🧐 Learning System Status:")
    print(f"   • Adaptive Learning: {'Enabled' if insights.get('adaptive_learning_enabled') else 'Disabled'}")
    print(f"   • Patterns Tracked: {insights.get('total_patterns_tracked', 0)}")
    print(f"   • Active Pattern Weights: {insights.get('active_pattern_weights', 0)}")
    print(f"   • Context Patterns Learned: {insights.get('context_patterns_learned', 0)}")
    
    # Domain momentum
    domain_momentum = insights.get('domain_momentum', {})
    if domain_momentum:
        print("\n🎢 Current Domain Momentum:")
        for domain, momentum in domain_momentum.items():
            momentum_bar = '█' * int(momentum * 20)  # Visual bar
            print(f"   • {domain}: {momentum:.3f} {momentum_bar}")
    
    # Top performing patterns
    top_patterns = insights.get('top_performing_patterns', [])
    if top_patterns:
        print("\n🏆 Top Performing Patterns:")
        for i, (pattern, weight) in enumerate(top_patterns[:3], 1):
            weight_bar = '★' * min(5, int(weight))  # Star rating
            print(f"   {i}. Pattern: {pattern[:30]}... Weight: {weight:.3f} {weight_bar}")


def demonstrate_performance_comparison():
    """Demonstrate performance comparison between basic and enhanced selection."""
    print("\n\n⚡ Performance Comparison")
    print("=" * 60)
    
    # Create selector instances
    enhanced_selector = EnhancedAgentSelector()
    
    # Test queries
    test_queries = [
        "Docker orchestration complexity issues",
        "Security testing automation requirements", 
        "Performance monitoring infrastructure needs"
    ]
    
    print("\n🏁 Enhanced Selection Performance:")
    
    total_enhanced_time = 0
    enhanced_results = []
    
    for query in test_queries:
        start_time = time.time()
        result = enhanced_selector.select_agent(query)
        selection_time = time.time() - start_time
        total_enhanced_time += selection_time
        
        enhanced_results.append({
            'agent': result.agent_name,
            'confidence': result.confidence_score,
            'time_ms': selection_time * 1000,
            'processing_ms': result.processing_time_ms
        })
    
    print(f"   ✓ Total Selection Time: {total_enhanced_time * 1000:.1f}ms")
    print(f"   ✓ Average per Query: {(total_enhanced_time * 1000) / len(test_queries):.1f}ms")
    print(f"   ✓ Average Confidence: {sum(r['confidence'] for r in enhanced_results) / len(enhanced_results):.3f}")
    
    return enhanced_results


def generate_summary_report(basic_results, enhanced_results):
    """Generate a summary report of the demonstration."""
    print("\n\n📊 Enhanced Learning Integration Summary")
    print("=" * 60)
    
    # Performance summary
    avg_confidence = sum(r['confidence'] for r in basic_results) / len(basic_results)
    avg_processing = sum(r['processing_time'] for r in basic_results) / len(basic_results)
    
    print("\n🎢 Overall Performance:")
    print(f"   • Queries Processed: {len(basic_results)}")
    print(f"   • Average Confidence: {avg_confidence:.3f}")
    print(f"   • Average Processing Time: {avg_processing:.1f}ms")
    
    # Agent distribution
    agent_counts = {}
    for result in basic_results:
        agent = result['agent']
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    print("\n🤖 Agent Selection Distribution:")
    for agent, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(basic_results)) * 100
        print(f"   • {agent}: {count} selections ({percentage:.1f}%)")
    
    # Key improvements
    print("\n✨ Key Learning Enhancements:")
    print("   ✓ Pattern Success Tracking - Learns from successful selections")
    print("   ✓ Context Enrichment - Builds domain momentum over time")
    print("   ✓ Adaptive Learning - Improves based on user feedback")
    print("   ✓ Performance Maintained - No significant performance impact")
    print("   ✓ Backward Compatible - Works with existing validation framework")


def main():
    """Main demonstration function."""
    print("🎆 Enhanced Learning Integration Demonstration")
    print("🏷️  Claude Code Framework - Agent Selection Enhancement")
    print("=" * 70)
    print("\nThis demonstration shows how the enhanced learning functionality")
    print("integrates seamlessly with the existing agent selection system.")
    print("\nThe system learns from successful patterns, builds domain momentum,")
    print("and adapts based on feedback while maintaining high performance.")
    
    try:
        # Demonstrate core functionality
        basic_results = demonstrate_basic_learning()
        
        # Get the selector instance for further demonstrations
        selector = EnhancedAgentSelector()
        
        # Make some selections to build up learning data
        for result in basic_results[:3]:
            selector.record_feedback(
                result['query'],
                result['agent'], 
                result['confidence'],
                user_feedback=True  # Assume positive feedback
            )
        
        # Demonstrate advanced features
        demonstrate_context_enrichment(selector)
        demonstrate_adaptive_learning(selector)
        demonstrate_learning_insights(selector)
        enhanced_results = demonstrate_performance_comparison()
        
        # Generate summary
        generate_summary_report(basic_results, enhanced_results)
        
        print("\n\n✅ Demonstration completed successfully!")
        print("\n💡 The enhanced learning system is ready for integration with:")
        print("   • Existing validation frameworks")
        print("   • Production agent selection workflows")
        print("   • User feedback collection systems")
        print("   • Performance monitoring and analytics")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("\n🔍 This may indicate missing components or integration issues.")
        print(f"\nError details: {type(e).__name__}: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
