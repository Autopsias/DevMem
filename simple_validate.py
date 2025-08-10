#!/usr/bin/env python3
"""Simple framework health validation without external dependencies."""

import os
import re
from pathlib import Path

def validate_framework():
    """Validate basic framework health."""
    print("=== Claude Code Framework Health Validation ===")
    
    # Check .claude directory
    claude_dir = Path('.claude')
    if not claude_dir.exists():
        print("❌ .claude directory not found")
        return False
        
    # Check agents directory
    agents_dir = claude_dir / 'agents'
    if not agents_dir.exists():
        print("❌ .claude/agents directory not found")
        return False
        
    # Count agents
    agent_files = list(agents_dir.glob('*.md'))
    secondary_files = list((agents_dir / 'secondary').glob('*.md')) if (agents_dir / 'secondary').exists() else []
    
    print(f"✅ Primary agents: {len(agent_files)}")
    print(f"✅ Secondary agents: {len(secondary_files)}")
    print(f"✅ Total agents: {len(agent_files) + len(secondary_files)}")
    
    # Check Claude Code compliance patterns
    compliant_agents = 0
    total_agents = len(agent_files) + len(secondary_files)
    
    for agent_file in agent_files + secondary_files:
        try:
            content = agent_file.read_text()
            if 'Use PROACTIVELY' in content:
                compliant_agents += 1
        except Exception as e:
            print(f"⚠️  Error reading {agent_file}: {e}")
    
    compliance_rate = (compliant_agents / total_agents) * 100 if total_agents > 0 else 0
    print(f"✅ Claude Code compliance: {compliant_agents}/{total_agents} ({compliance_rate:.1f}%)")
    
    # Check coordination data
    coord_dir = claude_dir / 'coordination_data'
    if coord_dir.exists():
        patterns_file = coord_dir / 'patterns.json'
        events_file = coord_dir / 'events.json'
        
        if patterns_file.exists():
            print("✅ Coordination patterns file exists")
        if events_file.exists():
            print("✅ Coordination events file exists")
    
    # Check logs
    logs_dir = claude_dir / 'logs'
    if logs_dir.exists():
        log_files = list(logs_dir.glob('*.log'))
        print(f"✅ Log files: {len(log_files)}")
    
    # Check framework initialization
    init_file = claude_dir / 'framework_initialized'
    if init_file.exists():
        print("✅ Framework initialized")
    
    print("\n=== Framework Health Summary ===")
    if compliance_rate >= 95:
        print("🟢 EXCELLENT: Framework is healthy and compliant")
    elif compliance_rate >= 80:
        print("🟡 GOOD: Framework is mostly healthy")
    else:
        print("🔴 NEEDS ATTENTION: Framework compliance issues detected")
    
    return compliance_rate >= 80

def test_agent_spawning():
    """Test basic agent spawning patterns."""
    print("\n=== Testing Agent Spawning Capability ===")
    
    # Check if we can import Task (this would fail if not available)
    try:
        # We'll just check if the agent files have proper structure
        agents_dir = Path('.claude/agents')
        test_agents = ['test-specialist.md', 'code-quality-specialist.md', 'digdeep.md']
        
        found_agents = 0
        for agent in test_agents:
            if (agents_dir / agent).exists():
                found_agents += 1
                print(f"✅ Found {agent}")
            else:
                print(f"❌ Missing {agent}")
        
        print(f"✅ Core agents available: {found_agents}/{len(test_agents)}")
        
        # Check for Task coordination patterns in agents
        task_pattern_count = 0
        for agent_file in agents_dir.glob('*.md'):
            try:
                content = agent_file.read_text()
                if 'Task(' in content:
                    task_pattern_count += 1
            except:
                pass
        
        print(f"✅ Agents with Task coordination: {task_pattern_count}")
        
        if found_agents >= 2 and task_pattern_count > 0:
            print("🟢 Agent spawning capability: READY")
            return True
        else:
            print("🔴 Agent spawning capability: LIMITED")
            return False
            
    except Exception as e:
        print(f"❌ Agent spawning test failed: {e}")
        return False

if __name__ == '__main__':
    framework_healthy = validate_framework()
    spawning_ready = test_agent_spawning()
    
    print("\n=== Overall Status ===")
    if framework_healthy and spawning_ready:
        print("🟢 FRAMEWORK STATUS: HEALTHY - All systems operational")
        exit(0)
    elif framework_healthy:
        print("🟡 FRAMEWORK STATUS: PARTIAL - Framework healthy, spawning limited")
        exit(0)
    else:
        print("🔴 FRAMEWORK STATUS: NEEDS ATTENTION - Issues detected")
        exit(1)
