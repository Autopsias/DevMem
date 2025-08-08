#!/usr/bin/env python3
"""Test import functionality for agent selection."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from agent_selector import EnhancedAgentSelector, select_best_agent, AgentMatchResult
    print("✓ Successfully imported EnhancedAgentSelector")
    print("✓ Successfully imported select_best_agent")
    print("✓ Successfully imported AgentMatchResult")
    
    # Test basic creation
    selector = EnhancedAgentSelector()
    print("✓ Successfully created EnhancedAgentSelector instance")
    
    # Test basic selection
    result = selector.select_agent("test query")
    print(f"✓ Successfully ran selection: {result.agent_name}")
    
    # Test global function
    global_result = select_best_agent("test query")
    print(f"✓ Successfully ran global function: {global_result.agent_name}")
    
    print("\n✅ All imports and basic functionality working!")
    
except Exception as e:
    print(f"❌ Import or basic functionality failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
