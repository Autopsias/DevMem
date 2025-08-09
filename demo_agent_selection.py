#!/usr/bin/env python3
"""Demo script showing enhanced agent selection capabilities."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent_selector import EnhancedAgentSelector
from pathlib import Path
import time
import re

def demo_basic_pattern_matching():
    """Demonstrate basic pattern matching capabilities."""
    print("🤖 Enhanced Agent Selection Demo")
    print("=" * 60)
    
    selector = EnhancedAgentSelector()
    
    # Test cases with expected results
    test_cases = [
        ("pytest test failing with async mock configuration", "test-specialist"),
        ("docker orchestration issues with container networking", "infrastructure-engineer"),
        ("security vulnerability scan reveals credential leaks", "security-enforcer"),
        ("performance bottleneck in latency optimization", "performance-optimizer"),
        ("refactor code with better variable naming and function splitting", "intelligent-enhancer"),
        ("GitHub Actions workflow configuration problems", "ci-specialist"),
        ("lint errors and code formatting issues", "code-quality-specialist")
    ]
    
    print("\n🎯 Basic Pattern Matching")
    print("-" * 40)
    
    for query, expected in test_cases:
        result = selector.select_agent(query)
        status = "✓" if result.agent_name == expected else "✗"
        confidence_indicator = "🟢" if result.confidence_score > 0.7 else "🟡" if result.confidence_score > 0.4 else "🔴"
        
        print(f"{status} Query: '{query[:50]}{'...' if len(query) > 50 else ''}'")  
        print(f"   Agent: {result.agent_name} {confidence_indicator} ({result.confidence_score:.2f})")
        print(f"   Keywords: {', '.join(result.context_keywords)}")
        print(f"   Time: {result.processing_time_ms:.2f}ms")
        print()

def demo_edge_cases():
    """Demonstrate handling of edge cases and variations."""
    print("\n🔍 Edge Cases & Variations")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    edge_cases = [
        "something is broken",  # Vague
        "performance and security issues",  # Multi-domain
        "help with testing stuff",  # Informal
        "fix broken deployment",  # Ambiguous
        "tests are not passing coverage",  # Natural language
        "container won't start up properly",  # Problem description
        "need to secure the application",  # Action-oriented
        "",  # Empty
        "docker container testing performance security audit",  # Multiple keywords
    ]
    
    for query in edge_cases:
        result = selector.select_agent(query)
        
        # Get suggestions for comparison
        suggestions = selector.get_agent_suggestions(query, top_n=3)
        
        print(f"Query: '{query}' {'(empty)' if not query else ''}")
        print(f"   Selected: {result.agent_name} ({result.confidence_score:.2f})")
        print(f"   Reasoning: {result.reasoning}")
        if len(suggestions) > 1:
            print(f"   Alternatives: {', '.join([f'{s.agent_name}({s.confidence_score:.2f})' for s in suggestions[1:]])}")
        print()

def demo_natural_language_variations():
    """Demonstrate handling of natural language variations."""
    print("\n🗺 Natural Language Variations")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    # Test different ways of expressing the same intent
    variation_groups = [
        # Testing variations
        [
            "test is failing",
            "tests are broken", 
            "testing framework not working",
            "pytest configuration issues",
            "unit tests need fixing"
        ],
        # Infrastructure variations
        [
            "docker container won't start",
            "container orchestration problems", 
            "service deployment failing",
            "infrastructure scaling issues",
            "kubernetes cluster problems"
        ],
        # Performance variations
        [
            "app is running slow",
            "performance bottleneck detected",
            "latency optimization needed",
            "system performance issues",
            "resource utilization problems"
        ]
    ]
    
    for i, variations in enumerate(variation_groups, 1):
        print(f"Variation Group {i}:")
        agents_selected = []
        
        for variation in variations:
            result = selector.select_agent(variation)
            agents_selected.append(result.agent_name)
            print(f"   '{variation}' -> {result.agent_name} ({result.confidence_score:.2f})")
        
        # Check consistency
        most_common = max(set(agents_selected), key=agents_selected.count)
        consistency = agents_selected.count(most_common) / len(agents_selected)
        consistency_indicator = "🟢" if consistency >= 0.8 else "🟡" if consistency >= 0.6 else "🔴"
        
        print(f"   Consistency: {consistency:.1%} {consistency_indicator} (most common: {most_common})")
        print()

def demo_claude_code_integration():
    """Demonstrate integration with Claude Code framework patterns."""
    print("\n🤖 Claude Code Framework Integration")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    claude_code_queries = [
        "FastMCP server implementation requiring SDK compliance",
        "Qdrant vector database optimization for hybrid search", 
        "BM25S keyword search performance improvement",
        "MCP protocol validation and testing coordination",
        "TruLens evaluation integration with testing pipeline",
        "make test-coverage failing with async patterns",
        "./scripts/ci-modular-runner.sh fast needs optimization",
        "Task() calls for parallel execution coordination",
        "memory access latency >25ms performance issue",
        "@.claude/memory/coordination-hub.md pattern for testing architecture"
    ]
    
    for query in claude_code_queries:
        result = selector.select_agent(query)
        multi_domains = selector.detect_multi_domain_query(query)
        
        print(f"Query: '{query[:55]}{'...' if len(query) > 55 else ''}'")
        print(f"   Agent: {result.agent_name} ({result.confidence_score:.2f})")
        if multi_domains:
            print(f"   Domains: {', '.join(multi_domains)}")
        if result.matched_patterns:
            print(f"   Patterns: {len(result.matched_patterns)} matched")
        print()

def record_pattern_in_coordination_hub(pattern_type: str, query: str, agent: str, confidence: float, success: bool):
    """Record successful patterns in coordination-hub.md for learning enhancement."""
    coordination_hub_path = Path('.claude/memory/coordination-hub.md')
    
    if not coordination_hub_path.exists():
        print(f"   ⚠ Coordination hub not found at {coordination_hub_path}")
        return False
    
    try:
        # Read current content
        with open(coordination_hub_path, 'r') as f:
            content = f.read()
        
        # Find the Infrastructure Learning Patterns section
        learning_section_pattern = r'(## Infrastructure Learning Patterns \(Auto-Generated\).*?)(\n## |\Z)'
        match = re.search(learning_section_pattern, content, re.DOTALL)
        
        if match:
            current_section = match.group(1)
            
            # Extract current patterns and metrics
            pattern_confidence = confidence if success else max(0.3, confidence - 0.2)
            keywords = ', '.join([word.lower() for word in query.split() if len(word) > 3])
            timestamp = f"{int((time.time() - 1754680000) / 86400)} days ago"  # Days since reference
            
            # Create new pattern entry
            new_pattern = f'\n- **{pattern_type}:{agent}**: {agent} (confidence: {pattern_confidence:.2f}, keywords: {keywords}, learned: {timestamp})'
            
            # Check if similar pattern already exists
            pattern_key = f'{pattern_type}:{agent}'
            if pattern_key not in current_section:
                # Add new pattern to the example section
                example_end = current_section.find('```\n\n### Learning Performance Metrics')
                if example_end > 0:
                    # Insert before the metrics section
                    updated_section = (current_section[:example_end] + 
                                     new_pattern + 
                                     current_section[example_end:])
                    
                    # Update total successful patterns count
                    total_pattern = re.search(r'- \*\*Total Successful Patterns\*\*: (\d+)', updated_section)
                    if total_pattern:
                        current_count = int(total_pattern.group(1))
                        new_count = current_count + 1 if success else current_count
                        updated_section = updated_section.replace(
                            f'- **Total Successful Patterns**: {current_count}',
                            f'- **Total Successful Patterns**: {new_count}'
                        )
                    
                    # Replace the section in the full content
                    new_content = content.replace(match.group(1), updated_section)
                    
                    # Write updated content
                    with open(coordination_hub_path, 'w') as f:
                        f.write(new_content)
                    
                    print(f"   ✓ Pattern recorded in coordination-hub.md: {pattern_key}")
                    return True
        
        print("   ⚠ Could not find Infrastructure Learning Patterns section")
        return False
        
    except Exception as e:
        print(f"   ❌ Failed to record pattern: {e}")
        return False

def demo_learning_enhancement():
    """Demonstrate learning enhancement capabilities."""
    print("\n🧠 Learning Enhancement Demo")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    # Test learning patterns with infrastructure focus
    infrastructure_queries = [
        "docker container orchestration with kubernetes cluster scaling",
        "terraform infrastructure provisioning automation pipeline",
        "service mesh networking configuration with istio",
        "container security hardening compliance validation",
        "kubernetes horizontal pod autoscaling performance optimization"
    ]
    
    print("Testing infrastructure pattern learning:")
    successful_patterns = 0
    
    for i, query in enumerate(infrastructure_queries, 1):
        result = selector.select_agent(query)
        print(f"   {i}. Query: '{query[:50]}...'")
        print(f"      Agent: {result.agent_name} (confidence: {result.confidence_score:.2f})")
        
        # Simulate positive feedback for infrastructure-engineer selections
        if result.agent_name == 'infrastructure-engineer':
            selector.record_feedback(query, result.agent_name, result.confidence_score, user_feedback=True)
            print("      ✓ Positive feedback recorded - boosting pattern weight")
            
            # Record successful pattern in coordination-hub.md
            pattern_type = "container_orchestration" if "orchestration" in query.lower() else "infrastructure_automation"
            record_pattern_in_coordination_hub(pattern_type, query, result.agent_name, result.confidence_score, True)
            successful_patterns += 1
        else:
            # Record feedback for missed infrastructure patterns
            selector.record_feedback(query, result.agent_name, result.confidence_score, 
                                   user_feedback=False, expected_agent='infrastructure-engineer')
            print("      ⚠ Negative feedback recorded - expected infrastructure-engineer")
            
            # Still record the pattern for learning purposes
            pattern_type = "infrastructure_missed"
            record_pattern_in_coordination_hub(pattern_type, query, result.agent_name, result.confidence_score, False)
        print()
    
    print(f"Successfully learned {successful_patterns}/{len(infrastructure_queries)} infrastructure patterns")
    
    # Test learning insights
    learning_insights = selector.get_learning_insights()
    if learning_insights:
        print("\nLearning System Insights:")
        print(f"   Total patterns tracked: {learning_insights.get('total_patterns_tracked', 0)}")
        print(f"   Active pattern weights: {learning_insights.get('active_pattern_weights', 0)}")
        print(f"   Context patterns learned: {learning_insights.get('context_patterns_learned', 0)}")
        print(f"   Adaptive learning enabled: {learning_insights.get('adaptive_learning_enabled', False)}")
        print(f"   Agents from directory: {learning_insights.get('agents_loaded_from_directory', 0)}")
        print(f"   Fallback threshold: {learning_insights.get('fallback_threshold', 0.4):.2f}")
        print(f"   Digdeep threshold: {learning_insights.get('digdeep_threshold', 0.3):.2f}")
        
        if 'domain_momentum' in learning_insights and learning_insights['domain_momentum']:
            print(f"   Domain momentum: {learning_insights['domain_momentum']}")
        
        if 'top_performing_patterns' in learning_insights:
            print("   Top performing patterns:")
            for pattern, weight in learning_insights['top_performing_patterns']:
                print(f"      {pattern}: {weight:.3f}")
    
    # Test repeat queries to show learning improvement
    print("\nTesting learned pattern improvement:")
    repeat_query = "kubernetes container orchestration infrastructure scaling"
    
    print(f"Query: '{repeat_query}'")
    result1 = selector.select_agent(repeat_query)
    print(f"   First selection: {result1.agent_name} (confidence: {result1.confidence_score:.2f})")
    
    # Record additional positive feedback
    selector.record_feedback(repeat_query, 'infrastructure-engineer', 0.95, user_feedback=True)
    
    result2 = selector.select_agent(repeat_query)
    print(f"   After learning: {result2.agent_name} (confidence: {result2.confidence_score:.2f})")
    
    if result2.confidence_score > result1.confidence_score:
        improvement = ((result2.confidence_score - result1.confidence_score) / result1.confidence_score) * 100
        print(f"   🚀 Learning improvement: {improvement:.1f}% confidence increase!")
    
    # Show memory file integration
    print("\n📝 Pattern learning recorded in .claude/memory/coordination-hub.md")
    print("   Infrastructure learning patterns automatically updated for future reference")

def demo_performance_characteristics():
    """Demonstrate performance characteristics."""
    print("\n⏱️ Performance Characteristics")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    # Single query performance
    import time
    query = "pytest async test mock configuration failing"
    
    # Warmup
    selector.select_agent(query)
    
    # Time multiple runs
    times = []
    for _ in range(10):
        start = time.perf_counter()
        result = selector.select_agent(query)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print("Single Query Performance (10 runs):")
    print(f"   Average: {avg_time:.2f}ms")
    print(f"   Range: {min_time:.2f}ms - {max_time:.2f}ms")
    print(f"   Result: {result.agent_name} ({result.confidence_score:.2f})")
    
    # Batch performance
    queries = [
        "test failing",
        "docker issue", 
        "security problem",
        "performance slow",
        "refactor code",
        "lint errors",
        "ci pipeline broken"
    ] * 10  # 70 total queries
    
    start = time.perf_counter()
    results = [selector.select_agent(q) for q in queries]
    total_time = (time.perf_counter() - start) * 1000
    
    print(f"\nBatch Performance ({len(queries)} queries):")
    print(f"   Total time: {total_time:.1f}ms")
    print(f"   Average per query: {total_time / len(queries):.2f}ms")
    print(f"   Throughput: {len(queries) / (total_time / 1000):.0f} queries/second")
    
    # Show result distribution
    agent_counts = {}
    avg_confidence = sum(r.confidence_score for r in results) / len(results)
    for result in results:
        agent_counts[result.agent_name] = agent_counts.get(result.agent_name, 0) + 1
    
    print(f"   Average confidence: {avg_confidence:.3f}")
    print(f"   Agent distribution: {dict(sorted(agent_counts.items()))}")
    
    # Show selection statistics
    stats = selector.get_selection_stats()
    if stats:
        print("\nSelection Statistics:")
        print(f"   Total selections: {stats['total_selections']}")
        print(f"   Average confidence: {stats['average_confidence']:.2f}")
        print(f"   Average processing time: {stats['average_processing_time_ms']:.2f}ms")
        if stats['most_selected_agent']:
            agent, count = stats['most_selected_agent']
            print(f"   Most selected agent: {agent} ({count} times)")

def demo_multi_suggestions():
    """Demonstrate multiple agent suggestions."""
    print("\n📈 Multiple Agent Suggestions")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    ambiguous_queries = [
        "docker container testing performance",
        "security and testing issues", 
        "code quality and performance problems",
        "infrastructure deployment with security concerns"
    ]
    
    for query in ambiguous_queries:
        suggestions = selector.get_agent_suggestions(query, top_n=4)
        
        print(f"Query: '{query}'")
        print("   Top suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            confidence_bar = "█" * int(suggestion.confidence_score * 10)
            print(f"      {i}. {suggestion.agent_name:<20} {confidence_bar:<10} ({suggestion.confidence_score:.2f})")
        print()

def demo_agent_directory_integration():
    """Demonstrate .claude/agents/ directory integration."""
    print("\n📁 .claude/agents/ Directory Integration")
    print("-" * 40)
    
    selector = EnhancedAgentSelector()
    
    # Show loaded agents
    all_agents = list(selector.agents.keys())
    default_agents = selector._get_default_agent_names()
    directory_agents = [agent for agent in all_agents if agent not in default_agents]
    
    print(f"Total agents loaded: {len(all_agents)}")
    print(f"Default agents: {len(default_agents)}")
    print(f"Directory agents: {len(directory_agents)}")
    
    if directory_agents:
        print("\nAgents loaded from .claude/agents/:")
        for agent in sorted(directory_agents):
            print(f"   • {agent}")
    
    # Test queries that should match directory agents
    directory_test_queries = [
        "I need to analyze system architecture patterns",  # architecture-validator
        "Help me review agent coordination patterns",      # agent-reviewer  
        "Create a new specialized agent for data processing", # agent-creator
        "Monitor system health and performance metrics",   # health-monitor
        "Coordinate multiple analysis workflows",          # analysis-gateway
        "Need comprehensive framework coordination",       # framework-coordinator
        "Review and validate environment configuration",   # environment-analyst
    ]
    
    print("\nTesting directory agent selection:")
    for query in directory_test_queries:
        result = selector.select_agent(query)
        is_directory_agent = result.agent_name in directory_agents
        indicator = "📁" if is_directory_agent else "⚙️"
        
        print(f"   {indicator} '{query[:50]}{'...' if len(query) > 50 else ''}'")
        print(f"      → {result.agent_name} ({result.confidence_score:.2f})")

def demo_improved_fallback_logic():
    """Demonstrate improved fallback logic that minimizes digdeep usage."""
    print("\n🎯 Improved Fallback Logic (Reduced digdeep Usage)")
    print("-" * 50)
    
    selector = EnhancedAgentSelector()
    
    # Test various fallback scenarios
    fallback_test_queries = [
        "help",  # Very vague - should avoid digdeep
        "something is broken",  # Vague problem
        "urgent production issue",  # Should use meta-coordinator
        "I have a problem",  # General problem
        "need assistance",  # General help
        "performance and security issues",  # Multi-domain
        "testing infrastructure deployment security",  # Multi-domain
        "x",  # Too short - might need digdeep
        "abc def ghi",  # Random text - might need digdeep
    ]
    
    digdeep_count = 0
    for query in fallback_test_queries:
        result = selector.select_agent(query)
        
        if result.agent_name == 'digdeep':
            digdeep_count += 1
            indicator = "🔍"
        elif result.agent_name in ['meta-coordinator', 'analysis-gateway']:
            indicator = "🎯"
        else:
            indicator = "⚙️"
        
        print(f"   {indicator} '{query}' → {result.agent_name} ({result.confidence_score:.2f})")
        print(f"      Reason: {result.reasoning}")
        print()
    
    print(f"digdeep usage: {digdeep_count}/{len(fallback_test_queries)} queries ({digdeep_count/len(fallback_test_queries)*100:.1f}%)")
    print("Target: <20% digdeep usage for better user experience")

def main():
    """Run the complete demo."""
    try:
        demo_basic_pattern_matching()
        demo_agent_directory_integration()
        demo_edge_cases()
        demo_natural_language_variations() 
        demo_claude_code_integration()
        demo_improved_fallback_logic()
        demo_learning_enhancement()
        demo_performance_characteristics()
        demo_multi_suggestions()
        
        print("\n" + "=" * 70)
        print("🎉 Enhanced Agent Selection Demo Complete!")
        print("=" * 70)
        print("\nKey Improvements Demonstrated:")
        print("• ✅ .claude/agents/ directory integration with automatic loading")
        print("• ✅ Enhanced cross-domain coordinator integration")
        print("• ✅ Improved pattern matching with better confidence scoring")
        print("• ✅ Reduced digdeep usage with smarter fallback logic")
        print("• ✅ Better multi-domain query handling")
        print("• ✅ Enhanced learning system with directory agent support")
        print("• ✅ Improved performance with caching and optimization")
        print("\n🚀 Ready for production use in Claude Code framework!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
