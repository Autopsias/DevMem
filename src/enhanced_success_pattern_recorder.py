"""Enhanced Success Pattern Recorder for Claude Code Agent Framework.

Records successful agent usage patterns in coordination-hub.md using existing format
for improved future agent selection accuracy.
"""

import re
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class EnhancedSuccessPatternRecorder:
    """Enhanced success pattern recorder using coordination-hub.md existing format."""
    
    def __init__(self, coordination_hub_path: Optional[str] = None):
        """Initialize the pattern recorder."""
        if coordination_hub_path:
            self.coordination_hub_path = coordination_hub_path
        else:
            self.coordination_hub_path = "/Users/ricardocarvalho/DeveloperFolder/DevMem/.claude/memory/coordination-hub.md"
        self.learning_section = "## 9. Agent Learning Pattern System"
        
    def record_successful_usage(self, query: str, selected_agent: str, success_metrics: Dict) -> bool:
        """Record successful agent usage in coordination-hub.md learning section."""
        try:
            pattern_key = self._generate_pattern_key(query, selected_agent)
            
            # Extract keywords from query
            keywords = self._extract_query_keywords(query)
            
            # Create pattern entry
            pattern_entry = {
                'pattern_key': pattern_key,
                'agent': selected_agent,
                'confidence': success_metrics.get('confidence', 1.0),
                'keywords': keywords,
                'learned_date': datetime.now().strftime('%Y-%m-%d'),
                'success_indicators': success_metrics.get('indicators', [])
            }
            
            # Update coordination-hub.md learning patterns section
            return self._update_learning_section(pattern_entry)
            
        except Exception as e:
            logger.error(f"Failed to record successful usage: {e}")
            return False
    
    def _generate_pattern_key(self, query: str, agent: str) -> str:
        """Generate pattern key from query content."""
        query_lower = query.lower()
        
        # Classify query type based on domain keywords
        if any(kw in query_lower for kw in ['test', 'pytest', 'mock', 'coverage', 'async']):
            return 'testing_patterns'
        elif any(kw in query_lower for kw in ['docker', 'container', 'kubernetes', 'infrastructure']):
            return 'container_patterns'
        elif any(kw in query_lower for kw in ['security', 'vulnerability', 'audit', 'compliance']):
            return 'security_patterns'
        elif any(kw in query_lower for kw in ['performance', 'optimization', 'bottleneck', 'resource']):
            return 'performance_patterns'
        elif any(kw in query_lower for kw in ['documentation', 'docs', 'guide', 'readme']):
            return 'documentation_patterns'
        elif any(kw in query_lower for kw in ['quality', 'refactoring', 'architecture', 'pattern']):
            return 'quality_patterns'
        else:
            return 'general_patterns'
    
    def _extract_query_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from user query."""
        technical_keywords = []
        words = query.lower().split()
        
        # Technical terms to capture (expanded list)
        tech_terms = {
            # Testing
            'test', 'testing', 'pytest', 'mock', 'async', 'coverage', 'fixture',
            'unittest', 'validation', 'assert', 'failure',
            
            # Infrastructure
            'docker', 'container', 'kubernetes', 'k8s', 'infrastructure', 'deployment',
            'orchestration', 'networking', 'scaling', 'service', 'helm',
            
            # Security
            'security', 'vulnerability', 'audit', 'compliance', 'scanning',
            'authentication', 'authorization', 'encryption',
            
            # Performance
            'performance', 'optimization', 'bottleneck', 'resource', 'memory',
            'cpu', 'latency', 'throughput', 'profiling',
            
            # Quality
            'quality', 'refactoring', 'architecture', 'pattern', 'design',
            'lint', 'analysis',
            
            # Documentation
            'documentation', 'docs', 'guide', 'readme', 'api', 'technical',
            'writing', 'manual'
        }
        
        for word in words:
            # Clean word of punctuation
            clean_word = re.sub(r'[^a-zA-Z0-9]', '', word)
            
            # Include if it's a technical term or long enough to be meaningful
            if clean_word.lower() in tech_terms or len(clean_word) > 5:
                technical_keywords.append(clean_word.lower())
                
        return technical_keywords[:5]  # Limit to top 5 keywords
    
    def _update_learning_section(self, pattern_entry: Dict) -> bool:
        """Update pattern entry in coordination-hub.md learning section."""
        try:
            # Read current coordination-hub.md content
            if not os.path.exists(self.coordination_hub_path):
                logger.warning(f"Coordination hub not found: {self.coordination_hub_path}")
                return False
                
            with open(self.coordination_hub_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create pattern line in existing format
            pattern_key = f"{pattern_entry['pattern_key']}:{pattern_entry['agent']}"
            keywords_str = ', '.join(pattern_entry['keywords'])
            
            pattern_line = f"- **{pattern_key}**: {pattern_entry['agent']} (confidence: {pattern_entry['confidence']:.2f}, keywords: {keywords_str}, learned: {pattern_entry['learned_date']})"
            
            # Find and update the appropriate section
            updated_content = self._insert_pattern_in_section(content, pattern_entry, pattern_line)
            
            if updated_content != content:
                # Write back to file
                with open(self.coordination_hub_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                logger.info(f"Successfully recorded pattern: {pattern_key}")
                return True
            else:
                logger.warning("No changes made to coordination hub")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update learning section: {e}")
            return False
    
    def _insert_pattern_in_section(self, content: str, pattern_entry: Dict, pattern_line: str) -> str:
        """Insert pattern line in the appropriate section of coordination-hub.md."""
        # Determine target section based on pattern type
        pattern_type = pattern_entry['pattern_key']
        
        section_mapping = {
            'testing_patterns': "**Testing & Quality Assurance Patterns:**",
            'container_patterns': "**Infrastructure & Container Patterns:**",
            'security_patterns': "**Security & Analysis Patterns:**", 
            'performance_patterns': "**Performance & Optimization Patterns:**",
            'documentation_patterns': "**Documentation & Communication Patterns:**",
            'quality_patterns': "**Architecture & Design Patterns:**",
            'general_patterns': "**Testing & Quality Assurance Patterns:**"  # Default fallback
        }
        
        target_section = section_mapping.get(pattern_type, "**Testing & Quality Assurance Patterns:**")
        
        # Find the High-Confidence Learned Patterns section first
        patterns_section_start = content.find("### High-Confidence Learned Patterns")
        if patterns_section_start == -1:
            logger.warning("Could not find High-Confidence Learned Patterns section")
            return content
        
        # Find the target subsection within the patterns section
        section_start = content.find(target_section, patterns_section_start)
        if section_start != -1:
            # Find next section or subsection to determine insertion point
            search_start = section_start + len(target_section)
            
            # Look for next subsection (**...:**) or main section (###)
            next_subsection = content.find("\n**", search_start)
            next_main_section = content.find("\n### ", search_start)
            
            # Determine insertion point (before next section)
            if next_subsection != -1 and (next_main_section == -1 or next_subsection < next_main_section):
                insertion_point = next_subsection
            elif next_main_section != -1:
                insertion_point = next_main_section
            else:
                # Insert at end of content
                insertion_point = len(content)
            
            # Insert the pattern line
            return content[:insertion_point] + "\n" + pattern_line + content[insertion_point:]
        else:
            # Target section not found, try to add it
            logger.info(f"Target section {target_section} not found, attempting to add it")
            return self._add_new_section(content, target_section, pattern_line)
    
    def _add_new_section(self, content: str, section_name: str, pattern_line: str) -> str:
        """Add a new pattern section if it doesn't exist."""
        # Find the High-Confidence section and add the new subsection
        high_confidence_start = content.find("### High-Confidence Learned Patterns")
        if high_confidence_start != -1:
            # Find the end of high-confidence section (before Medium-Confidence or end)
            medium_confidence_start = content.find("### Medium-Confidence Learned Patterns", high_confidence_start)
            if medium_confidence_start != -1:
                insertion_point = medium_confidence_start
            else:
                # Find any other ### section after high-confidence
                next_section = content.find("\n### ", high_confidence_start + 50)
                insertion_point = next_section if next_section != -1 else len(content)
            
            # Insert new section with pattern
            new_section = f"\n{section_name}\n{pattern_line}\n"
            return content[:insertion_point] + new_section + content[insertion_point:]
        
        return content
    
    def get_recorded_patterns_count(self) -> int:
        """Get count of patterns recorded in coordination hub."""
        try:
            if not os.path.exists(self.coordination_hub_path):
                return 0
                
            with open(self.coordination_hub_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count pattern entries (lines starting with "- **" in learning section)
            learning_section_start = content.find("### High-Confidence Learned Patterns")
            if learning_section_start == -1:
                return 0
            
            # Extract learning section content
            next_main_section = content.find("\n## ", learning_section_start)
            learning_content = content[learning_section_start:next_main_section] if next_main_section != -1 else content[learning_section_start:]
            
            # Count pattern lines
            pattern_lines = [line for line in learning_content.split('\n') if line.strip().startswith('- **')]
            return len(pattern_lines)
            
        except Exception as e:
            logger.error(f"Failed to count recorded patterns: {e}")
            return 0
    
    def validate_coordination_hub_format(self) -> bool:
        """Validate that coordination hub has the expected format for learning."""
        try:
            if not os.path.exists(self.coordination_hub_path):
                return False
                
            with open(self.coordination_hub_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required sections
            required_sections = [
                "## 9. Agent Learning Pattern System",
                "### High-Confidence Learned Patterns"
            ]
            
            for section in required_sections:
                if section not in content:
                    logger.warning(f"Required section missing: {section}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate coordination hub format: {e}")
            return False
