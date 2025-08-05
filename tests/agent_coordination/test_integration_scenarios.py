"""
Integration Testing for Agent Ecosystem (Story S6.3)

Tests integration scenarios including:
- Agent ecosystem integration scenarios
- Cross-agent communication patterns validation
- Resource usage under various coordination loads
- End-to-end workflow testing
"""

import pytest
import asyncio
import time
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import threading
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class AgentIntegrationScenario:
    """Represents an agent integration test scenario."""
    name: str
    description: str
    primary_agents: List[str]
    secondary_agents: List[str]
    coordination_type: str  # 'sequential', 'parallel', 'hybrid'
    expected_outcomes: Dict[str, Any]


class AgentEcosystemIntegrator:
    """Integration testing framework for the complete agent ecosystem."""
    
    def __init__(self):
        self.agents_dir = Path("/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/agents")
        self.memory_dir = Path("/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/memory")
        self.communication_dir = Path("/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/communication")
        
        # Load agent configurations
        self.primary_agents = self._load_primary_agents()
        self.secondary_agents = self._load_secondary_agents()
        
        # Integration test scenarios
        self.test_scenarios = self._define_integration_scenarios()
    
    def _load_primary_agents(self) -> Dict[str, Dict[str, Any]]:
        """Load primary agent configurations."""
        primary_agents = {}
        
        for agent_file in self.agents_dir.glob("*.md"):
            agent_name = agent_file.stem
            content = agent_file.read_text()
            
            primary_agents[agent_name] = {
                "file_path": agent_file,
                "content": content,
                "has_ultrathink": "UltraThink Analysis" in content,
                "has_epic4": "Epic 4:" in content,
                "coordination_patterns": self._extract_coordination_patterns(content),
                "tools": self._extract_tools(content),
                "domains": self._extract_domains(content)
            }
        
        return primary_agents
    
    def _load_secondary_agents(self) -> Dict[str, Dict[str, Any]]:
        """Load secondary agent configurations."""
        secondary_agents = {}
        secondary_dir = self.agents_dir / "secondary"
        
        if secondary_dir.exists():
            for agent_file in secondary_dir.glob("*.md"):
                agent_name = agent_file.stem
                content = agent_file.read_text()
                
                secondary_agents[agent_name] = {
                    "file_path": agent_file,
                    "content": content,
                    "specialization": self._extract_specialization(content),
                    "auto_activate_patterns": self._extract_auto_activate_patterns(content)
                }
        
        return secondary_agents
    
    def _extract_coordination_patterns(self, content: str) -> List[str]:
        """Extract coordination patterns from agent content."""
        patterns = []
        if "Sequential" in content or "sequential" in content.lower():
            patterns.append("sequential")
        if "Parallel" in content or "parallel" in content.lower():
            patterns.append("parallel")
        if "Meta" in content or "meta-coordination" in content.lower():
            patterns.append("meta")
        if "Cross-domain" in content or "Cross-Domain" in content:
            patterns.append("cross-domain")
        return patterns
    
    def _extract_tools(self, content: str) -> List[str]:
        """Extract tools from agent content."""
        tools = []
        # Look for tool mentions in content
        tool_indicators = ["Read", "Edit", "Bash", "Grep", "Task", "WebFetch", "mcp__"]
        for tool in tool_indicators:
            if tool in content:
                tools.append(tool)
        return tools
    
    def _extract_domains(self, content: str) -> List[str]:
        """Extract domain expertise from agent content."""
        domains = []
        domain_keywords = {
            "testing": ["test", "testing", "pytest", "coverage"],
            "infrastructure": ["docker", "container", "deployment", "infrastructure"],
            "security": ["security", "vulnerability", "threat", "audit"],
            "performance": ["performance", "optimization", "benchmark", "efficiency"],
            "development": ["development", "coding", "implementation", "refactor"],
            "ci": ["ci", "pipeline", "github actions", "automation"],
            "quality": ["quality", "linting", "standards", "validation"]
        }
        
        content_lower = content.lower()
        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                domains.append(domain)
        
        return domains
    
    def _extract_specialization(self, content: str) -> str:
        """Extract specialization from secondary agent content."""
        if "async" in content.lower():
            return "async-patterns"
        elif "type" in content.lower():
            return "type-system"
        elif "mock" in content.lower():
            return "mocking"
        elif "docker" in content.lower():
            return "containerization"
        elif "performance" in content.lower():
            return "performance-optimization"
        else:
            return "general"
    
    def _extract_auto_activate_patterns(self, content: str) -> List[str]:
        """Extract auto-activation patterns from secondary agent content."""
        patterns = []
        if "Auto-Activate" in content:
            # Extract patterns between "Auto-Activate" and next section
            lines = content.split('\n')
            in_auto_activate = False
            for line in lines:
                if "Auto-Activate" in line:
                    in_auto_activate = True
                elif in_auto_activate and line.startswith('#'):
                    break
                elif in_auto_activate and '-' in line and '→' in line:
                    pattern = line.split('→')[0].strip().strip('-').strip()
                    patterns.append(pattern)
        return patterns
    
    def _define_integration_scenarios(self) -> List[AgentIntegrationScenario]:
        """Define comprehensive integration test scenarios."""
        return [
            AgentIntegrationScenario(
                name="testing_workflow_integration",
                description="End-to-end testing workflow with multiple agent types",
                primary_agents=["test-specialist", "analysis-gateway", "synthesis-coordinator"],
                secondary_agents=["async-pattern-fixer", "mock-configuration-expert", "coverage-optimizer"],
                coordination_type="sequential",
                expected_outcomes={
                    "coordination_success": True,
                    "context_preservation": True,
                    "specialized_expertise": True
                }
            ),
            AgentIntegrationScenario(
                name="infrastructure_performance_coordination",
                description="Infrastructure and performance analysis coordination",
                primary_agents=["infrastructure-engineer", "meta-coordinator"],
                secondary_agents=["docker-specialist", "performance-optimizer", "resource-optimizer"],
                coordination_type="parallel",
                expected_outcomes={
                    "parallel_execution": True,
                    "resource_optimization": True,
                    "cross_domain_integration": True
                }
            ),
            AgentIntegrationScenario(
                name="security_quality_analysis",
                description="Security and quality analysis with conflict resolution",
                primary_agents=["security-enforcer", "code-quality-specialist", "synthesis-coordinator"],
                secondary_agents=["security-auditor", "pattern-analyzer"],
                coordination_type="hybrid",
                expected_outcomes={
                    "conflict_resolution": True,
                    "unified_solution": True,
                    "security_quality_balance": True
                }
            ),
            AgentIntegrationScenario(
                name="development_lifecycle_integration",
                description="Complete development lifecycle with git integration",
                primary_agents=["intelligent-enhancer", "git-commit-assistant", "test-specialist"],
                secondary_agents=["type-system-expert", "linting-engineer", "validation-tester"],
                coordination_type="sequential",
                expected_outcomes={
                    "lifecycle_completion": True,
                    "quality_validation": True,
                    "git_integration": True
                }
            ),
            AgentIntegrationScenario(
                name="crisis_response_coordination",
                description="Multi-domain crisis response with meta-coordination",
                primary_agents=["meta-coordinator", "analysis-gateway", "synthesis-coordinator"],
                secondary_agents=["docker-specialist", "security-auditor", "performance-optimizer"],
                coordination_type="parallel",
                expected_outcomes={
                    "rapid_response": True,
                    "multi_domain_analysis": True,
                    "strategic_coordination": True
                }
            )
        ]


@pytest.fixture
def ecosystem_integrator():
    """Fixture providing agent ecosystem integrator."""
    return AgentEcosystemIntegrator()


class TestAgentEcosystemIntegration:
    """Test complete agent ecosystem integration."""
    
    def test_ecosystem_completeness(self, ecosystem_integrator):
        """Test that the complete 34-agent ecosystem is accessible across all agent types."""
        integrator = ecosystem_integrator
        
        total_agents = len(integrator.primary_agents) + len(integrator.secondary_agents)
        
        # Validate ecosystem completeness
        assert len(integrator.primary_agents) >= 15, f"Should have at least 15 primary agents, found {len(integrator.primary_agents)}"
        assert len(integrator.secondary_agents) >= 15, f"Should have at least 15 secondary agents, found {len(integrator.secondary_agents)}"
        assert total_agents >= 30, f"Should have at least 30 total agents, found {total_agents}"
        
        # Validate key agents exist
        key_primary_agents = ["test-specialist", "infrastructure-engineer", "meta-coordinator", "synthesis-coordinator"]
        for agent_name in key_primary_agents:
            assert agent_name in integrator.primary_agents, f"Key primary agent {agent_name} should exist"
        
        key_secondary_agents = ["async-pattern-fixer", "docker-specialist", "performance-optimizer"]
        for agent_name in key_secondary_agents:
            assert agent_name in integrator.secondary_agents, f"Key secondary agent {agent_name} should exist"
    
    def test_agent_configuration_integrity(self, ecosystem_integrator):
        """Test integrity of agent configurations."""
        integrator = ecosystem_integrator
        
        # Test primary agents
        for agent_name, config in integrator.primary_agents.items():
            assert config["content"], f"Primary agent {agent_name} should have content"
            assert config["file_path"].exists(), f"Primary agent {agent_name} file should exist"
            
            # UltraThink Analysis should be present in most primary agents
            if agent_name not in ["token-monitor", "user-feedback-coordinator"]:  # Some may not have UltraThink
                assert config["has_ultrathink"] or config["has_epic4"], \
                    f"Primary agent {agent_name} should have UltraThink or Epic 4 patterns"
        
        # Test secondary agents
        for agent_name, config in integrator.secondary_agents.items():
            assert config["content"], f"Secondary agent {agent_name} should have content"
            assert config["file_path"].exists(), f"Secondary agent {agent_name} file should exist"
            assert config["specialization"], f"Secondary agent {agent_name} should have specialization"
    
    def test_cross_domain_capabilities(self, ecosystem_integrator):
        """Test cross-domain capabilities across the ecosystem."""
        integrator = ecosystem_integrator
        
        # Collect all domains across agents
        all_domains = set()
        for agent_name, config in integrator.primary_agents.items():
            all_domains.update(config["domains"])
        
        # Validate domain coverage
        expected_domains = ["testing", "infrastructure", "security", "performance", "development", "quality"]
        for domain in expected_domains:
            assert domain in all_domains, f"Domain {domain} should be covered by at least one agent"
        
        # Test agents with multiple domain expertise
        multi_domain_agents = []
        for agent_name, config in integrator.primary_agents.items():
            if len(config["domains"]) > 2:
                multi_domain_agents.append(agent_name)
        
        assert len(multi_domain_agents) > 0, "Should have agents with multi-domain expertise"


class TestIntegrationScenarios:
    """Test predefined integration scenarios."""
    
    def test_testing_workflow_integration(self, ecosystem_integrator):
        """Test testing workflow integration scenario."""
        integrator = ecosystem_integrator
        scenario = next(s for s in integrator.test_scenarios if s.name == "testing_workflow_integration")
        
        # Validate agents exist
        for agent_name in scenario.primary_agents:
            assert agent_name in integrator.primary_agents, f"Primary agent {agent_name} should exist for scenario"
        
        for agent_name in scenario.secondary_agents:
            assert agent_name in integrator.secondary_agents, f"Secondary agent {agent_name} should exist for scenario"
        
        # Simulate scenario execution
        start_time = time.time()
        
        coordination_results = {}
        for agent_name in scenario.primary_agents:
            agent_config = integrator.primary_agents[agent_name]
            coordination_results[agent_name] = {
                "has_testing_domain": "testing" in agent_config["domains"],
                "coordination_capable": len(agent_config["coordination_patterns"]) > 0,
                "has_context_preservation": "Context Preservation" in agent_config["content"]
            }
        
        execution_time = time.time() - start_time
        
        # Validate scenario outcomes
        assert execution_time < 1.0, "Integration scenario should execute quickly"
        assert len(coordination_results) == len(scenario.primary_agents), "Should process all primary agents"
        
        # Validate testing expertise
        testing_agents = [name for name, result in coordination_results.items() if result["has_testing_domain"]]
        assert len(testing_agents) > 0, "Should have agents with testing domain expertise"
    
    def test_infrastructure_performance_coordination(self, ecosystem_integrator):
        """Test infrastructure and performance coordination scenario."""
        integrator = ecosystem_integrator
        scenario = next(s for s in integrator.test_scenarios if s.name == "infrastructure_performance_coordination")
        
        # Validate parallel coordination capability
        parallel_capable_agents = []
        for agent_name in scenario.primary_agents:
            agent_config = integrator.primary_agents[agent_name]
            if "parallel" in agent_config["coordination_patterns"] or "meta" in agent_config["coordination_patterns"]:
                parallel_capable_agents.append(agent_name)
        
        assert len(parallel_capable_agents) > 0, "Should have agents capable of parallel coordination"
        
        # Simulate parallel execution
        start_time = time.time()
        
        def simulate_agent_processing(agent_name):
            """Simulate agent processing."""
            agent_config = integrator.primary_agents[agent_name]
            time.sleep(0.01)  # 10ms processing simulation
            return {
                "agent": agent_name,
                "infrastructure_capable": "infrastructure" in agent_config["domains"],
                "performance_capable": "performance" in agent_config["domains"],
                "tools_available": len(agent_config["tools"]) > 0
            }
        
        # Execute agents in parallel simulation
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(simulate_agent_processing, agent_name) for agent_name in scenario.primary_agents]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        execution_time = time.time() - start_time
        
        # Validate parallel execution
        assert execution_time < 0.5, "Parallel coordination should be faster than sequential"
        assert len(results) == len(scenario.primary_agents), "Should process all agents in parallel"
        
        # Validate domain expertise
        infrastructure_agents = [r for r in results if r["infrastructure_capable"]]
        assert len(infrastructure_agents) > 0, "Should have infrastructure-capable agents"
    
    def test_security_quality_analysis_integration(self, ecosystem_integrator):
        """Test security and quality analysis integration."""
        integrator = ecosystem_integrator
        scenario = next(s for s in integrator.test_scenarios if s.name == "security_quality_analysis")
        
        # Validate conflict resolution capabilities
        conflict_resolution_agents = []
        for agent_name in scenario.primary_agents:
            agent_config = integrator.primary_agents[agent_name]
            if "Conflict Resolution" in agent_config["content"]:
                conflict_resolution_agents.append(agent_name)
        
        assert len(conflict_resolution_agents) > 0, "Should have agents with conflict resolution capabilities"
        
        # Simulate security vs quality conflicts
        security_agents = []
        quality_agents = []
        
        for agent_name in scenario.primary_agents:
            agent_config = integrator.primary_agents[agent_name]
            if "security" in agent_config["domains"]:
                security_agents.append(agent_name)
            if "quality" in agent_config["domains"]:
                quality_agents.append(agent_name)
        
        # Validate balanced expertise
        assert len(security_agents) > 0, "Should have security-focused agents"
        assert len(quality_agents) > 0, "Should have quality-focused agents"


class TestCrossDomainCommunication:
    """Test cross-domain communication patterns."""
    
    def test_communication_protocol_integration(self, ecosystem_integrator):
        """Test communication protocol integration."""
        integrator = ecosystem_integrator
        
        # Test communication directory structure
        if integrator.communication_dir.exists():
            communication_files = list(integrator.communication_dir.glob("*.md"))
            assert len(communication_files) > 0, "Should have communication protocol files"
            
            # Validate communication protocols
            protocol_types = []
            for comm_file in communication_files:
                content = comm_file.read_text()
                if "Primary Agent" in content:
                    protocol_types.append("primary")
                if "Secondary Agent" in content:
                    protocol_types.append("secondary")
                if "Cross-Domain" in content:
                    protocol_types.append("cross-domain")
            
            assert "primary" in protocol_types, "Should have primary agent communication protocols"
            assert "cross-domain" in protocol_types, "Should have cross-domain communication protocols"
    
    def test_context_management_integration(self, ecosystem_integrator):
        """Test context management across agent transitions."""
        integrator = ecosystem_integrator
        
        # Test agents with context preservation capabilities
        context_capable_agents = []
        for agent_name, config in integrator.primary_agents.items():
            if "Context Preservation" in config["content"] or "context" in config["content"].lower():
                context_capable_agents.append(agent_name)
        
        assert len(context_capable_agents) > 5, "Should have multiple agents with context preservation"
        
        # Test synthesis coordinator specifically
        if "synthesis-coordinator" in integrator.primary_agents:
            synthesis_config = integrator.primary_agents["synthesis-coordinator"]
            assert "Result Synthesis" in synthesis_config["content"], \
                "Synthesis coordinator should have result synthesis capabilities"
            assert "Multi-Agent" in synthesis_config["content"], \
                "Synthesis coordinator should handle multi-agent coordination"


class TestResourceUsageUnderLoad:
    """Test resource usage under various coordination loads."""
    
    def test_light_coordination_load(self, ecosystem_integrator):
        """Test resource usage under light coordination load."""
        integrator = ecosystem_integrator
        
        start_time = time.time()
        
        # Simulate light load - access few agents
        light_load_agents = ["test-specialist", "analysis-gateway"]
        processed_agents = {}
        
        for agent_name in light_load_agents:
            if agent_name in integrator.primary_agents:
                config = integrator.primary_agents[agent_name]
                processed_agents[agent_name] = {
                    "content_length": len(config["content"]),
                    "coordination_patterns": config["coordination_patterns"]
                }
        
        execution_time = time.time() - start_time
        
        # Validate light load performance
        assert execution_time < 0.1, "Light coordination load should execute very quickly"
        assert len(processed_agents) == len(light_load_agents), "Should process all light load agents"
    
    def test_heavy_coordination_load(self, ecosystem_integrator):
        """Test resource usage under heavy coordination load."""
        integrator = ecosystem_integrator
        
        start_time = time.time()
        
        # Simulate heavy load - access most agents
        heavy_load_agents = list(integrator.primary_agents.keys())[:10]  # First 10 primary agents
        processed_agents = {}
        
        for agent_name in heavy_load_agents:
            config = integrator.primary_agents[agent_name]
            processed_agents[agent_name] = {
                "content_length": len(config["content"]),
                "coordination_patterns": config["coordination_patterns"],
                "domains": config["domains"],
                "tools": config["tools"]
            }
            
            # Simulate some processing time
            time.sleep(0.001)  # 1ms per agent
        
        execution_time = time.time() - start_time
        
        # Validate heavy load performance
        assert execution_time < 1.0, "Heavy coordination load should still execute within reasonable time"
        assert len(processed_agents) == len(heavy_load_agents), "Should process all heavy load agents"
        
        # Validate comprehensive processing
        total_content = sum(result["content_length"] for result in processed_agents.values())
        assert total_content > 0, "Should process substantial agent content"
    
    def test_concurrent_coordination_load(self, ecosystem_integrator):
        """Test concurrent coordination scenarios."""
        integrator = ecosystem_integrator
        
        def simulate_coordination_session(session_id: int):
            """Simulate a coordination session."""
            session_agents = list(integrator.primary_agents.keys())[session_id*2:(session_id+1)*2]  # 2 agents per session
            results = {}
            
            for agent_name in session_agents:
                if agent_name in integrator.primary_agents:
                    config = integrator.primary_agents[agent_name]
                    results[agent_name] = len(config["content"])
                    time.sleep(0.005)  # 5ms processing per agent
            
            return {"session_id": session_id, "processed": len(results), "results": results}
        
        start_time = time.time()
        
        # Run 3 concurrent coordination sessions
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(simulate_coordination_session, i) for i in range(3)]
            session_results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        execution_time = time.time() - start_time
        
        # Validate concurrent execution
        assert execution_time < 0.5, "Concurrent coordination should be efficient"
        assert len(session_results) == 3, "Should complete all concurrent sessions"
        
        total_processed = sum(result["processed"] for result in session_results)
        assert total_processed > 0, "Should process agents across all sessions"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])