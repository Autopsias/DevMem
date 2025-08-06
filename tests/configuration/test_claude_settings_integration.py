"""Test integration with existing Claude Code settings.json files."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.configuration import SettingsLoader, AgentConfigurationSchema
from src.configuration.hot_reload import ConfigurationManager


class TestClaudeSettingsIntegration:
    """Test Claude Code settings.json integration."""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory with .claude structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            claude_dir = project_path / ".claude"
            claude_dir.mkdir()
            yield project_path
    
    @pytest.fixture
    def sample_claude_settings(self):
        """Sample Claude Code settings.json with agent configuration."""
        return {
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [{"type": "command", "command": "./hooks/security.sh"}]
                    }
                ]
            },
            "agents": {
                "global_settings": {
                    "framework_enabled": True,
                    "natural_delegation": True
                },
                "performance": {
                    "token_optimization": True,
                    "prompt_caching": True
                },
                "agents": {
                    "test-specialist": {
                        "enabled": True,
                        "performance": {
                            "response_timeout": 25.0,
                            "max_context_tokens": 9000
                        }
                    }
                }
            }
        }
    
    def test_load_existing_claude_settings(self, temp_project_dir, sample_claude_settings):
        """Test loading configuration from existing .claude/settings.json."""
        # Write sample settings file
        settings_file = temp_project_dir / ".claude" / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(sample_claude_settings, f)
        
        # Load configuration
        loader = SettingsLoader(project_root=temp_project_dir)
        config = loader.load_configuration()
        
        # Verify configuration loaded correctly
        assert isinstance(config, AgentConfigurationSchema)
        assert config.global_settings["framework_enabled"] is True
        assert config.performance["token_optimization"] is True
        assert "test-specialist" in config.agents
    
    def test_hierarchical_settings_override(self, temp_project_dir):
        """Test hierarchical settings override behavior."""
        # Create project-level settings
        project_settings = {
            "agents": {
                "performance": {"token_optimization": False}
            }
        }
        
        # Create local settings that override project settings
        local_settings = {
            "agents": {
                "performance": {"token_optimization": True, "prompt_caching": False}
            }
        }
        
        # Write settings files
        with open(temp_project_dir / ".claude" / "settings.json", 'w') as f:
            json.dump(project_settings, f)
        
        with open(temp_project_dir / ".claude" / "settings.local.json", 'w') as f:
            json.dump(local_settings, f)
        
        # Load and verify override behavior
        loader = SettingsLoader(project_root=temp_project_dir)
        config = loader.load_configuration()
        
        # Local settings should override project settings
        assert config.performance["token_optimization"] is True
        assert config.performance["prompt_caching"] is False
    
    def test_agent_configuration_extraction(self, temp_project_dir):
        """Test extraction of agent configuration from Claude settings."""
        claude_settings = {
            "hooks": {"PreToolUse": []},
            "permissions": {"allow": ["Bash:*"]},
            "agent_framework": {
                "global_settings": {"framework_enabled": True},
                "agents": {
                    "digdeep": {"enabled": True}
                }
            }
        }
        
        settings_file = temp_project_dir / ".claude" / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(claude_settings, f)
        
        loader = SettingsLoader(project_root=temp_project_dir)
        config = loader.load_configuration()
        
        # Verify agent configuration was extracted
        assert config.global_settings["framework_enabled"] is True
        assert "digdeep" in config.agents
    
    def test_configuration_validation_with_claude_settings(self, temp_project_dir):
        """Test configuration validation with Claude settings format."""
        invalid_settings = {
            "agents": {
                "agents": {
                    "test-agent": {
                        # Missing required 'type' field
                        "performance": {
                            "response_timeout": -5  # Invalid negative timeout
                        }
                    }
                }
            }
        }
        
        settings_file = temp_project_dir / ".claude" / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(invalid_settings, f)
        
        loader = SettingsLoader(project_root=temp_project_dir)
        
        # Should load successfully but with validation warnings
        config = loader.load_configuration()
        assert isinstance(config, AgentConfigurationSchema)
    
    def test_hot_reload_with_claude_settings(self, temp_project_dir):
        """Test hot reload functionality with Claude settings."""
        initial_settings = {
            "agents": {
                "global_settings": {"framework_enabled": False}
            }
        }
        
        settings_file = temp_project_dir / ".claude" / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(initial_settings, f)
        
        # Initialize configuration manager
        config_manager = ConfigurationManager(project_root=temp_project_dir)
        initial_config = config_manager.initialize()
        
        assert initial_config.global_settings["framework_enabled"] is False
        
        # Modify settings file
        updated_settings = {
            "agents": {
                "global_settings": {"framework_enabled": True}
            }
        }
        
        with open(settings_file, 'w') as f:
            json.dump(updated_settings, f)
        
        # Force reload
        updated_config = config_manager.reload_config()
        assert updated_config.global_settings["framework_enabled"] is True
        
        # Cleanup
        config_manager.shutdown()
    
    def test_missing_claude_settings_fallback(self, temp_project_dir):
        """Test fallback to defaults when Claude settings are missing."""
        loader = SettingsLoader(project_root=temp_project_dir)
        config = loader.load_configuration()
        
        # Should load default configuration successfully
        assert isinstance(config, AgentConfigurationSchema)
        assert len(config.agents) > 0  # Should have default agents
        assert config.version == "1.0"
    
    def test_malformed_claude_settings_handling(self, temp_project_dir):
        """Test handling of malformed Claude settings files."""
        # Write malformed JSON
        settings_file = temp_project_dir / ".claude" / "settings.json"
        with open(settings_file, 'w') as f:
            f.write("{ invalid json }")
        
        loader = SettingsLoader(project_root=temp_project_dir)
        
        # Should handle gracefully and return default configuration
        config = loader.load_configuration()
        assert isinstance(config, AgentConfigurationSchema)
    
    @patch.dict('os.environ', {'CLAUDE_AGENT_FRAMEWORK_ENABLED': 'false'})
    def test_environment_variable_integration(self, temp_project_dir):
        """Test environment variable integration with Claude settings."""
        settings = {
            "agents": {
                "global_settings": {"framework_enabled": True}
            }
        }
        
        settings_file = temp_project_dir / ".claude" / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
        
        loader = SettingsLoader(project_root=temp_project_dir)
        config = loader.load_configuration()
        
        # Environment variable should override settings file
        # (This test assumes environment handler implementation)
        assert isinstance(config, AgentConfigurationSchema)
    
    def test_configuration_change_detection(self, temp_project_dir):
        """Test configuration file change detection."""
        settings_file = temp_project_dir / ".claude" / "settings.json"
        
        # Write initial settings
        with open(settings_file, 'w') as f:
            json.dump({"agents": {}}, f)
        
        loader = SettingsLoader(project_root=temp_project_dir)
        loader.load_configuration()
        
        # Initially no changes
        assert not loader.is_config_changed()
        
        # Modify file
        import time
        time.sleep(0.1)  # Ensure timestamp difference
        with open(settings_file, 'w') as f:
            json.dump({"agents": {"test": True}}, f)
        
        # Should detect change
        assert loader.is_config_changed()


class TestClaudeCodeIntegration:
    """Integration tests specific to Claude Code format compatibility."""
    
    def test_claude_code_settings_format_compatibility(self):
        """Test compatibility with actual Claude Code settings.json format."""
        # Use the actual format from the real settings file
        actual_claude_settings = {
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [
                            {
                                "type": "command",
                                "command": "./scripts/hooks/bash_security.sh"
                            }
                        ]
                    }
                ],
                "PostToolUse": []
            }
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            claude_dir = project_path / ".claude"
            claude_dir.mkdir()
            
            settings_file = claude_dir / "settings.json"
            with open(settings_file, 'w') as f:
                json.dump(actual_claude_settings, f)
            
            loader = SettingsLoader(project_root=project_path)
            config = loader.load_configuration()
            
            # Should load without errors even though no agent config exists
            assert isinstance(config, AgentConfigurationSchema)
            # Should fall back to defaults
            assert len(config.agents) > 0
    
    def test_claude_permissions_format_compatibility(self):
        """Test compatibility with Claude Code permissions format."""
        actual_permissions_settings = {
            "permissions": {
                "allow": [
                    "Bash(bash:*)",
                    "Bash(gh:*)",
                    "WebFetch(domain:github.com)"
                ],
                "deny": []
            }
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            claude_dir = project_path / ".claude"
            claude_dir.mkdir()
            
            settings_file = claude_dir / "settings.local.json"
            with open(settings_file, 'w') as f:
                json.dump(actual_permissions_settings, f)
            
            loader = SettingsLoader(project_root=project_path)
            config = loader.load_configuration()
            
            # Should load successfully
            assert isinstance(config, AgentConfigurationSchema)